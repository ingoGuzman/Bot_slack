import pymongo


#Setters/ pytest checkers
def get_database_name():
	return "nestor"

def get_mongo_host():
	return "localhost"

def get_mongo_port():
	return 27017


#Database connection
def connect_database():
	myclient = pymongo.MongoClient(host=get_mongo_host(), port=get_mongo_port())
	db = myclient[get_database_name()]

	return db

#Database write
def db_write(message, database_name, collection_name):
	database = connect_database()
	my_doc = {"message" : message}
	print("Writing a new document in the database:"+str(my_doc))
	database[collection_name].insert_one(my_doc)
