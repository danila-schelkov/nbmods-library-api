import uvicorn

from api.api_config import api_config

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=str(api_config.host),
        port=api_config.port,
        reload=api_config.reload,
    )
