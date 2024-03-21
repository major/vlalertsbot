"""Send Discord notifications."""

from discord_webhook import DiscordEmbed, DiscordWebhook

from vlalertsbot.alert import Alert
from vlalertsbot.config import DISCORD_WEBHOOK_URL, STOCK_LOGO, TRANSPARENT_PNG


def build_description(alert: Alert) -> str:
    """Build the description."""
    description = [
        f"**{alert.volume}** shares for **${alert.dollars}**",
        f"**{alert.relative_size}x** avg trade & bigger then **{alert.size}%** of all trades",
    ]
    if alert.last_trade_date:
        description.append(f"Trade this large last seen **{alert.last_trade_date}**")
    return "\n".join(description)


def send_discord_notification(alert: Alert) -> None:
    """Send a Discord notification."""
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)

    embed = DiscordEmbed(
        title=f"{alert.symbol}: #{alert.rank} @ ${alert.price}",
        description=build_description(alert),
    )
    # embed.set_author(**self.generate_action())
    embed.set_image(url=TRANSPARENT_PNG)
    embed.set_thumbnail(url=STOCK_LOGO % alert.symbol)
    embed.set_footer(text=f"Traded: {alert.timestamp} Eastern")

    webhook.add_embed(embed)
    webhook.execute()
