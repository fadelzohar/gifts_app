from markdown_it.rules_block import fence

from talkfest.collection.config import UserRoomConfigDb
from talkfest.country.operations import CountryOperations
from talkfest.user.opreations import UserOperations,UsersOperationsList
from talkfest.room.operations import RoomOperations,RoomOperationsList
from talkfest.ml.apriori_model import Apriori, FitDataUser, FitData, FitDataStatic
from talkfest.factory.config import FactoryStaticConfig, QueryFactoryConfig, FactoryConfigSecure, \
    UserRoomFactoryConfigSecure
from talkfest.collection.operations import UserRoomOperations
from talkfest.supervisor.config import BugSupervisor
from talkfest.gift.operations import GiftOperations
from talkfest.static.operations import StaticOperations
from talkfest.collection.config import UserRoomConfig
from talkfest.Query.operations import QueryOperations


class FactoryId(FactoryConfigSecure,BugSupervisor):

    def __init__(self,id):
        FactoryConfigSecure.__init__(self,int(id))
        BugSupervisor.__init__(self)

    def fetch_user_profile(self) -> dict:
        user_ob = UserOperations(self.id)
        return user_ob.fetch_profile()

    def fetch_user_image(self):
        user_ob = UserOperations(self.id)
        return user_ob.get_image()

    def prapare_home_recomendation(self) -> list:
        ObUser = FitDataUser([], [], 2)
        ObSystem = FitDataStatic([],[])
        aproiri_class = Apriori(ObUser.prepare_data_fit(),ObSystem.visitor_map_as_fitdata_class())
        return aproiri_class.y_parallel_to_x_values()


    def fetch_user_home_recommendation_main(self):
        map = []
        for user in self.prapare_home_recomendation():
            user_ob = UserOperations(user)
            map.append(
                {
                    "user_id": user,
                    "last_room_id": user_ob.fetch_user_last_room_not_completed()
                }
            )
        return map



    def fetch_user_home_recomendation(self) -> list:
        map = []
        for user in self.prapare_home_recomendation():
            user_class = UserOperations(user)
            map.append(user_class.fetch_profile())
        return map


    def update_user_image(self, image):
        ObUser = UserOperations(self.id)
        ObUser.add_info("image", image)


    def fetch_user_home_recomendation_as_country_main(self):
        map = []
        UserOperations_class = UserOperations(self.id)
        country_id = UserOperations_class.fetch_user_country()
        CountryOperations_class = CountryOperations(country_id)
        '''
        return best users have coins ids
        '''
        users_coins_sorted = CountryOperations_class.fetch_user_country_users_coins_as_id()

        '''
        return last room from these users
        '''
        for user in users_coins_sorted:
            ob_user = UserOperations(user)
            map.append(
                {
                    "user_id": user,
                    "last_room": ob_user.fetch_user_last_room_not_completed()
                }
            )
        return map



    def fetch_user_home_recomendation_logic(self) -> list:
        map = []
        if self.fetch_user_home_recommendation_main() == []:
            map.extend(self.fetch_user_home_recomendation_as_country_main())
        else:
            map.extend(self.fetch_user_home_recommendation_main())
        return map


    def update_or_add_user_info(self,query,value) -> None:
        try:
            user_class = UserOperations(self.id)
            user_class.add_info(query, value)
            return "success"
        except:
            return "error"


    def add_coin(self,rid,buyer_id,member_id):
        try:
            UserRoomOperations_class = UserRoomOperations(rid, buyer_id)
            UserRoomOperations_class.add_coins(member_id)
        except:
            return "error"

    def fetch_user_giftes_current(self) -> list:
        map = []
        user_class = UserOperations(self.id)
        giftes = user_class.fetch_user_giftes()
        total_cash = int(user_class.fetch_user_cash_total())
        for gift in giftes:
            try:
                if int(gift["gift_info"]["price"]) <= total_cash:
                    map.append(gift["gift_info"])
                    total_cash -= int(gift['gift_info']['price'])
            except:
                pass
        return map



    def fetch_user_total_cash(self):
        user_class = UserOperations(self.id)
        return user_class.fetch_user_cash_total()


    def fetch_user_total_giftes(self):
        user_class=  UserOperations(self.id)
        return user_class.fetch_user_giftes()


    def fetch_room_members_gifts_enrollment(self) -> list:
        self.add_bug('ff','kk')
        map = []
        RoomOperations_class = RoomOperations(self.id)
        room_members = RoomOperations_class.fetch_room_members_as_dict()
        self.add_bug('ee','fgf')
        for member in room_members:
            self.add_bug('in', 'gfg')
            UserRoomOperations_class = UserRoomOperations(self.id,member['member_id'])
            member['gifts_enrollment'] = UserRoomOperations_class.fetch_room_member_gifts_enrollment()
            member['total'] = UserRoomOperations_class.fetch_room_member_gifts_enrollment_total_coins()
            map.append(member)
        return map


    def fetch_room_profile(self):
        RoomOperations_class = RoomOperations(self.id)
        return RoomOperations_class.fetch_room()

    def fetch_gifts_info(self):
        GiftOperations_class = GiftOperations(self.id)
        return GiftOperations_class.fetch_gift_info()



