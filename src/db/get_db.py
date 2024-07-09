import os

from motor.motor_asyncio import AsyncIOMotorClient


def get_db() -> AsyncIOMotorClient:
	"""Get the database client.

	Returns
		MongoClient: The database client.
	"""
	client = AsyncIOMotorClient(host=os.environ.get("DB_HOST", "localhost"), port=27017)
	return client["turbit-t1"]
