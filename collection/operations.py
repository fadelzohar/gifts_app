from talkfest.collection.config import *
from talkfest.utility.utilities import *
from talkfest.user.opreations import *
from talkfest.room.operations import *
from talkfest.gift.operations import GiftOperations


class UserRoomOperations(UserRoomConfigDb):

    def __init__(self,_id,id) -> None:
        UserRoomConfigDb.__init__(self,_id,id)


    def fetch_room_member_coins(self) -> list:
        map = []
        query = "SELECT * FROM coins WHERE rid={rid} AND uid_hoster={hoster}".format(rid=self.user.id,hoster=self.room.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for coin in fetch:
            map.append(coin[0])
        return map



    def fetch_room_member_gifts_enrollment(self) -> list:
        map = []
        query = "SELECT * FROM room_gift_enrollment WHERE rid={rid} AND member_id={id}".format(rid=self.room.id,id=self.user.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for gift in fetch:
            GiftOperations_class = GiftOperations(gift[2])
            map.append(
                {
                    "record_id": gift[0],
                    "rid": gift[1],
                    "member_id": gift[2],
                    "gift_info": GiftOperations_class.fetch_gift_info()
                }
            )
        return map


    def fetch_room_member_gifts_enrollment_total_coins(self) -> int:
        total = 0
        for gift in self.fetch_room_member_gifts_enrollment():
            total += int(gift['gift_info']['price'])
        return total


    def fetch_room_members_and_coins(self):
        map = []
        RoomOperations_class = RoomOperations(self.room.id)
        for member in RoomOperations_class.fetch_room_members_as_dict():
            #user_room_class = UserRoomOperations(self.id,member[2])
            member['coins'] = RoomOperations_class.fetch_room_member_coins()
            member['coins_count'] = len(RoomOperations_class.fetch_room_member_coins())
            map.append(member)

        return map


    def fetch_room_member_requests(self):
        map = []
        query = "SELECT * FROM room_request WHERE rid={rid} AND uid_to={uid}".format(rid= self.room.id,uid= self.user.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for request in fetch:
            user_ob = UserOperations(request[2])
            map.append(

                {
                    "user_id": user_ob.fetch_user_info(),
                    "room_id": request[1],
                    "request_state": request[3]

                }
            )
        return map


    def add_room_member(self):
        query = "INSERT INTO rooms_members WHERE rid={rid} AND uid_member={uid}".format(rid=self.room.id,uid=self.user.id)
        self._cursor.execute(query)
        connection.commit()
        connection.close()



    def add_coins(self,uid):
        query = "INSERT INTO coins VALUES({rid},{uid_buyer},{uid_hoster})".format(rid=self.room.id,uid_buyer=self.user.id,uid_hoster=uid)
        self._cursor.execute(query)
        connection.commit()
        connection.close()


    def add_user_room_gift(self,gift_id) -> None:
        query = "INSERT INTO users_gifts(user_id,room_id,gift_id) VALUES({user_id},{gift_id},{room_id})".format(user_id=self.user.id,gift_id=gift_id,room_id=self.room.id)
        self._cursor.execute(query)
        connection.commit()


    def fetch_user_room_gifts(self):
        map = []
        query = "SELECT * FROM users_gifts WHERE user_id= {user_id} AND room_id={room_id}".format(user_id=self.user.user.id,room_id=self.room.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for gift in fetch:
            map.append(
                {
                    "record_id": gift[0],
                    "gift_id": gift[2]
                }
            )
        return map


    def fetch_user_room_last_gift(self):
        map = {}
        query = "SELECT * FROM users_gifts WHERE user_id={user_id} AND room_id={room_id}".format(user_id=self.user.id,room_id=self.room.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        map.update({
            "record_id": fetch[len(fetch) -1][0],
            "gift_id": fetch[len(fetch) -1][1]
        })
        return map





ob = UserRoomOperations(1,5)
print(ob.fetch_user_room_last_gift())
