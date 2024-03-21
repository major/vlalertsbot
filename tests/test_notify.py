"""Test cases for alert module."""

from unittest import mock

from vlalertsbot import notify
from vlalertsbot.alert import Alert


def test_build_description(real_emails):
    """Test building the description."""
    alert = Alert(real_emails)
    description = notify.build_description(alert)
    assert isinstance(description, str)
    assert len(description) > 0


@mock.patch("vlalertsbot.notify.DISCORD_WEBHOOK_URL", new="https://127.0.0.1/api/webhooks/123")
@mock.patch("vlalertsbot.notify.DiscordWebhook.execute")
def test_send_discord_notification(mock_execute, real_emails):
    """Test sending a Discord notification."""
    alert = Alert(real_emails)
    notify.send_discord_notification(alert)
    assert mock_execute.called
