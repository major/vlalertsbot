"""Test cases for alert module."""

import pytest

from vlalertsbot.alert import Alert


def test_alert_price(real_emails):
    """Test alert price."""
    alert = Alert(real_emails)
    assert isinstance(alert.price, str)
    assert len(alert.price) > 0
    assert alert.price.replace(".", "").replace(",", "").isdigit()


def test_alert_dollars(real_emails):
    """Test alert dollars."""
    alert = Alert(real_emails)
    assert isinstance(alert.dollars, str)
    assert len(alert.dollars) > 0
    assert alert.dollars.replace(".", "").replace(",", "").isdigit()


@pytest.mark.parametrize("real_emails", ["trade_rank"], indirect=True)
def test_alert_last_trade_date(real_emails):
    """Test alert last trade date."""
    alert = Alert(real_emails)
    assert isinstance(alert.last_trade_date, str)
    assert len(alert.last_trade_date) > 0


@pytest.mark.parametrize("real_emails", ["trade_rank_1"], indirect=True)
def test_alert_last_trade_date_missing(real_emails):
    """Test alert last trade date for #1 trades."""
    alert = Alert(real_emails)
    assert alert.last_trade_date is None


# Only trade rank alerts have a rank.
@pytest.mark.parametrize("real_emails", ["trade_rank"], indirect=True)
def test_alert_rank(real_emails):
    """Test alert rank."""
    alert = Alert(real_emails)
    assert isinstance(alert.rank, str)
    assert len(alert.rank) > 0
    assert alert.rank.isdigit()


def test_alert_relative_size(real_emails):
    """Test alert relative size."""
    alert = Alert(real_emails)
    assert isinstance(alert.relative_size, str)
    assert len(alert.relative_size) > 0
    assert alert.relative_size.isdigit()


def test_alert_size(real_emails):
    """Test alert size."""
    alert = Alert(real_emails)
    assert isinstance(alert.size, str)
    assert len(alert.size) > 0
    assert alert.size.replace(".", "").replace(",", "").isdigit()


def test_alert_symbol(real_emails):
    """Test alert symbol."""
    alert = Alert(real_emails)
    assert isinstance(alert.symbol, str)
    assert len(alert.symbol) <= 4
    assert len(alert.symbol) >= 1


def test_alert_timestamp(real_emails):
    """Test alert timestamp."""
    alert = Alert(real_emails)
    assert isinstance(alert.timestamp, str)
    assert len(alert.timestamp) > 0


def test_alert_volume(real_emails):
    """Test alert volume."""
    alert = Alert(real_emails)
    assert isinstance(alert.volume, str)
    assert len(alert.volume) > 0
    assert alert.volume.replace(".", "").replace(",", "").isdigit()
