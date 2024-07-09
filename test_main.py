import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import main
from src.db.crud import retrieve_people, retrieve_posts
from src.schemas import Comment, People, Post

# ruff: noqa: S311, S101, PLR2004, PERF203

client = TestClient(app=main.app)


## because I'm only testing get endpoints,
## I did not use a mock db
def test_get_people() -> None:
	"""Test of /people endpoint"""
	response = client.get("/people")
	assert response.status_code == 200
	for person in response.json():
		try:
			People(**person)
		except ValidationError as e:
			pytest.fail("Validation error at /people", e)


def test_get_comments() -> None:
	"""Test of /comments endpoint"""
	response = client.get("/comments")
	assert response.status_code == 200
	for comment in response.json():
		try:
			Comment(**comment)
		except ValidationError as e:
			pytest.fail("Validation error at /comments", e)


def test_get_posts() -> None:
	"""Test of /posts endpoint"""
	response = client.get("/posts")
	assert response.status_code == 200
	for posts in response.json():
		try:
			Post(**posts)
		except ValidationError as e:
			pytest.fail("Validation error at /posts", e)


@pytest.mark.asyncio()
async def test_comments_of_post() -> None:
	"""Test of /{post_id}/comments endpoint"""
	posts = await retrieve_posts()
	post_id = posts[0]["_id"]
	response = client.get(f"/{post_id}/comments")
	assert response.status_code == 200
	for comment in response.json():
		try:
			Comment(**comment)
		except ValidationError as e:
			pytest.fail("Validation error at /{post_id}/comments", e)


@pytest.mark.asyncio()
async def test_posts_of_person() -> None:
	"""Test of /{person_id}/posts endpoint"""
	people = await retrieve_people()
	person_id = people[0]["_id"]
	response = client.get(f"/{person_id}/posts")
	assert response.status_code == 200
	for posts in response.json():
		try:
			Post(**posts)
		except ValidationError as e:
			pytest.fail("Validation error at /{person_id}/posts", e)
