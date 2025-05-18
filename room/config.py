from talkfest.db.db_config import *
from talkfest.config.config import config, ConfigDb


class RoomConfig(config):
    id = None
    def __init__(self,id):
        config.__init__(self,id)



class RoomConfigDb(ConfigDb):

    def __init__(self,id):
        ConfigDb.__init__(self,id)


