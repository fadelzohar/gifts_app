
from talkfest.db.db_config import DbConnection
from talkfest.security.security_rules import SecurityGate


class config:

    def __init__(self,id) -> None:
        self.id = id

class ConfigQuery:

    def __init__(self,query):
        self.query = query


class ConfigQuerySecure(ConfigQuery):


    def __init__(self,query):
        SecurityGate_class = SecurityGate(query)
        ConfigQuery.__init__(self,SecurityGate_class.filter_string())


class ConfigSecure(config):

     def __init__(self,id) -> None:
         SecurityGate_class = SecurityGate(id)
         config.__init__(self,SecurityGate_class.filter_integer())


class ConfigSecureDb(ConfigSecure,DbConnection):
    def __init__(self,id):
        ConfigSecure.__init__(self,id)
        DbConnection.__init__(self)


class ConfigDb(config,DbConnection):

    def __init__(self,id) -> None:
        config.__init__(self,id)
        DbConnection.__init__(self)


