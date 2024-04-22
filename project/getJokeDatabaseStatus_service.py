from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class JokeStatusRequest(BaseModel):
    """
    No specific input required other than authentication which is handled separately. But since this endpoint requires very specific user roles, those roles will be validated upon processing the request.
    """

    pass


class JokeStatusResponse(BaseModel):
    """
    Provides an overview of the joke database's current status, including count of jokes and the last updated timestamp.
    """

    last_update: datetime
    total_jokes: int


async def getJokeDatabaseStatus(request: JokeStatusRequest) -> JokeStatusResponse:
    """
    Provides a status report on the joke database, including the last update time and the total number of jokes available. Useful for database managers and system administrators to monitor and manage the database effectively. This is a protected endpoint, needing authentication for access.

    Args:
        request (JokeStatusRequest): No specific input required other than authentication which is handled separately. But since this endpoint requires very specific user roles, those roles will be validated upon processing the request.

    Returns:
        JokeStatusResponse: Provides an overview of the joke database's current status, including count of jokes and the last updated timestamp.

    Example:
        request = JokeStatusRequest()
        response = await getJokeDatabaseStatus(request)
        print(response.last_update, response.total_jokes)
    """
    latest_joke = await prisma.models.Joke.prisma().find_first(
        order={"createdAt": "desc"}
    )
    total_jokes = await prisma.models.Joke.prisma().count()
    return JokeStatusResponse(
        last_update=latest_joke.createdAt, total_jokes=total_jokes
    )
