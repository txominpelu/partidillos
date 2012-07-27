from django import test

from partidillos.partidillosapp.views import main
from partidillos.partidillosapp import models

from bunch import Bunch

from datetime import date, time, datetime

from django.test import client
from django.contrib import auth

from pytz import timezone
from django.utils.timezone import utc

from partidillos import settings

class GetDateTestCase(test.TestCase):

    def setUp(self):
        self.date = date(2005, 10, 25)
        self.datestr = self.date.strftime("%d-%m-%Y")
        self.time = time(12, 30)
        self.timestr = self.time.strftime("%H:%M")
        self.datetime = timezone('Europe/Madrid').localize(datetime.combine(self.date, self.time))

    #when( theres no place) return form with error indicating no place
    def test_good_date(self):
        self.assertEqual(main._get_date(self.timestr, self.datestr), 
                self.datetime) 

    #when( theres no day) return none
    def test_no_day(self):
        self.assertEqual(main._get_date(self.timestr, ""), None) 

    #when( theres no time) return none
    def test_no_time(self):
        self.assertEqual(main._get_date("",self.datestr), None) 

    #when( day and time but one of them doesnt have right format) return none
    def test_wrong_format(self):
        self.assertEqual(main._get_date("wrongformat",self.datestr), None) 

class CreateFormTestCase(test.TestCase):

    def setUp(self):
        auth.models.User.objects.create_user('temporary',
                'temporary@gmail.com', 'temporary')
        self.zone = timezone(settings.TIME_ZONE)
        self.datetime = timezone('Europe/Madrid').localize(datetime.combine(date(2005, 10, 25), time(12, 30)))
        self.place = "My place"
        self.user = 1

    #when( theres no place) return form with error indicating no place
    def test_no_place(self):
        form = main._create_form(self.datetime, "", self.user)
        self.assertEqual(self.zone.localize(form['date'].value()), self.datetime) #Unauthorized
        self.assertFalse(form['place'].value())
        self.assertFalse(form.is_valid())


    #when( all is right) form is valid
    def test_all_right(self):
        form = main._create_form(self.datetime,
                self.place, self.user)
        self.assertEqual(self.zone.localize(form['date'].value()), self.datetime) 
        self.assertEqual(form['place'].value(), self.place)
        self.assertTrue(form.is_valid())


class CreateMatchTestCase(test.TestCase):

    def setUp(self):
        self.date = date(2005, 10, 25)
        self.datestr = self.date.strftime("%d-%m-%Y")
        self.time = time(12, 30)
        self.timestr = self.time.strftime("%H:%M")
        self.datetime = datetime.combine(self.date, self.time)
        self.place = "My place"
        auth.models.User.objects.create_user('temporary', 'temporary@gmail.com',
                'temporary')
        self.client = client.Client()
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        auth.models.User.objects.get(pk=1).delete()

    #when ( request is get ) return form with empty fields
    def testCreateMatchGet(self):
        response = self.client.get('/match/create/')
        self.assertEqual(response.context['form']['date'].value(), None)
        self.assertEqual(response.context['form']['place'].value(), None)
        self.assertEqual(response.status_code, 200)

    #when ( request is post ) return form with given fields
    def testCreateMatchPost(self):
        response = self.client.post('/match/create/', 
                {'dia': self.datestr, 'hora': self.timestr, 'place': self.place})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mymatches.html')

