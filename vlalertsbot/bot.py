"""Core bot functionality."""

import email
import logging

from imapclient import IMAPClient

from vlalertsbot import config
from vlalertsbot.alert import Alert
from vlalertsbot.notify import send_discord_notification

log = logging.getLogger(__name__)


def get_emails() -> list:
    """Get the emails from the email server."""
    client = IMAPClient("imap.fastmail.com", ssl=True)
    client.login(config.IMAP_USERNAME, config.IMAP_PASSWORD)
    client.select_folder("VLAlerts", readonly=True)
    messages = client.search()

    return list(client.fetch(messages, "RFC822").items())


def is_new_email(message_id: str) -> bool:
    """Check if the email is new."""
    return bool(config.DATABASE.get(message_id) is not True)


def mark_email_as_read(message_id: str) -> None:
    """Mark the email as read."""
    config.DATABASE[message_id] = True
    config.DATABASE.dump()


def process_emails() -> None:
    """Process the emails."""
    for _, data in get_emails():
        email_message = email.message_from_bytes(data[b"RFC822"])
        raw_message = str(email_message.get_payload(decode=True))
        subject = email.header.decode_header(email_message["Subject"])[0][0].decode("utf-8")

        message_id = email_message.get("Message-ID", "missing")
        if is_new_email(message_id):
            email_message = email.message_from_bytes(data[b"RFC822"])
            log.info("New email: %s", subject)

            alert = Alert(raw_message)
            send_discord_notification(alert)

            mark_email_as_read(message_id)
        else:
            log.info("Old email: %s", subject)


if __name__ == "__main__":
    process_emails()
