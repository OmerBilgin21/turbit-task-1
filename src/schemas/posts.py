from .oid import Oid
from .out import Out


class Post(Out):
	title: str
	body: str
	userId: Oid
