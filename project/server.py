import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import prisma
import prisma.enums
import project.createUser_service
import project.deleteUser_service
import project.fetchRandomJoke_service
import project.getJokeDatabaseStatus_service
import project.getUserDetails_service
import project.listUsers_service
import project.updateJokeServiceSettings_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joker203",
    lifespan=lifespan,
    description="create a single api that returns one random joke using litellm",
)


@app.get(
    "/jokes/random", response_model=project.fetchRandomJoke_service.RandomJokeResponse
)
async def api_get_fetchRandomJoke(
    request: project.fetchRandomJoke_service.RandomJokeRequest,
) -> project.fetchRandomJoke_service.RandomJokeResponse | Response:
    """
    This endpoint retrieves a random joke from an external joke service or the database. It uses a GET request to ensure simplicity and accessibility. The response is expected to be a JSON object containing the joke text. This endpoint is publicly accessible, allowing any API user to request a random joke without authentication.
    """
    try:
        res = await project.fetchRandomJoke_service.fetchRandomJoke(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    roles: List[prisma.enums.Role], username: str, email: str
) -> project.createUser_service.CreateUserResponse | Response:
    """
    Creates a new user record in the system database. This endpoint is protected to ensure only authorized administrators manage user access.
    """
    try:
        res = await project.createUser_service.createUser(roles, username, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str, confirmation: bool
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a user from the system using the user ID. This action is irreversible and strictly limited to System Administrators to maintain data integrity and security.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId, confirmation)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/admin/jokes/settings",
    response_model=project.updateJokeServiceSettings_service.UpdateJokeSettingsResponse,
)
async def api_post_updateJokeServiceSettings(
    apiKey: Optional[str], serviceUrl: Optional[str]
) -> project.updateJokeServiceSettings_service.UpdateJokeSettingsResponse | Response:
    """
    Allows system administrators to update settings related to the external joke service or database configurations. The endpoint expects JSON payload with settings options and returns a success or error message upon execution. This operations is protected and requires administrator authentication.
    """
    try:
        res = await project.updateJokeServiceSettings_service.updateJokeServiceSettings(
            apiKey, serviceUrl
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    request: project.listUsers_service.GetUsersRequest,
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Provides a list of all users registered in the system. Accessible by System Administrators, this endpoint assists in managing users and supports pagination to efficiently handle large data sets.
    """
    try:
        res = await project.listUsers_service.listUsers(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/admin/jokes/status",
    response_model=project.getJokeDatabaseStatus_service.JokeStatusResponse,
)
async def api_get_getJokeDatabaseStatus(
    request: project.getJokeDatabaseStatus_service.JokeStatusRequest,
) -> project.getJokeDatabaseStatus_service.JokeStatusResponse | Response:
    """
    Provides a status report on the joke database, including the last update time and the total number of jokes available. Useful for database managers and system administrators to monitor and manage the database effectively. This is a protected endpoint, needing authentication for access.
    """
    try:
        res = await project.getJokeDatabaseStatus_service.getJokeDatabaseStatus(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}", response_model=project.getUserDetails_service.UserDetailsResponse
)
async def api_get_getUserDetails(
    userId: str,
) -> project.getUserDetails_service.UserDetailsResponse | Response:
    """
    Fetches details for a specific user given the user ID. This secure endpoint ensures that sensitive user information is only accessible to System Administrators.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: str, email: Optional[str], roles: List[project.updateUser_service.UserRole]
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates a user's details based on the provided user ID. Requires JSON input with updateable user attributes and can be used only by System Administrators to manage user information.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, roles)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
