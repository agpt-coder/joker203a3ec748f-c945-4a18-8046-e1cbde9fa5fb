import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model indicating the outcome of the delete operation. It will primarily communicate the success or any errors.
    """

    success: bool
    message: str


async def deleteUser(userId: str, confirmation: bool) -> DeleteUserResponse:
    """
    Deletes a user from the system using the user ID. This action is irreversible and strictly limited to System Administrators to maintain data integrity and security.

    Args:
        userId (str): The unique identifier for the user to be deleted.
        confirmation (bool): A confirmation flag to prevent accidental deletions. It must be True to proceed with the deletion.

    Returns:
        DeleteUserResponse: A response model indicating the outcome of the delete operation. It will primarily communicate the success or any errors.

    Example:
        # Sample function call
        response = await deleteUser("d3f02834-f830-4c6b-83d0-2d5d6bc24544", True)
        print(response)
    """
    if not confirmation:
        return DeleteUserResponse(success=False, message="Deletion not confirmed.")
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return DeleteUserResponse(success=False, message="User not found.")
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponse(success=True, message="User successfully deleted.")
