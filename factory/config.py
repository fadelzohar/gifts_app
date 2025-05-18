from talkfest.db.db_config import *
from talkfest.static.operations import StaticOperations
from talkfest.security.security_rules import *
from talkfest.collection.config import UserRoomConfig, UserRoomConfigDb
from talkfest.Query.config import QueryConfig
from talkfest.config.config import config,ConfigSecure,ConfigSecureDb ,DbConnection, ConfigDb
from talkfest.user.config import UserConfig


class FactoryConfig(config):

    def __init__(self,id):
        config.__init__(self,id)

class FactoryConfigDb(ConfigDb):

    def __init__(self,id):
        ConfigDb.__init__(self,id)


class FactoryConfigSecure(ConfigSecure):
    def __init__(self,id):
        ConfigSecure.__init__(self,id)



class FactoryConfigSecureDb(ConfigSecureDb):

    def __init__(self,id):
        ConfigSecureDb.__init__(self,id)


class FactoryStaticConfig(StaticOperations):

    def __init__(self):
        super().__init__()


class UserRoomFactoryConfigSecure(UserRoomConfig):

    def __init__(self,*args):

        UserRoomConfig.__init__(self,FactoryConfigSecure(args[0]),FactoryConfigSecure(args[1]))


class QueryFactoryConfig(QueryConfig):

    def __init__(self,query):
        SecurityGate_class = SecurityGate(query)
        QueryConfig.__init__(self,SecurityGate_class.filter_string())



