import os

import uvicorn
from bson import ObjectId
from fastapi import FastAPI, HTTPException

from src.db.crud import (
	retrieve_comments,
	retrieve_comments_of_post,
	retrieve_people,
	retrieve_posts,
	retrieve_posts_of_user,
)
from src.schemas import Comment, People, Post

app = FastAPI()


@app.get("/people")
async def get_people() -> list[People]:
	"""Returns the people in the database

	Returns:
		list[People]: List of people
	"""
	return await retrieve_people()


@app.get("/comments")
async def get_comments() -> list[Comment]:
	"""Returns the comments in the database

	Returns:
		list[Comment]: List of comments
	"""
	return await retrieve_comments()


@app.get("/posts")
async def get_posts() -> list[Post]:
	"""Returns the posts in the database

	Returns:
		list[Post]: List of posts
	"""
	return await retrieve_posts()


@app.get("/{post_id}/comments")
async def comments_of_post(
	post_id: str,
) -> list[Comment] | None:
	"""Returns the comments that belongs to a certain post

	Args:
		post_id (str): id of post

	Raises:
		HTTPException: 400 if given id is not valid

	Returns:
		list[Comment] | None: Comments of a post if any.
	"""
	if not ObjectId.is_valid(post_id):
		raise HTTPException(
			status_code=400,
			detail="Invalid bson ObjectId",
		)
	return await retrieve_comments_of_post(post_id=ObjectId(post_id))


@app.get("/{person_id}/posts")
async def posts_of_person(
	person_id: str,
) -> list[Post] | None:
	"""Returns the posts that belongs to a certain person

	Args:
		person_id (str): id of person

	Raises:
		HTTPException: 400 if given id is not valid

	Returns:
		list[Post] | None: Posts of a person if any.
	"""
	if not ObjectId.is_valid(person_id):
		raise HTTPException(
			status_code=400,
			detail="Invalid bson ObjectId",
		)
	return await retrieve_posts_of_user(person_id=ObjectId(person_id))


if __name__ == "__main__":
	env = os.environ.get("ENV", "dev")
	if env == "dev":
		uvicorn.run(
			"main:app",
			host="0.0.0.0",
			port=8000,
			reload=True,
			log_level="info",
		)
	else:
		uvicorn.run(
			"main:app",
			host="0.0.0.0",
			port=8000,
			log_level="info",
		)
