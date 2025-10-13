from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Stay Frosty Soldier"}

@app.post("/new-post")
def createNewPost(body: dict = Body()):
    print(body)
    return{"New Post:": f"title {body['title']} content {body['content']}"  }
