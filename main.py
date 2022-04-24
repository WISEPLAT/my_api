# pip install flask-restful
# http://127.0.0.1:5000/hi http://127.0.0.1:5000/hi/ http://127.0.0.1:5000/hi/2
# to test:
# curl -X PUT -d "{\"text\":\"val text dksh\", \"lang\":\"oo\"}" -H "Content-Type: application/json" http://127.0.0.1:5000/hi/5
# in windows please use double quotes!!! and slash

from flask import Flask
from flask_restful import Api, Resource, reqparse
import random

my_list = [
    {
        "id": 1,
        "text": "Привет Мир!",
        "lang": "ru"
    },
    {
        "id": 2,
        "text": "你好世界!",
        "lang": "ch"
    },
    {
        "id": 3,
        "text": "Hello World!",
        "lang": "en"
    },
    {
        "id": 4,
        "text": "Hallo Welt!",
        "lang": "de"
    },
]


class HiResource(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(my_list), 200
        for val in my_list:
            if (val["id"] == id):
                return val, 200
        return "Warning! Can't find text! ))", 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("lang")
        params = parser.parse_args()
        print(params)
        for val in my_list:
            if (id == val["id"]):
                val["text"] = params["text"]
                val["lang"] = params["lang"]
                return val, 200
        val = {
            "id": id,
            "text": params["text"],
            "lang": params["lang"]
        }
        my_list.append(val)
        return val, 201

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("lang")
        params = parser.parse_args()
        for val in my_list:
            if (id == val["id"]):
                return f"This text with id={id} already exists", 400
        val = {
            "id": id,
            "text": params["text"],
            "lang": params["lang"]
        }
        my_list.append(val)
        return val, 201

    def delete(self, id):
        global my_list
        my_list = [val for val in my_list if val["id"] != id]
        return f"Record with id={id} was deleted!", 200


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(HiResource, "/hi", "/hi/", "/hi/<int:id>")
    app.run(debug=True)
