from fastapi import FastAPI

from api.api_config import config
from api.routes.index_route import api

app = FastAPI()

app.mount(config.root_path, api)
