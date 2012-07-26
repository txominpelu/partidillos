import unittest
from partidillos.partidillosapp.views import main
from partidillos.partidillosapp import models

from bunch import Bunch
import json

class DjangoBunch(Bunch):

    def save(self):
        pass

class MyRelatedManager(list):

    def all(self):
        return self

    def add(self, element):
        self.append(element)


class JoinTestCase(unittest.TestCase):

    def setUp(self):
        self.match = DjangoBunch(date="", place="", players=MyRelatedManager())

    def testJoinMatchNoUser(self):
        self.assertEqual(main.join(None, self.match).status_code, 403) #Unauthorized
        #assert(joinMatch(None, match) explains that theres no user) #Unauthorized
        self.assertEqual(len(self.match.players), 0)

    def testJoinMatchUserAlreadyInMatch(self):
        user = Bunch()
        self.match.players.append(user)
        self.assertEqual(main.join(user, self.match).status_code, 403) #Precondition failed
        self.assertEqual(len(self.match.players), 1)
        #assert(joinMatch(user, match) explains that user is already in match) #Precondition failed

    def testJoinMatch(self):
        user = Bunch(name="user")
        response = main.join(user, self.match )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user in self.match.players)

class LeaveTestCase(unittest.TestCase):

    def setUp(self):
        self.match = DjangoBunch(date="", place="", players=MyRelatedManager())
        self.user = DjangoBunch(name="player1")
        self.match.players.append(self.user)

    def testJoinMatchNoUser(self):
        self.assertEqual(main.leave(None, self.match).status_code, 403) #Unauthorized
        #assert(joinMatch(None, match) explains that theres no user) #Unauthorized
        self.assertEqual(len(self.match.players), 1)

    def testLeaveMatchUserNotInMatch(self):
        self.assertEqual(main.leave(DjangoBunch(name="player2"), self.match).status_code, 403) #Precondition failed
        self.assertEqual(len(self.match.players), 1)
        #assert(joinMatch(user, match) explains that user is already in match) #Precondition failed

    def testLeaveMatch(self):
        response = main.leave(self.user, self.match )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(not self.user in self.match.players)



