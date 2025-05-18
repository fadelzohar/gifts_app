from talkfest.db.db_config import DbConnection
from talkfest.user.config import UserConfig
from talkfest.room.config import RoomConfig
from talkfest.vote.config import *
from talkfest.config.config import config

class UserRoomConfig(UserConfig,RoomConfig):
    def __init__(self,*args):
        self.user: config = config(args[0])
        self.room: config = config(args[1])


class UserRoomConfigDb(DbConnection):
    
    def __init__(self,*args):
        self.user: config = config(args[0])
        self.room: config = config(args[1])
        DbConnection.__init__(self)
    


class UserRoomVoteConfigDb(VoteConfig,RoomConfig,DbConnection):

    def __init__(self,_id,id):
        VoteConfig.__init__(self,_id)
        RoomConfig.__init__(self,id)
        DbConnection.__init__(self)