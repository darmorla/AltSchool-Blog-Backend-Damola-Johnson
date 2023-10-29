from fastapi import APIRouter, Form, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel, validator
import csv
import uuid
from auth import oauth2_scheme



router = APIRouter()

class BlogPost(BaseModel):
    id: str
    title: str
    author: str
    content: str

class BlogUpdate(BaseModel):
    title: str
    content: str

    @validator('content')
    def content_must_be_short(cls, v):
        if len(v.split()) > 200:
            raise ValueError('Content cannot exceed 200 words')
        return v

def read_posts():
    try:
        with open("blog.csv", 'r') as file:
            reader = csv.DictReader(file)
            posts = []
            for row in reader:
                posts.append(row)
            return posts
    except FileNotFoundError:
        return []

def write_posts(posts):
    with open("blog.csv", 'w', newline='') as file:
        fieldnames = ["id", "title", "author", "content"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)

@router.get("/posts/")
def read_posts_view():
    return read_posts()

@router.post("/posts/create")
def create_post(
    title: Annotated[str, Form()],
    author: Annotated[str, Form()],
    content: Annotated[str, Form()],
    current_user: str = Depends(oauth2_scheme)
):
    posts = read_posts()
    new_id = str(uuid.uuid4())
    new_post = BlogPost(id=new_id, title=title, author=author, content=content)
    posts.append(new_post.dict())
    write_posts(posts)
    return new_post

@router.put("/posts/{post_id}")
async def update_post(post_id: str, post: BlogUpdate, current_user: str = Depends(oauth2_scheme)):
    posts = read_posts()
    for idx, p in enumerate(posts):
        if p['id'] == post_id:
            posts[idx] = post.dict()
            write_posts(posts)
            return {"message": "Post updated successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/posts/delete{post_id}")
async def delete_post(post_id: str, current_user: str = Depends(oauth2_scheme)):
    posts = read_posts()
    for idx, p in enumerate(posts):
        if p['id'] == post_id:
            del posts[idx]
            write_posts(posts)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")