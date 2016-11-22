from pymongo import MongoClient


class DB(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.socnet_db

    def get_user_by_id(self, usr_id):
        return self.db.users.find_one({"user_id": usr_id})

    def insert_new_user(self, registration_info):
        print registration_info
        if self.db.users.insert(registration_info):
            if self.db.messages.insert({"user_id": registration_info["user_id"], "msgs": []}):
                return True
            return False

    def get_user_mail(self, user_id):
        user_object_id = self.db.users.find_one({"user_id": user_id})["_id"]
        msgs = self.db.messages.find_one({"user_id": user_object_id})["msgs"]
        return msgs
