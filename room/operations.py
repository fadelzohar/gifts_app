
from talkfest.room.config import *
#from talkfest.collection.operations import *
from talkfest.utility.utilities import *
#from talkfest.user.opreations import *
from talkfest.gift.operations import GiftOperations
import requests

class RoomOperations(RoomConfigDb):

    def __init__(self,id):
        RoomConfigDb.__init__(self,id)
        self.make_db_conn()


    def make_db_conn(self):
        return connection.ping(reconnect=True)



    def fetch_room(self):
        map = {}
        query = "SELECT * FROM rooms WHERE id={rid}".format(rid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if len(fetch) > 0:
            map.update(
                {
                    "room_id": fetch[0][0],
                    "creator_id": fetch[0][1],
                    "is_completed": fetch[0][2],
                    "members": self.fetch_room_members_as_dict(),
                    "votes": self.fetch_room_votes(),
                    "visitors": self.fetch_room_visitors(),

                    "comments": self.fetch_room_comments(),
                    "gifts": self.fetch_room_gifts_enrolled()
                }
            )
        else:
            map = []
        return map



    def fetch_room_comments(self):
        map = []
        query = "SELECT * FROM comments WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for comment in fetch:
            map.append(
                {
                    "comment_id": comment[0],
                    "user_id": comment[1],
                    "text": comment[2]
                }
            )
        return map





    '''
    ------ callback for fetch_room_members method -------
    '''
    def fetch_room_member(self):
        layer_1_class = layer_1_utility(self.fetch_room_members(), "coins_count")
        return layer_1_class.sorting()

    '''  -------------   '''


    def fetch_room_members(self):
        map = []
        query = "SELECT * FROM rooms_members WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for member in fetch:
            map.append(member[2])
        return map

    def fetch_room_members_as_dict(self):
        map = []
        query = "SELECT * FROM rooms_members WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for member in fetch:
            map.append({
                "record_id": member[0],
                "member_id": member[2]
            })
        return map

    def fetch_room_visitors(self):
        #connection.ping(reconnect=True)
        map = []
        query = "SELECT * FROM rooms_visitors WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for hoster in fetch:
            map.append(
                {
                    "record_id": hoster[0],
                    "visitor_id": hoster[1],
                }
            )  
        return map




    def fetch_room_votes(self):
        map = []
        query = "SELECT * FROM rooms_members_votes WHERE rid={rrid}".format(rrid= self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for vote in fetch:
            map.append(
                {
                    "record_id": vote[0],
                    "uid_hoster": vote[3],
                    "uid_visitor": vote[2],
                }
            )
        return map


    def check_is_completed(self):
        query = "SELECT * FROM rooms WHERE id={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if fetch[0][2] == 1:
            return True
        else:
            return False


    def fetch_room_target(self):
        query = "SELECT (target) FROM room_goals WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if len(fetch) > 0:

            return fetch[0]
        else:
            return 0
        

    def check_state(self) -> int:
        query = "SELECT * FROM rooms WHERE id={rid}".format(rid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        return fetch[0][2] 


    def fetch_coins(self):
        map = []
        query = "SELECT * FROM room_coins WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for coin in fetch:
            map.append(
                {
                    "id": fetch[0],
                    "room_id": fetch[1],
                    "uid_buyer": fetch[2],
                    "uid_hoster": fetch[3]
                }
            )
        return map 

         

    def fetch_room_gifts_enrolled(self):
        map = []
        query = "SELECT * FROM room_gift_enrollment WHERE rid={rrid}".format(rrid=self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for gift in fetch:
            GiftOperations_class = GiftOperations(gift[3])
            map.append(
                {
                    "record_id": gift[0],
                    "room_id": gift[1],
                    "member_id": gift[2],
                    "user_gift_info": GiftOperations_class.fetch_gift_info()
                }
            )
        return map


class RoomOperationsList(DbConnection):

    def __init__(self, rid_list):
        self.rid_list = rid_list
        DbConnection.__init__(self)

    def fetch_rooms(self):
        map = []
        for rid in self.rid_list:
            room_class = RoomOperations(rid)
            map.append(room_class.fetch_room())
        return map


    def fetch_room_members(self):
        map = []
        for room in self.rid_list:
            query = "SELECT * FROM rooms_members WHERE rid={rrid}".format(rrid=room)
            self._cursor.execute(query)
            fetch = self._cursor.fetchall()
            for member in fetch:
                map.append(member[2])
        layer_0_utility_class = layer_0_utility(map)
        return layer_0_utility_class.remove_repeated()


    def fetch_room_members_as_dict(self):
        map = []
        for room in self.rid_list:
            query = "SELECT * FROM rooms_members WHERE rid={rid}".format(rid=room)
            self._cursor.execute(query)
            fetch = self._cursor.fetchall()
            room_dict = {"rid": room, "members" : []}
            for member in fetch:
                room_dict["members"].append(member[2])
            map.append(room_dict)
        return map


    def fetch_room_members(self) -> list[dict]:
        map = []
        for room in self.rid_list:
            query = "SELECT * FROM rooms_members WHERE rid={rid}".format(rid=room)
            self._cursor.execute(query)
            fetch = self._cursor.fetchall()
            for member in fetch:
                map.append({

                    "record_id": member[0],
                    "member_id": member[2],
                })
        return map



    def fetch_room_members_as_list(self) -> list:
        map = []
        for room in self.rid_list:
            query = "SELECT * FROM rooms_members WHERE rid={rid}".format(rid=room)
            self._cursor.execute(query)
            fetch = self._cursor.fetchall()
            for member in fetch:
                map.append(member[2])
        return map



ob = RoomOperations(2)
print(ob.fetch_room_visitors())
