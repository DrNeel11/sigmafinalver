from pymongo import MongoClient

client=MongoClient("mongodb+srv://neel11:Neelpavi1234@cluster0.yxm11.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.users
collection=db.user_collection