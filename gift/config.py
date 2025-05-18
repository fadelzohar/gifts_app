from talkfest.db.db_config import DbConnection


class GiftConfig:

    def __init__(self,id):
        self.id = id

class GiftConfigDb(GiftConfig,DbConnection):

    def __init__(self,id):
        GiftConfig.__init__(self,id)
        DbConnection.__init__(self)




    


