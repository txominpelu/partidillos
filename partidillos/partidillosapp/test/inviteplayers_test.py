from django import test

from partidillos.partidillosapp.views import main
from partidillos.partidillosapp import models

from partidillos import settings


class InvitePlayerTestCase(test.TestCase):

    #when ( request is get ) return form with  fields
    def test_inviteget_noplayers(self):
        
        self.assertEqual(response.context['form']['players'].value(), None)
        self.assertEqual(response.context['form']['place'].value(), None)
        self.assertEqual(response.status_code, 200)

    #when ( request is post ) return form with given fields
    def testCreateMatchPost(self):
        response = self.client.post('/match/create/', 
                {'dia': self.datestr, 'hora': self.timestr, 'place': self.place})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mymatches.html')

