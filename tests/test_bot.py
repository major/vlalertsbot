"""Test cases for bot module."""

from unittest import mock

import pickledb

from vlalertsbot import bot


@mock.patch("vlalertsbot.bot.config")
def test_is_new_email(mock_config, tmp_path_factory):
    """Test parsing an email one time only when it is new."""
    fn = tmp_path_factory.mktemp("data")
    mock_config.DATABASE = pickledb.load(f"{fn}/vl_alerts.db", False)

    assert bot.is_new_email("123") is True
    bot.mark_email_as_read("123")
    assert bot.is_new_email("123") is False
