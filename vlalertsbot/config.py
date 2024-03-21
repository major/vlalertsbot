"""Configuration options for the bot."""

import os

import pickledb

# Where the alerts should be sent.
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "missing webhook url")

# IMAP server.
IMAP_SERVER = os.environ.get("IMAP_SERVER", "imap.fastmail.com")

# IMAP credentials.
IMAP_USERNAME = os.environ.get("IMAP_USERNAME", "missing username")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD", "missing password")

# Database.
DATABASE = pickledb.load("vl_alerts.db", False)

# Get the stock logo for the embed.
STOCK_LOGO = "https://s3.amazonaws.com/logos.atom.finance/stocks-and-funds/%s.png"

# Transparent PNG to make the alerts the same width.
TRANSPARENT_PNG = "https://major.io/transparent.png"
