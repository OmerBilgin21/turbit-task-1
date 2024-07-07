# ruff: noqa: ERA001, F841
import asyncio

import aiohttp

from src.db.get_db import get_db

# schemas
from src.schemas import People


async def fetch_people() -> list[People]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[People | None]: List of people
	"""
	async with (
		aiohttp.ClientSession() as session,
		session.get(
			"https://jsonplaceholder.typicode.com/users",
			timeout=10,
		) as response,
	):
		return await response.json()


async def fetch_posts() -> list[People]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[People | None]: List of people
	"""
	async with (
		aiohttp.ClientSession() as session,
		session.get(
			"https://jsonplaceholder.typicode.com/posts",
			timeout=10,
		) as response,
	):
		return await response.json()


async def fetch_comments() -> list[People]:
	"""Fetches data from JSONPlaceholder and returns it

	Returns:
		list[People | None]: List of people
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

	if people_data is not None and len(people_data) > 0:
		pass
		# for person in people_data:
		# del person["id"]
		# await peoplec.insert_many(people_data)

	if posts_data is not None and len(posts_data) > 0:
		# I inserted the posts after people because
		# I wanted to use the ObjectId from bson instead of a float for userId
		# So I found the related person from the db and
		# inserted that user's id as the userId
		for post in posts_data:
			owner_email = next(
				(
					person["email"]
					for person in people_data
					if person["id"] == post["userId"]
				),
				None,
			)
			person_from_db = await peoplec.find_one({"email": owner_email})
			del post["userId"]
			del post["id"]
			post["userId"] = person_from_db["_id"]
		# await postsc.insert_many(posts_data)

	if comments_data is not None and len(comments_data) > 0:
		# I inserted the comments after posts because
		# I wanted to use the ObjectId from bson instead of a float for postId
		# So I found the related post from the db and
		# inserted that post's id as the postId
		for comment in comments_data:
			owner_post_title = next(
				(
					post["title"]
					for post in posts_data
					if post["id"] == comment["postId"]
				),
				None,
			)
			post_from_db = await postsc.find_one({"title": owner_post_title})
			comment["postId"] = post_from_db["_id"]
			del comment["id"]
		# await commentsc.insert_many(comments_data)


asyncio.run(insert_to_db())
