from fastapi import FastAPI

app = FastAPI()


@app.get('/healthcheck')
def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint.

    Returns:
        A dictionary containing the application's health status.
    """
    return {'status': 'ok'}