class QueryFactoryOperations(QueryFactoryConfig):

    def __init__(self,query):
        QueryFactoryConfig.__init__(self,query)


    def search_for_user(self):
        QueryOperations_class = QueryOperations(self.query)
        return QueryOperations_class.search_user()

    def search_for_code(self):
        QueryOperations_class = QueryOperations(self.query)
        return QueryOperations_class.search_code()






class FactoryStaticOperations:
    
    def __init__(self) -> None:
        return None

    def fetch_gifts_info(self):
        StaticOperations_class = StaticOperations()
        return StaticOperations_class.fetch_gifts_info()


    def fetch_all_users_names(self):
        StaticOperations_class = StaticOperations()
        return StaticOperations_class.fetch_all_users_names()

    def fetch_all_rooms_codes(self):
        StaticOperations_class = StaticOperations()
        return StaticOperations_class.fetch_all_rooms_codes()

class UserRoomFactoryOperations(UserRoomFactoryConfigSecure):

    def __init__(self,_id,id):
        UserRoomFactoryConfigSecure.__init__(self,_id,id)

    def fetch_room_member_gifts_enrollment(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self._id,self.id)
        return UserRoomOperations_class.fetch_room_member_gifts_enrollment()

    def add_room_member(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self._id,self.id)
        return UserRoomOperations_class.add_room_member()


    def add_user_room_gift(self, gift_id) -> list:
        UserRoomOperations_class = UserRoomOperations(self._id,self.id)
        return UserRoomOperations_class.add_user_room_gift(gift_id)


    def fetch_user_room_gifts(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self._id,self.id)
        return UserRoomOperations_class.fetch_user_room_gifts()


    def fetch_user_room_last_gift(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self._id,self.id)
        return UserRoomOperations_class.fetch_user_room_last_gift()



'''

class FactorDoubleId(FactoryConfigDoubleId):

    def __init__(self,query1,query2) -> None:
        FactoryConfigDoubleId.__init__(self,query1,query2)

    def fetch_room_member_gifts_enrollment(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self.query1,self.query2)
        return UserRoomOperations_class.fetch_room_member_gifts_enrollment()

    def add_room_member(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self.query1,self.query2)
        return UserRoomOperations_class.add_room_member()


    def add_user_room_gift(self, gift_id) -> list:
        UserRoomOperations_class = UserRoomOperations(self.query1,self.query2)
        return UserRoomOperations_class.add_user_room_gift(gift_id)


    def fetch_user_room_gifts(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self.query1,self.query2)
        return UserRoomOperations_class.fetch_user_room_gifts()


    def fetch_user_room_last_gift(self) -> list:
        UserRoomOperations_class = UserRoomOperations(self.query1,self.query2)
        return UserRoomOperations_class.fetch_user_room_last_gift()

'''













ObSystem = FitDataStatic([],[])
print(ObSystem.visitor_map_as_fitdata_class())
ob = FactoryId(1)
print("ff")
print(ob.fetch_user_home_recomendation())

ob_user = FactoryId(1)
print(ob_user.fetch_user_total_cash())
print(ob_user.fetch_user_total_giftes())
print(ob_user.fetch_user_total_cash())
print(ob_user.fetch_user_giftes_current())
print(ob_user.fetch_room_members_gifts_enrollment())
print(ob_user._map)
print("hint2")
print(ob_user.prapare_home_recomendation())
ob.update_user_image("gfgfgfdfdsfds")
print(ob.fetch_user_home_recomendation_as_country_main())
print(ob_user.fetch_user_home_recommendation_main())
print(ob.fetch_room_profile())


