from talkfest.db.db_config import DbConnection , connection
from talkfest.supervisor.config import BugSupervisor

class UserConfig:
    # public
    _id = None

    def __init__(self, _id: int):
        self._id = _id


class UserConfigDb(UserConfig, DbConnection):

    def __init__(self, _id):
        UserConfig.__init__(self, _id)
        DbConnection.__init__(self)


class UserConfigDbSupervisor(UserConfigDb,BugSupervisor):

    def __init__(self,_id):
        UserConfigDb.__init__(self,_id)
        BugSupervisor.__init__(self)

