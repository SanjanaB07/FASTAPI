from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    bio: str


class CategoryCreate(BaseModel):
    name: str


class BookCreate(BaseModel):
    title: str
    isbn: str
    year: int
    author_id: int
    category_id: int
