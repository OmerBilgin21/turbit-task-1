import asyncio
import os

import aiohttp
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


def get_db() -> AsyncIOMotorClient:
	"""Get the database client.

	Returns
		MongoClient: The database client.
	"""
	client = AsyncIOMotorClient(host=os.environ.get("DB_HOST", "localhost"), port=27017)
	return client["turbit-t1"]


async def fetch_people() -> list[dict]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[dict | None]: List of people
	"""
	async with (
		aiohttp.ClientSession() as session,
		session.get(
			"https://jsonplaceholder.typicode.com/users",
			timeout=10,
		) as response,
	):
		return await response.json()


async def fetch_posts() -> list[dict]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[dict | None]: List of posts
	"""
	async with (
		aiohttp.ClientSession() as session,
		session.get(
			"https://jsonplaceholder.typicode.com/posts",
			timeout=10,
		) as response,
	):
		return await response.json()


async def fetch_comments() -> list[dict]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[dict | None]: List of comments
	"""
	async with (
		aiohttp.ClientSession() as session,
		session.get(
			"https://jsonplaceholder.typicode.com/comments",
			timeout=10,
		) as response,
	):
		return await response.json()


async def insert_to_db() -> None:
	"""Inserts retrieved data to Mongo"""
	db = get_db()
	peoplec = db["people"]
	commentsc = db["comments"]
	postsc = db["posts"]

	posts_data = await fetch_posts()
	people_data = await fetch_people()
	comments_data = await fetch_comments()

	if (
		not isinstance(people_data, list)
		or not isinstance(posts_data, list)
		or not isinstance(comments_data, list)
	):
		print("Something went wrong.")  # noqa: T201
		return

	for person in people_data:
		person["_id"] = ObjectId()

	for post in posts_data:
		# find the owner of the post to be able to
		# relate them correctly with ObjectId
		owner_id = next(
			(person["_id"] for person in people_data if person["id"] == post["userId"]),
			None,
		)
		post["_id"] = ObjectId()
		# replace userId from a float to ObjectId
		post["userId"] = owner_id

	# same as posts/people relationship replace float postId with ObjectId ones
	for comment in comments_data:
		owner_post_id = next(
			(post["_id"] for post in posts_data if post["id"] == comment["postId"]),
			None,
		)
		comment["postId"] = owner_post_id

	# clear float ids from JSONPlaceholder after doing the matching with ObjectIds
	def remove_id(data_list: list[dict]) -> None:
		for item in data_list:
			item.pop("id", None)

	remove_id(people_data)
	remove_id(posts_data)
	remove_id(comments_data)
	await peoplec.insert_many(people_data)
	await postsc.insert_many(posts_data)
	await commentsc.insert_many(comments_data)


asyncio.run(insert_to_db())
