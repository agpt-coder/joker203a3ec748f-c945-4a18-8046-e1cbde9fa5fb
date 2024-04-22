from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class RandomJokeRequest(BaseModel):
    """
    This request model is used for retrieving a random joke. It's a simple GET request without any parameters, reflecting the accessibility and simplicity of this public endpoint.
    """

    pass


class RandomJokeResponse(BaseModel):
    """
    The model for the response when fetching a random joke. It returns a joke in JSON format that includes the content of the joke.
    """

    joke_content: str
    source: Optional[str] = None


async def fetchRandomJoke(request: RandomJokeRequest) -> RandomJokeResponse:
    """
    This endpoint retrieves a random joke from an external joke service or the database. It uses a GET request to ensure simplicity and accessibility. The response is expected to be a JSON object containing the joke text. This endpoint is publicly accessible, allowing any API user to request a random joke without authentication.

    Args:
        request (RandomJokeRequest): This request model is used for retrieving a random joke. It's a simple GET request without any parameters, reflecting the accessibility and simplicity of this public endpoint.

    Returns:
        RandomJokeResponse: The model for the response when fetching a random joke. It returns a joke in JSON format that includes the content of the joke.
    """
    async with httpx.AsyncClient() as client:
        joke_sources = await prisma.models.JokeSource.prisma().find_many()
        if joke_sources:
            for source in joke_sources:
                try:
                    response = await client.get(source.endpoint)
                    response.raise_for_status()
                    joke_content = response.json()["joke"]
                    return RandomJokeResponse(
                        joke_content=joke_content, source=source.name
                    )
                except (httpx.RequestError, httpx.HTTPStatusError, KeyError):
                    continue
    joke_record = await prisma.models.Joke.prisma().find_first()
    if joke_record:
        return RandomJokeResponse(
            joke_content=joke_record.content, source=joke_record.source
        )
    else:
        raise Exception("No available jokes in external sources or local database.")
