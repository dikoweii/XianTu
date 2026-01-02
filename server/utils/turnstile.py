from __future__ import annotations

from typing import Any

import httpx

from server.core.config import settings


async def verify_turnstile(
    *,
    token: str,
    remote_ip: str | None = None,
) -> tuple[bool, list[str]]:
    """
    Verify a Cloudflare Turnstile token.

    Returns (success, error_codes).
    """
    if not settings.TURNSTILE_SECRET_KEY:
        return False, ["missing-secret"]

    data: dict[str, Any] = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        data["remoteip"] = remote_ip

    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.post(settings.TURNSTILE_VERIFY_URL, data=data)
        resp.raise_for_status()
        payload = resp.json()

    success = bool(payload.get("success"))
    error_codes = payload.get("error-codes") or []
    if not isinstance(error_codes, list):
        error_codes = [str(error_codes)]

    return success, [str(x) for x in error_codes]
