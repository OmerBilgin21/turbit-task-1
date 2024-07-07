from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.schemas import Comment, People, Post

from .get_db import get_db

PEOPLE_COLLECTION_NAME = "people"
COMMENTS_COLLECTION_NAME = "comments"
POSTS_COLLECTION_NAME = "posts"


async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
	"""Get the database collection.

	Args:
		collection_name (str): The name of the collection.

	Returns:
		AsyncIOMotorCollection: The collection.
	"""
	db = get_db()
	return db[collection_name]


async def retrieve_people() -> list[People]:
	"""Fetches people from db and returns it

	Returns:
		list[People]: List of people
	"""
	peoplec = await get_collection(PEOPLE_COLLECTION_NAME)
	return await peoplec.find({}).to_list(length=None)


async def retrieve_comments() -> list[Comment]:
	"""Fetches comments from the db and returns it

	Returns:
		list[Comment]: List of comments
	"""
	commentc = await get_collection(COMMENTS_COLLECTION_NAME)
	return await commentc.find({}).to_list(length=None)


async def retrieve_posts() -> list[Post]:
	"""Fetches posts from the db and returns it

	Returns:
		list[Post]: List of posts
	"""
	postsc = await get_collection(POSTS_COLLECTION_NAME)
	return await postsc.find({}).to_list(length=None)


async def retrieve_comments_of_post(post_id: ObjectId) -> list[Comment]:
	"""Retrieve the comments that belongs to a certain post

	Args:
		post_id (ObjectId): id of post

	Returns:
		list[Comment]: List of comments
	"""
	commentsc = await get_collection(COMMENTS_COLLECTION_NAME)
	return await commentsc.find({"postId": post_id}).to_list(length=None)


async def retrieve_posts_of_user(person_id: ObjectId) -> list[Post]:
	"""Retrieve the posts that belongs to a certain person

	Args:
		person_id (ObjectId): id of person

	Returns:
		list[Post]: List of posts
	"""
	postsc = await get_collection(POSTS_COLLECTION_NAME)
	return await postsc.find({"userId": person_id}).to_list(length=None)
