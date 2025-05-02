from fastapi import FastAPI

from library.index import Index, get_index

app = FastAPI()


@app.get("/", response_model_exclude_none=True)
def index() -> Index:
    return get_index()
