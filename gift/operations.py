from talkfest.gift.config import GiftConfig,GiftConfigDb


class GiftOperations(GiftConfigDb):

    def __init__(self,id):
        GiftConfigDb.__init__(self,id)


    def fetch_gift_info(self):
        map = {}
        query = "SELECT * FROM gifts WHERE id={id}".format(id = self.id)
        self._cursor.execute(query)
        fetch = self._cursor.fetchall()
        if len(fetch) != 0:
            map.update(
                {
                    "gift_id": fetch[0][0],
                    "name": fetch[0][1],
                    "price": int(fetch[0][2])
                }
            )
        return map
