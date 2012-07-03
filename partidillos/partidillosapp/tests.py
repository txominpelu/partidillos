import unittest
from partidillos.partidillosapp import views
from partidillos.partidillosapp import models

from bunch import Bunch
import json

class DjangoBunch(Bunch):

    def save(self):
        pass

class JoinTestCase(unittest.TestCase):

    def setUp(self):
        self.match = DjangoBunch(date="", place="", players=[])

    def testJoinMatchNoUser(self):
        self.assertEqual(views.join(None, self.match).status_code, 403) #Unauthorized
        #assert(joinMatch(None, match) explains that theres no user) #Unauthorized
        self.assertEqual(len(self.match.players), 0)

    def testJoinMatchUserAlreadyInMatch(self):
        user = Bunch()
        self.match.players.append(user)
        self.assertEqual(views.join(user, self.match).status_code, 403) #Precondition failed
        self.assertEqual(len(self.match.players), 1)
        #assert(joinMatch(user, match) explains that user is already in match) #Precondition failed

    def testJoinMatch(self):
        user = Bunch(name="user")
        response = views.join(user, self.match, serializer )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user in self.match.players)


class LeaveTestCase(unittest.TestCase):

    def setUp(self):
        self.match = DjangoBunch(date="", place="", players=[])
        self.user = Bunch("player1")
        self.match.players.append(user)

    def testJoinMatchNoUser(self):
        self.assertEqual(views.leave(None, self.match).status_code, 403) #Unauthorized
        #assert(joinMatch(None, match) explains that theres no user) #Unauthorized
        self.assertEqual(len(self.match.players), 1)

    def testLeaveMatchUserNotInMatch(self):
        self.assertEqual(views.leave(Bunch("player2"), self.match).status_code, 403) #Precondition failed
        self.assertEqual(len(self.match.players), 1)
        #assert(joinMatch(user, match) explains that user is already in match) #Precondition failed

    def testLeaveMatch(self):
        response = views.leave(self.user, self.match )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user in self.match.players)



