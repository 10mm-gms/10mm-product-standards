import asyncio
import logging
import os
import uuid

import boto3
import httpx
import markdown2
from botocore.config import Config

from ..config import GmsBackendSettings

logger = logging.getLogger(__name__)


async def send_ses_email(
    settings: GmsBackendSettings,
    recipient: str,
    subject: str,
    body_markdown: str,
):
    """
    Sends an email via AWS SES API.
    Renders markdown to HTML.
    """
    if not all(
        [
            settings.ses_region,
            settings.ses_access_key,
            settings.ses_secret_key,
            settings.ses_from_email,
        ]
    ):
        logger.info(f"Email to {recipient} skipped: SES not fully configured.")
        return False

    body_html = markdown2.markdown(body_markdown)
    loop = asyncio.get_event_loop()

    def _sync_send():
        config = Config(
            region_name=settings.ses_region,
            connect_timeout=5,
            read_timeout=10,
            retries={"max_attempts": 0},
        )
        client = boto3.client(
            "ses",
            config=config,
            aws_access_key_id=settings.ses_access_key,
            aws_secret_access_key=settings.ses_secret_key,
        )
        return client.send_email(
            Source=settings.ses_from_email,
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Html": {"Data": body_html}, "Text": {"Data": body_markdown}},
            },
        )

    try:
        if os.getenv("MOCK_SES") == "true":
            logger.info(f"MOCK SES: Email to {recipient} would have been sent (MOCK_SES active)")
            return f"mock-msg-{uuid.uuid4()}"

        response = await loop.run_in_executor(None, _sync_send)
        return response.get("MessageId")
    except Exception as e:
        logger.error(f"Failed to send SES email to {recipient}: {e}")
        raise


async def send_google_chat_message(
    settings: GmsBackendSettings,
    text: str,
):
    """Sends a message to a Google Chat space via webhook."""
    if not settings.google_chat_webhook_url:
        logger.info("Google Chat notification skipped: webhook URL not configured.")
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(settings.google_chat_webhook_url, json={"text": text})
        response.raise_for_status()
        return True
