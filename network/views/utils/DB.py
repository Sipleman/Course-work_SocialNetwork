from datetime import datetime, date, time

from bson import ObjectId
from pymongo import MongoClient


class DB(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.socnet_db
        ####
        self.user = None

    def set_current_user(self, user_id):
        self.user = self.db.users.find_one({"user_id": str(user_id)})

    def get_current_user(self):
        return self.user

    def get_user_path(self):
        return "/socnet/userpage/" + self.user["user_id"]

    def get_user_friend_object(self):
        return {"_id": self.user["_id"], "date": datetime.now()}

    def get_user_by_id(self, user_id):
        user = self.db.users.find_one({"user_id": str(user_id)})
        print user
        if user:
            user["user_path"] = "/socnet/userpage/" + str(user_id)
        return user

    def get_user_by_object_id(self, object_id):
        user = self.db.users.find_one({"_id": ObjectId(object_id)})
        if user:
            user["user_path"] = "/socnet/userpage/" + str(user["user_id"])
        return user

    def insert_new_user(self, registration_info):
        print registration_info
        if self.db.users.insert(registration_info):
            user_obj_id = self.get_user_by_id(registration_info["user_id"])["_id"]
            if self.db.messages.insert({"user_id": user_obj_id, "msgs": []}):
                if self.db.friend_lists.insert({"user_id": user_obj_id, "sent_requests": [], "requests": [], "friends": []}):
                    self.db.wall_records.insert({"user_id": user_obj_id, "wall": []})
                    return True
            return False

    def get_current_user_mail(self):
        # user_object = self.db.users.find_one({"user_id": str(user_id)})
        print self.user["_id"]
        msgs = self.db.messages.find_one({"user_id": self.user["_id"]})["msgs"]
        for msg in msgs:
            user_from = self.get_user_by_object_id(msg["sender"])
            msg["from"] = user_from["name"] + " " + user_from["lastname"]
            msg["user_path"] = user_from["user_path"]
        print msgs
        return msgs

    def send_message(self, receiver, content):
        # user_object_id = self.db.users.find_one({"user_id": str(user_id)})["_id"]
        receiver_object_id = self.db.users.find_one({"user_id": receiver})["_id"]
        msg = {
            "receiver": receiver_object_id,
            "content": content,
            "sender": self.user["_id"],
            "date": datetime.now()
        }
        return self.db.messages.update(
            {"user_id": receiver_object_id},
            {"$addToSet": {"msgs": msg}})

    def get_current_user_friends(self):
        friends_ids = self.db.friend_lists.find_one({"user_id": ObjectId(self.user["_id"])})["friends"]
        friend_list = []
        for friend_id in friends_ids:
            friend = self.db.users.find_one({"_id": ObjectId(friend_id["_id"])})
            friend["link"] = "/socnet/userpage/" + str(friend["user_id"])
            friend.pop("_id")
            friend_list.append(friend)
        return friend_list

    def get_current_user_requests(self):
        user_ids = self.db.friend_lists.find_one({"user_id": ObjectId(self.user["_id"])})["requests"]
        requests = []
        for user_id in user_ids:
            request = self.db.users.find_one({"_id": ObjectId(user_id)})
            request["link"] = "/socnet/userpage/" + str(request["user_id"])
            request.pop("_id")
            requests.append(request)

        return requests

    def send_friend_request(self, receiver_id):
        receiver_object_id = self.get_user_by_id(receiver_id)["_id"]
        user_request = {"receiver": receiver_object_id}
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.user["_id"])},
            {"$addToSet": {"sent_requests": user_request}}
        )
        self.db.friend_lists.update(
            {"user_id": ObjectId(receiver_object_id)},
            {"$addToSet": {"requests": ObjectId(self.user["_id"])}}
        )

    def get_current_user_sent_requests(self):
        requests = self.db.friend_lists.find_one({"_id": ObjectId(self.user["_id"])})["sent_requests"]
        return requests

    def accept_friend_request(self, friend_id):
        friend_object = {"_id": ObjectId(self.get_user_by_id(friend_id)["_id"]), "date": datetime.now()}
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.user["_id"])},
            {"$pull": {"requests": friend_object["_id"]}}
            )
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.user["_id"])},
            {"$addToSet": {"friends": friend_object}}
        )
        self.db.friend_lists.update(
            {"user_id": ObjectId(friend_object["_id"])},
            {"$addToSet": {"friends": self.get_user_friend_object()}}
        )

    def cancel_friend_request(self, friend_id):
        receiver = self.get_user_by_id(friend_id)["_id"]
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.user["_id"])},
            {"$pull": {"sent_requests": {"sender": ObjectId(receiver)}}}
        )
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.get_user_by_id(friend_id)["_id"])},
            {"$pull": {"requests": {"sender": ObjectId(receiver)}}},
        )

    def get_current_user_sent_msgs(self):
        msgs = list(self.db.messages.aggregate([
                    {"$match": {}},
                    {"$group": {"_id": "$msgs.sender", "content":  {"$first": "$msgs.content"}}},
                    {"$unwind": "$_id"},
                    {"$unwind": "$content"},
                    {"$match": {"_id": ObjectId(self.user["_id"])}}
                    ]))
        return msgs

    def is_friend(self, friend_id):
        friends_ids = self.db.friend_lists.find_one({"user_id": ObjectId(self.user["_id"])})["friends"]
        friend_object_id = self.get_user_by_id(friend_id)["_id"]
        for friend in friends_ids:
            if friend["_id"] == friend_object_id:
                return True

        return False

    def delete_friend(self, friend_id):
        friend_object_id = self.get_user_by_id(friend_id)["_id"]
        self.db.friend_lists.update(
            {"user_id": ObjectId(self.user["_id"])},
            {"$pull": {"friends": {"_id": ObjectId(friend_object_id)}}}
        )
        self.db.friend_lists.update(
            {"user_id": ObjectId(friend_object_id)},
            {"$pull": {"friends": {"_id": self.user["_id"]}}}
        )
        return True

    def get_user_wall_by_id(self, user_id):
        user_obj_id = self.get_user_by_id(user_id)["_id"]
        result = self.db.wall_records.find_one({"user_id": ObjectId(user_obj_id)})
        print result
        if result and "wall" in result:
            for record in result["wall"]:
                record["date"] = str(record["date"])
            return result["wall"]

        return {}

    def send_wall_msg(self, sender_obj_id, receiver_id, content):
        receiver = self.get_user_by_id(receiver_id)

        wall_record = {"sender": sender_obj_id, "receiver": receiver["_id"], "content": content["content"],
                       "id": content["_id"], "date": content["date"], "comments": [], "likes": 0}
        self.db.wall_records.update(
            {"user_id": ObjectId(receiver["_id"])},
            {"$addToSet": {"wall": wall_record}}
        )

    def increase_like(self, user_id, post_id):
        user_obj_id = self.get_user_by_id(user_id)["_id"]

    def insert_new_comment(self, response_data):
        user_obj_id = self.get_user_by_id(response_data["receiver"])
