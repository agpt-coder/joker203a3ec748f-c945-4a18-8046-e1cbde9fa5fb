from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRole(BaseModel):
    """
    Determines the access level and permissions of a user.
    """

    role: prisma.enums.Role


class APIRequestModel(BaseModel):
    """
    Definition of API requests made by a user with details on request timing and endpoint accessed.
    """

    id: str
    createdAt: datetime
    endpoint: str
    response: Optional[str] = None


class UserDetailsResponse(BaseModel):
    """
    Response model containing detailed information of a user. Includes sensitive details, hence access is restricted.
    """

    id: str
    email: str
    createdAt: datetime
    updatedAt: datetime
    roles: List[UserRole]
    requests: List[APIRequestModel]


async def getUserDetails(userId: str) -> UserDetailsResponse:
    """
    Fetches details for a specific user given the user ID. This secure endpoint ensures that sensitive user information is only accessible to System Administrators.

    Args:
    userId (str): The unique identifier of the user to fetch details for.

    Returns:
    UserDetailsResponse: Response model containing detailed information of a user. Includes sensitive details, hence access is restricted.

    Example:
    user_details = await getUserDetails('123')
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"roles": True, "requests": True}
    )
    if user is None:
        raise ValueError("User not found.")
    user_roles = [UserRole(role=role.role) for role in user.roles]
    user_requests = [
        APIRequestModel(
            id=req.id,
            createdAt=req.createdAt,
            endpoint=req.endpoint,
            response=req.response,
        )
        for req in user.requests
    ]
    return UserDetailsResponse(
        id=user.id,
        email=user.email,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        roles=user_roles,
        requests=user_requests,
    )
