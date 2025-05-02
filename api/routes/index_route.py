from fastapi import FastAPI

from library.index import Index, get_index

api = FastAPI()


@api.get("/index.json", response_model_exclude_none=True)
def index() -> Index:
    return get_index()
