from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routers.blog import router as blog_router
from routers.users import router as user_router
import csv
app = FastAPI()
templates = Jinja2Templates(directory="templates")



app.include_router(blog_router, prefix="/blog", tags=["Blog Posts"])
app.include_router(user_router, prefix="/user", tags=["User"])




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
    

@app.get("/home")
def home():
    return read_posts



@app.get("/about")
def about():
    return {"About the Damola Johnson Blog"}

@app.post("/contact")
def contact():
    return {"Contact Us"}