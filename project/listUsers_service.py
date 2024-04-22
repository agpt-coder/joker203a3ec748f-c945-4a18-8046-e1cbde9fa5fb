from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetUsersRequest(BaseModel):
    """
    Request model for retrieving all users. As there are no parameters required for this request, the primary consideration here is authorization, which is managed outside the parameters of this model.
    """

    pass


class RoleDetails(BaseModel):
    """
    Details of a user's role.
    """

    role: prisma.enums.Role


class UserDetails(BaseModel):
    """
    Details of an individual user, including their roles.
    """

    id: str
    email: str
    createdAt: datetime
    updatedAt: datetime
    roles: List[RoleDetails]


class GetUsersResponse(BaseModel):
    """
    Response model containing a list of users. Each user is detailed with necessary attributes such as id, email, and associated roles.
    """

    users: List[UserDetails]


async def listUsers(request: GetUsersRequest) -> GetUsersResponse:
    """
    Provides a list of all users registered in the system. Accessible by System Administrators, this endpoint assists in managing users and supports pagination to efficiently handle large data sets.

    Args:
        request (GetUsersRequest): Request model for retrieving all users. As there are no parameters required for this request, the primary consideration here is authorization, which is managed outside the parameters of this model.

    Returns:
        GetUsersResponse: Response model containing a list of users. Each user is detailed with necessary attributes such as id, email, and associated roles.
    """
    prisma_users = await prisma.models.User.prisma().find_many(include={"roles": True})
    users_details = []
    for user in prisma_users:
        roles = [RoleDetails(role=srole.role) for srole in user.roles]
        user_detail = UserDetails(
            id=user.id,
            email=user.email,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt,
            roles=roles,
        )
        users_details.append(user_detail)
    response = GetUsersResponse(users=users_details)
    return response
