"""Core bot functionality."""

import logging
import re
from dataclasses import dataclass
from functools import cached_property
from typing import Optional

log = logging.getLogger(__name__)


@dataclass
class Alert:
    """Parse alerts from VL."""

    body: str

    def get_first_match(self, pattern: str) -> Optional[str]:
        """Get the first match from the body."""
        matches = re.search(pattern, self.body)
        return matches[1] if matches else None

    @cached_property
    def dollars(self) -> Optional[str]:
        """Parse the dollars from the alert."""
        return self.get_first_match(r"DOLLARS: \$([0-9\.,]*)")

    @cached_property
    def last_trade_date(self) -> Optional[str]:
        """Parse the last trade date from the alert."""
        return self.get_first_match(r"This is its largest trade since [\w]+, ([\w\s,]+).")

    @cached_property
    def price(self) -> Optional[str]:
        """Parse the price from the alert."""
        return self.get_first_match(r"PRICE: \$([0-9\.,]*)")

    @cached_property
    def rank(self) -> Optional[str]:
        """Parse the rank from the alert."""
        return self.get_first_match(r"RANK: ([0-9]*)")

    @cached_property
    def relative_size(self) -> Optional[str]:
        """Parse the relative size from the alert."""
        return self.get_first_match(r"RELATIVE SIZE: ([0-9]*)x larger than")

    @cached_property
    def size(self) -> Optional[str]:
        """Parse the size from the alert."""
        return self.get_first_match(r"SIZE: Larger than ([0-9\.,]*)%")

    @cached_property
    def symbol(self) -> Optional[str]:
        """Parse the symbol from the alert."""
        return self.get_first_match(r"([A-Z]+) printed")

    @cached_property
    def timestamp(self) -> Optional[str]:
        """Parse the timestamp from the alert."""
        return self.get_first_match(r"([\d\-]+) @ ([\d:]+)")

    @cached_property
    def volume(self) -> Optional[str]:
        """Parse the volume from the alert."""
        return self.get_first_match(r"VOLUME: ([0-9\.,]*) shares")
