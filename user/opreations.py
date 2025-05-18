from talkfest.gift.config import GiftConfigDb
from talkfest.room.operations import RoomOperationsList, RoomOperations
from talkfest.user.config import *
from talkfest.utility.utilities import *
from talkfest.gift.operations import GiftOperations
from talkfest.reciept.operations import RecieptOperations
from talkfest.reciept.config import config as RecieptConfig
import codecs
#from talkfest.ml.apriori_model import FitData
#from talkfest.static.operations import StaticOperations
import json



'''
class of operations for users attribute as
-- id
-- DbConnection
'''


class UserOperations(UserConfigDbSupervisor):

    def __init__(self, _id):
        UserConfigDb.__init__(self, _id)
        self.make_db_conn()

    # create user identity only in database
    def create_user(self):
        query = "INSERT INTO users(name,at_name,email,phone_num,pass,image) VALUES('','','','','','')"
        self._cursor.execute(query)
        connection.commit()
        connection.close()



    '''
    add user info as
    -- query
    -- value
    '''
    def add_info(self,query, value):
        q = "UPDATE users SET {_query} = '{_value}' WHERE id={_id}".format(_query=query, _value=value,_id=self._id)
        self._cursor.execute(q)
        connection.commit()

    def make_db_conn(self):
        return connection.ping(reconnect=True)

    def fetch_profile(self):
        return {
            "user_id": self._id,
            "info": self.fetch_user_info(),
            "rooms": self.fetch_rooms(),
            "followers": self.fetch_user_followers(),
            "following": self.fetch_user_following(),
            "room_requests": self.fetch_user_requests(),
            "coins": self.fetch_user_coins(),
            "image": self.get_image()
        }


    def fetch_user_info(self):
        map = {}
        query = "SELECT * FROM users WHERE id={id}".format(id =self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if len(fetch) > 0:
            map.update({
                "name": fetch[0][1],
                "@name": fetch[0][2]
            })
        return map


    '''
    fetch room he was created
    '''
    def fetch_rooms(self):
        map = []
        query = "SELECT * FROM rooms WHERE uid_creator={id}".format(id = self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for room in fetch:
            room_class = RoomOperations(room[0])
            map.append(
                {
                    "id": room[0],
                    #"hosters": room_class.fetch_room_hoster(),
                    "members": room_class.fetch_room_members(),
                }
            )
        return map

    def fetch_rooms_not_completed(self):
        map = []
        query = "SELECT * FROM rooms WHERE uid_creator={id} AND is_completed=0".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for room in fetch:
            room_class = RoomOperations(room[0])
            map.append(
                {
                    "id": room[0],
                    "members": room_class.fetch_room_members()

                }
            )
        return map

    def fetch_user_followers(self) -> list:
        map = []
        query = "SELECT * FROM follows WHERE following_id={id}".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for user in fetch:
            map.append(user[1])
        return map



    def fetch_user_following(self):
        map = []
        query = "SELECT * FROM follows WHERE follower_id={id}".format(id = self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for user in fetch:
            map.append(user[2])
        return map

    def get_image(self):
        profile_sel_query = "SELECT * FROM users WHERE id={0}".format(self._id)
        self._cursor.execute(profile_sel_query)
        profile_sel_fetch = self._cursor.fetchall()
        if len(profile_sel_fetch) != 0:
            try:
                image_profile = codecs.decode(profile_sel_fetch[0][7])

                return image_profile
            except:
                return None
        else:
            return None



    def fetch_user_last_room_not_completed(self):
        map = []
        query = "SELECT * FROM rooms WHERE uid_creator={id} AND is_completed=0".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if len(fetch) > 0:

            return fetch[len(fetch) - 1][0]



    def fetch_user_requests(self) -> list:
        map = []
        query = "SELECT * FROM room_request WHERE uid_to={uid_to}".format(uid_to=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for request in fetch:
            if request[3] == 0:
                map.append({
                    "request_id": request[0],
                    "room_id": request[1],
                })
        return map 


    def fetch_user_coins(self) -> list:
        map = []
        query = "SELECT * FROM coins WHERE uid_buyer={uid}".format(uid=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for coin in fetch:
            map.append(
                {
                    'id': fetch[0],
                    'room_id': fetch[1],
                    'uid_member': fetch[2],
                }
            )   
        return map



    def fetch_user_total_votes(self) -> list[dict]:
        map = []
        query = "SELECT * FROM rooms_members_votes WHERE uid_member={id}".format(id= self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for vote in fetch:
            map.append(
                {
                    "vote_id": vote[0]
                }
            )
        return map


    def fetch_user_messeges_from(self):
        map = []
        query = "SELECT * FROM chats WHERE uid_from={id}".format(id= self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for messege in fetch:
            map.append(
                {
                    "record_id": messege[0],
                    "receiver": messege[3],
                    "messege": messege[4],
                    "date_established": messege[1]

                }
            )
        return map


    def fetch_user_messege_to(self):
        map = []
        query = "SELECT * FROM chats WHERE uid_to={id}".format(id= self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for messege in fetch:
            map.append(
                {
                    "record_id": messege[0],
                    "sender": messege[2],
                    "messege": messege[4],
                    "date_established": messege[1]
                }

            )
        return map

    '''
    prepare for data training in ml model
    '''

    def fetch_user_visitor_rooms(self) -> list:
        map = []
        #map = FitData([],[])
        query = "SELECT * FROM rooms_visitors WHERE uid_visitor={uid}".format(uid=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for visit in fetch:
            map.append(visit[2])
        return map

    def fetch_user_visitor_rooms_members(self):
        RoomOperationsList_class = RoomOperationsList(self.fetch_user_visitor_rooms())
        return RoomOperationsList_class.fetch_room_members_as_list()


    def fetch_user_country(self):
        query = "SELECT * FROM users WHERE id={id}".format(id =self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        return fetch[0][1]


    def fetch_user_coins_earn(self) -> list:
        map = {"uid": self._id, "coins": 0}
        query = "SELECT * FROM coins WHERE uid_hoster={uid}".format(uid=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for coin in fetch:
            if coin[3] == self._id:
                map['coins'] = map['coins'] + 1
        return map



    def fetch_user_cash(self):
        map = []
        query = "SELECT * FROM users_cash WHERE user_id={id}".format(id= self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for cash in fetch:
            map.append(
                {
                    "id": cash[0],
                    "withdraw_or_deposit": cash[3],
                    "quantity": cash[2]
                }
            )
        return map


    def fetch_user_cash_total(self):
        layer_1_utility_class = layer_1_utility(self.fetch_user_cash(), "withdraw_or_deposit")
        return int(layer_1_utility_class.find_total_0_or_1())



    def fetch_user_giftes(self):
        map = []
        query = "SELECT * FROM users_gifts WHERE user_id={id}".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for gift in fetch:
            GiftOperations_class = GiftOperations(gift[2])
            self.add_bug("here", 'something')

            map.append({
                "record_id": gift[0],
                "gift_id": gift[2],
                "gift_info": GiftOperations_class.fetch_gift_info()

            })
        map.reverse()
        return map



    def fetch_user_gifts_enrollment(self):
        map = []
        query = "SELECT * FROM room_gift_enrollment WHERE member_id={id}".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for gift in fetch:
            GiftOperations_class = GiftOperations(gift[1])
            map.append(GiftOperations_class.fetch_gift_info())
        return map


    def fetch_user_giftes_have_now(self):
        map = []
        total_cash = self.fetch_user_cash_total()
        total_gifts = self.fetch_user_giftes()
        total_gifts.reverse()
        for gift in total_gifts:
            if gift['gift_info']['price'] < total_cash:
                map.append(gift)
        return map


    def fetch_user_reciepts(self):
        map = []
        query = "SELECT * FROM user_reciepts WHERE user_id={id}".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        for reciept in fetch:
            map.append(
                {
                    "reciept_id": reciept[0],
                    "user_id": reciept[1],
                    "image": "",
                    "done": reciept[3]
                }
            )
        map.reverse()
        return map


    def create_room(self, date_established, date_start):
        self.make_db_conn()
        query = "INSERT INTO rooms(uid_creator,is_completed,period,date_established,date_start) VALUES({id},0,1,'{date_0}','{date_1}')".format(id=self._id,date_0=date_established,date_1=date_start)
        self._cursor.execute(query)
        connection.commit()
        #connection.close()

    def add_reciept(self,phone_num,serial_num) -> None:
        query = "INSERT INTO user_reciept(user_id,image,done,phone_num,serial_num) VALUES({id},'',{is_done},'{phone_num}','{serial_num}')".format(id=self._id,is_done=0,phone_num=phone_num,serial_num=serial_num)
        self._cursor.execute(query)
        connection.commit()
        #connection.close()


    def fetch_user_last_room(self):
        map = {}
        query = "SELECT * FROM rooms WHERE uid_creator={id}".format(id=self._id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        index = len(fetch) - 1
        while fetch[index] == 1:
            index -= 1

        map.update({
            'room_id': fetch[index][0],
            "is_completed": fetch[index][2],
            "date_established": fetch[index][4],
            "date_start": fetch[index][5]
        })
        return map




'''

class UserRecieptsOperations(UserConfigDb,RecieptConfig):
    
    def __init__(self,_id):
        UserConfigDb.__init__(self,_id)
        RecieptConfig.__init__(self)
        
    def add_reciept(self):
        query = "INSERT INTO user_reciept(u)"

'''





class UsersOperationsList:

    def __init__(self,id_list):
        self.id_list = id_list

    def fetch_users_profiles(self):
        map = []
        for user in self.id_list:
            user_operations_class = UserOperations(user)
            map.append(user_operations_class.fetch_profile())

        return map

    def fetch_users_rooms(self):
        map = []
        for user in self.id_list:
            UserOperations_class = UserOperations(user)
            map.append(UserOperations_class.fetch_rooms_not_completed())

        return map

    def fetch_users_last_room(self):
        map = []
        for user in self.id_list:
            UserOperations_class = UserOperations(user)
            map.append(UserOperations_class.fetch_user_last_room())
        return map


    def fetch_users_votes(self):
        map = []
        for user in self.id_list:
            user_operations_class = UserOperations(user)
            votes = user_operations_class.fetch_user_total_votes()
            map.append(
                {
                    "user_id": user,
                    "votes": votes,
                    "votes_count": len(votes)
                }
            )
        return map

    def fetch_users_votes_sorted(self) -> list:
        layer_1_utility_class = layer_1_utility(self.id_list, "votes_count")
        sorted = layer_1_utility_class.sorting()
        return sorted.reverse()




ob = UserOperations(2)
print(ob.fetch_user_giftes())
print(ob.fetch_user_cash_total())
print(ob.fetch_user_giftes_have_now())
print("hint")
obj = UsersOperationsList([1,2,3])
print(obj.fetch_users_last_room())
print(ob.fetch_user_visitor_rooms_members())
ob.add_reciept('1212','1212')
#ob.create_room("11-11-11","12-11-11")


