
from django import test

from partidillos.partidillosapp import views
from partidillos.partidillosapp import models

from bunch import Bunch

from datetime import date, time, datetime

from django.test import client
from django.contrib import auth


class CreateCreateMatchFormTestCase(test.TestCase):

    def setUp(self):
        self.date = date(2005, 10, 25)
        self.datestr = self.date.strftime("%Y-%m-%d")
        self.time = time(12, 30)
        self.timestr = self.time.strftime("%H:%M")
        self.datetime = datetime.combine(self.date, self.time)
        self.place = "My place"

    #when( theres no place) return form with error indicating no place
    def testNoPlace(self):
        form = views._create_creatematchform(self.timestr, self.datestr,
            "")
        self.assertEqual(form['date'].value(), self.datetime) #Unauthorized
        self.assertFalse(form['place'].value())

    #when( theres no day) return form with no date
    def testNoDay(self):
        form = views._create_creatematchform(self.timestr, "", self.place)
        self.assertEqual(form['date'].value(), None) #Unauthorized
        self.assertEqual(form['place'].value(), self.place)

    #when( theres no time) return form with error indicating no time
    def testNoTime(self):
        form = views._create_creatematchform("", self.datestr, self.place)
        self.assertEqual(form['date'].value(), None) #Unauthorized
        self.assertEqual(form['place'].value(), self.place)

    #when( day and time but one of them doesnt have right format) return error date in the wrong format
    def testWrongDateFormat(self):
        form = views._create_creatematchform("wrongtime", self.datestr, self.place)
        self.assertEqual(form['date'].value(), None) #Unauthorized
        self.assertEqual(form['place'].value(), self.place)
        self.assertFalse(form.is_valid())

    #when( all is right) redirect to partidillos, is saving the match
    def testCreateMatchRightPost(self):
        form = views._create_creatematchform(self.timestr, self.datestr, self.place)
        self.assertEqual(form['date'].value(), self.datetime) #Unauthorized
        self.assertEqual(form['place'].value(), self.place)
        self.assertTrue(form.is_valid())


class CreateMatchTestCase(test.TestCase):

    def setUp(self):
        self.date = date(2005, 10, 25)
        self.datestr = self.date.strftime("%Y-%m-%d")
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
        response = self.client.get('/partidillos/create-match.html')
        self.assertEqual(response.context['form']['date'].value(), None)
        self.assertEqual(response.context['form']['place'].value(), None)
        self.assertEqual(response.status_code, 200)

    #when ( request is post ) return form with given fields
    def testCreateMatchPost(self):
        response = self.client.post('/partidillos/create-match.html', 
                {'dia': self.datestr, 'hora': self.timestr, 'place':
                    self.place})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/partidillos/index.html')

