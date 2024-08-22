"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi

from src.utilities.messages.exceptions.http.exc_details import (
    http_409_user_collision_details
)


async def http_409_exc_bad_user_collision_request(id: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_409_CONFLICT,
        detail=http_409_user_collision_details(id=id),
    )
