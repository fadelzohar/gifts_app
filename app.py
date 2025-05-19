import json

from flask import Flask, jsonify, request

from talkfest.collection.operations import UserRoomOperations
from talkfest.factory.absolute_render import FactoryId, FactoryStaticOperations, UserRoomFactoryOperations
from flask_cors import CORS, cross_origin
app = Flask(__name__)


CORS(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/gg")
def g():
    return "ggvfdsddv"




'''
API for USER
'''
@app.route('/add/image', methods=["POST", "GET"])
def debug2():


    image_url = request.form['photo']
    ob = FactoryId(2)
    ob.update_user_image(image_url)

    return {"done": len(image_url)}

@app.route("/user/profile/<id>", methods=["GET"])
def user_profile(id):
    ob = FactoryId(id)
    fetch = ob.fetch_user_profile()
    return json.dumps(fetch)

@app.route("/user/image/<id>", methods=['GET'])
def user_image(id):
    ob = FactoryId(int(id))
    fetch = ob.fetch_user_image()
    return json.dumps({"user_image": fetch})

@app.route("/home/<id>", methods =["GET"])
def home(id):
    ob = FactoryId(id)
    fetch = ob.fetch_user_home_recomendation_logic()
    return json.dumps(fetch)

'''
end API for USER
'''

'''
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
'''


'''
API for ROOMS
'''

@app.route("/room/gifts/<id>", methods=["GET"])
def room_gifts(id):
    ob = FactoryId(int(id))
    fetch = ob.fetch_room_members_gifts_enrollment()
    return json.dumps(fetch)

@app.route("/room/profil/<id>", methods=["GET"])
def room_profile(id):
    ob = FactoryId(int(id))
    fetch = ob.fetch_room_profile()
    return json.dumps(fetch)


'''
end API for ROOMS
'''



'''
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
'''



'''
API for GIFTS
'''

@app.route("/gift/info/<id>")
def gift_info(id):
    ob = FactoryId(int(id))
    fetch = ob.fetch_gifts_info()
    return json.dumps(fetch)

@app.route("/gifts/info", methods=["GET"])
def gifts_info():
    ob = FactoryStaticOperations()
    return ob.fetch_gifts_info()


'''
end API for GIFTS
'''

'''
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
'''


'''
API for USER and ROOM
'''


@app.route("/room/member/gifts/<user_id>/<room_id>", methods=["GET"])
def room_member_gifts(user_id,room_id):
    ob = UserRoomFactoryOperations(user_id,room_id)
    fetch = ob.fetch_room_member_gifts_enrollment()
    return json.dumps(fetch)


@app.route('/user/room/gift/<user_id>/<room_id>/<gift_id>', methods=["POST"])
def user_room_gift(user_id,room_id,gift_id):
    ob = UserRoomFactoryOperations(user_id,room_id)
    try:
        ob.add_user_room_gift(gift_id)
        return json.dumps({"id": ob.fetch_user_room_last_gift(), "state": 'successful'})
    except:
        return json.dumps({"state": "error"})


@app.route('/user/room/gift/last/<user_id>/<room_id>', methods=["GET"])
def user_room_gift_last(user_id,room_id):
    ob = UserRoomOperations(user_id,room_id)
    fetch = ob.fetch_user_room_last_gift()
    return json.dumps(fetch)



'''
end API for USER and ROOM
'''




'''
API for STATIC
'''


@app.route("/users/names", methods=["GET"])
def users_names():
    ob = FactoryStaticOperations()
    return json.dumps(ob.fetch_all_users_names())

@app.route('/rooms/codes', methods=["GET"])
def rooms_codes():
    ob = FactoryStaticOperations()
    return json.dumps(ob.fetch_all_rooms_codes())


'''
end API for STATIC
'''
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True, port=7000)