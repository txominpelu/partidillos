import datetime
from django.contrib.auth.models import User
from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp.views.matches import MyMatchesListViewHtml
from django.utils.timezone import now

from django import test

oneday = datetime.timedelta(days=1)
yesterday = now() - oneday
tomorrow = now() + oneday

# MyMatches

class MyMatchesListViewHtmlTest(test.TestCase):

    def create_match (self, user, date):
        return Match(creator=user, date=date, place="place")

    # setup
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'email',
                'password').get_profile()
        self.user2 = User.objects.create_user('user2', 'email',
                'password').get_profile()
        print "Now {0}:".format(now())
        print "Tomorrow {0}".format(tomorrow)

        # create a couple of outdated matches with user1
        # create a couple of non-expired matches with user1
        # create a couple of matches with user2
        users = [self.user1, self.user1, self.user2]
        dates = [yesterday, tomorrow, tomorrow]
        self.matches = [ self.create_match(user, date) for user, date in zip(users, dates)]
        for match in self.matches: match.save()
    
        

    def test_mymatches(self):
        # see that making the request with user1 it only sees the matches that are his and are not outdated
        self.assertEqual(1,
                len(MyMatchesListViewHtml().get_mymatches(self.user1)))
        self.assertEqual(self.matches[1],
                MyMatchesListViewHtml().get_mymatches(self.user1)[0])

# Voy a jugar

#create a couple of outdated matches where user1 plays
#create a couple of non-expired matches where user1 plays
#create a couple of non-expired matches where user2 plays
#see that making the request with user1 it only sees the matches that hes going
#to play and are not outdated
