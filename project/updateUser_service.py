from typing import Any, Dict, List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRole(BaseModel):
    """
    Determines the access level and permissions of a user.
    """

    role: prisma.enums.Role


class UpdateUserResponse(BaseModel):
    """
    Confirmation of successful update along with the updated user details.
    """

    success: bool
    userId: str
    updatedFields: Dict[str, Any]


async def updateUser(
    userId: str, email: Optional[str], roles: List[UserRole]
) -> UpdateUserResponse:
    """
    Updates a user's details based on the provided user ID. Requires JSON input with updateable
    user attributes and can be used only by System Administrators to manage user information.

    Args:
        userId (str): The unique identifier for the user to be updated.
        email (Optional[str]): If provided, the new email address for the user.
        roles (List[UserRole]): List of UserRole instances representing the updated roles for the user.

    Returns:
        UpdateUserResponse: Contains success status, user ID, and a dictionary of fields that were updated.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"roles": True}
    )
    if not user:
        return UpdateUserResponse(success=False, userId=userId, updatedFields={})
    update_data = {"email": email} if email else {}
    updated_roles_data = []
    if roles:
        await prisma.models.UserRole.prisma().delete_many(where={"userId": userId})
        for role in roles:
            new_role = await prisma.models.UserRole.prisma().create(
                data={"role": role.role, "userId": userId}
            )
            updated_roles_data.append({"role": new_role.role, "roleId": new_role.id})
    if email:
        await prisma.models.User.prisma().update(
            where={"id": userId}, data={"email": email}
        )
        update_data["email"] = email
    return UpdateUserResponse(
        success=True,
        userId=userId,
        updatedFields={"email": email, "roles": updated_roles_data},
    )
