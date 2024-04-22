from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateJokeSettingsResponse(BaseModel):
    """
    Response model for updating joke settings indicating success or failure.
    """

    success: bool
    message: str


async def updateJokeServiceSettings(
    apiKey: Optional[str], serviceUrl: Optional[str]
) -> UpdateJokeSettingsResponse:
    """
    Allows system administrators to update settings related to the external joke service.
    The function attempts to update the joke service settings in the database and returns a response model indicating success or failure.

    Args:
        apiKey (Optional[str]): API key for external joke service.
        serviceUrl (Optional[str]): Base URL for the external joke service.

    Returns:
        UpdateJokeSettingsResponse: Response model for updating joke settings indicating success or failure.
    """
    try:
        joke_sources = await prisma.models.JokeSource.prisma().find_many()
        if joke_sources:
            joke_source = joke_sources[0]
            update_data = {}
            if apiKey is not None:
                update_data["apiKey"] = apiKey
            if serviceUrl is not None:
                update_data["endpoint"] = serviceUrl
            await prisma.models.JokeSource.prisma().update(
                where={"id": joke_source.id}, data=update_data
            )
            return UpdateJokeSettingsResponse(
                success=True, message="Joke service settings updated successfully."
            )
        else:
            return UpdateJokeSettingsResponse(
                success=False, message="No joke source found to update."
            )
    except Exception as e:
        return UpdateJokeSettingsResponse(
            success=False, message=f"Failed to update joke service settings: {str(e)}"
        )
