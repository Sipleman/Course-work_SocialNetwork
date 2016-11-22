from datetime import datetime, date, time

from bson import ObjectId
from pymongo import MongoClient


class DB(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.socnet_db

    def get_user_by_id(self, usr_id):
        return self.db.users.find_one({"user_id": usr_id})

    def get_user_info_by_object_id(self, object_id):
        user = self.db.users.find_one({"_id": ObjectId(object_id)})
        return user["name"] + user["lastname"]

    def insert_new_user(self, registration_info):
        print registration_info
        if self.db.users.insert(registration_info):
            if self.db.messages.insert({"user_id": registration_info["user_id"], "msgs": []}):
                return True
            return False

    def get_user_mail(self, user_id):
        user_object = self.db.users.find_one({"user_id": str(user_id)})
        msgs = self.db.messages.find_one({"user_id": user_object["_id"]})["msgs"]
        for msg in msgs:
            msg["from"] = self.get_user_info_by_object_id(msg["sender"])
        print msgs
        return msgs

    def send_message(self, receiver, content, user_id):
        user_object_id = self.db.users.find_one({"user_id": str(user_id)})["_id"]
        receiver_object_id = self.db.users.find_one({"user_id": receiver})["_id"]
        msg = {
            "receiver": receiver,
            "content": content,
            "sender": user_object_id,
            "date": datetime.now()
        }
        return self.db.messages.update(
            {"user_id": receiver_object_id},
            {"$addToSet": {"msgs": msg}})
