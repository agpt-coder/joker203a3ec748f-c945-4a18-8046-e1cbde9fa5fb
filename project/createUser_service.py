from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    This model represents the response after creating a new user in the system. It provides confirmation of the created record with minimal user data.
    """

    id: str
    username: str
    email: str
    roles: List[prisma.enums.Role]


async def createUser(
    username: str, email: str, roles: List[prisma.enums.Role]
) -> CreateUserResponse:
    """
    Creates a new user record in the system database. This endpoint is protected to ensure only authorized administrators manage user access.

    Args:
        username (str): The username for the new user.
        email (str): The email address for the new user, must be unique.
        roles (List[prisma.enums.Role]): A list of roles assigned to the user, must be a subset of existing roles defined in the system.

    Returns:
        CreateUserResponse: This model represents the response after creating a new user in the system. It provides confirmation of the created record with minimal user data.
    """
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "roles": {"create": [{"role": role} for role in roles]}},
        include={"roles": True},
    )
    return CreateUserResponse(
        id=new_user.id,
        username=username,
        email=new_user.email,
        roles=[ur.role for ur in new_user.roles],
    )
