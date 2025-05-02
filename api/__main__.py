import uvicorn

from api.api_config import config

if __name__ == "__main__":
    uvicorn.run(
        "api:app", host=str(config.host), port=config.port, reload=config.reload
    )
