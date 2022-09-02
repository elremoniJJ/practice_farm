#import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

#create app instance from FastAPI class
app = FastAPI()

from app.database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo
)


origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from app.model import ToDo

#import HTMLSession
from requests_html import HTMLSession

#create class for Scraper, using Quotes.toscrape.com
class Scraper():

    def scrapedata(self, tag):
        url = f"https://quotes.toscrape.com/tag/{tag}"
        s = HTMLSession()
        r = s.get(url)

        print(f"r = {r}")

        qlist = []

        quotes = r.html.find('div.quote')

        for q in quotes:
            item = {
                'text': q.find('span.text', first=True).text.strip(),
                'author': q.find('small.author', first=True).text.strip()
            }
            qlist.append(item)

        return qlist

#create variable containing Scraper class
quotes = Scraper()


@app.get("/quotes/{cat}", tags=['Scrape Quotes'])
async def read_item(cat):
    return quotes.scrapedata(cat)



@app.get("/", tags=['Root'])
async def root() -> dict:
    return {"Ping":"Pong"}

# get -- read all
@app.get("/api/todo", tags=['Todos'])
async def get_todo() -> dict:
    response = await fetch_all_todos()
    return response

# get -- read one
@app.get("/api/todo{title}", response_model=ToDo, tags=['Todos'])
async def get_todo_by_id(title) -> dict:
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"No todo item with title: {title}")


# post -- create
@app.post("/api/todo", response_model=ToDo, tags=['Todos'])
async def post_todo(todo:ToDo) -> dict:
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


# put -- update
@app.put("/api/todo{title}", response_model=ToDo, tags=["Todos"])
async def put_todo(title:str, description:str) -> dict:
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(404, f"No todo item with title: {title}")

# delete -- delete
@app.delete("/api/todo{title}", tags=["Todos"])
async def delete_todo(title:str) -> dict:
    response = await remove_todo(title)
    if response:
        return f"Successfully deleted {title}"
    raise HTTPException(404, f"No todo item with title: {title}")
