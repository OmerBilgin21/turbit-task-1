from .oid import Oid
from .out import Out


class Comment(Out):
	name: str
	email: str
	body: str
	postId: Oid
