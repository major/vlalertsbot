"""Get VL Alerts from my inbox."""
import email
import logging
import os
import re

import pickledb
from discord_webhook import DiscordEmbed, DiscordWebhook
from imapclient import IMAPClient

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", False)
IMAP_USERNAME = os.environ.get("IMAP_USERNAME", False)
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD", False)


STOCK_LOGO = "https://s3.amazonaws.com/logos.atom.finance/stocks-and-funds/%s.png"
TRANSPARENT_PNG = "https://major.io/transparent.png"

logging.basicConfig(level=logging.INFO)

client = IMAPClient('imap.fastmail.com', ssl=True)
client.login(IMAP_USERNAME, IMAP_PASSWORD)
client.select_folder("VLAlerts", readonly=True)
messages = client.search()

db = pickledb.load('vl_alerts.db', False)

for uid, message_data in client.fetch(messages, "RFC822").items():
    email_message = email.message_from_bytes(message_data[b"RFC822"])
    raw_message = str(email_message.get_payload(decode=True))
    
    message_id = email_message.get('Message-ID')
    if db.get(message_id) == True:
        logging.info(f"Skipping message %s because it's already in the database.", message_id)
        continue

    logging.info("Processing message %s", message_id)

    # Dig all the useful data out of the email.
    try:
        symbol, trade_date, trade_time = re.findall(r"([A-Z]*) printed an important [closing ]*?trade on ([0-9\-]*) @ ([0-9:]*)", raw_message)[0]
    except IndexError:
        logging.error("Failed to parse message %s", message_id)
        continue
    price = re.findall(r"PRICE: \$([0-9\.,]*)", raw_message)[0]
    dollars = re.findall(r"DOLLARS: \$([0-9,]*)", raw_message)[0]
    rank = re.findall(r"RANK: ([0-9]*)", raw_message)[0]
    volume = re.findall(r"VOLUME: ([0-9,]*) shares", raw_message)[0]
    size = re.findall(r"SIZE: Larger than ([0-9\.]*)%", raw_message)[0]
    relative_size = re.findall(r"RELATIVE SIZE: ([0-9]*)x larger than", raw_message)[0]
    try:
        last_trade_date = re.findall(r"This is its largest trade since [\w]+, ([\w\s,]+).", raw_message)[0]
    except IndexError:
        last_trade_date = "ever"

    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    embed = DiscordEmbed(
        title=f"{symbol}: #{rank} @ ${price}",
        description=(
            f"**{volume}** shares for **${dollars}**\n"
            f"**{relative_size}x** larger than average\n"
            f"Larger than **{size}%** of all trades\n"
            f"Trade this large last seen **{last_trade_date}**\n"
        ),
    )
    # embed.set_author(**self.generate_action())
    embed.set_image(url=TRANSPARENT_PNG)
    embed.set_thumbnail(url=STOCK_LOGO % symbol)
    embed.set_footer(text=f"Traded on {trade_date} @ {trade_time} Eastern")

    webhook.add_embed(embed)
    webhook.execute()

    db.set(message_id, True)
    db.dump()