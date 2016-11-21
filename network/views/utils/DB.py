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
            return True