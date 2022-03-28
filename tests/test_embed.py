"""Tests for qord.Embed"""

from qord.dataclasses.embeds import (
    Embed,
    EmbedAuthor,
    EmbedFooter,
)

import unittest


class TestEmbeds(unittest.TestCase):
    def test_total_length(self):
        embed = Embed()
        embed.title = "*" * 952
        embed.description = "*" * 2048

        assert embed.total_length() == 3000

        embed.author = EmbedAuthor(name="*" * 1000)
        embed.footer = EmbedFooter(text="*" * 1000)
        embed.set_field(name="*" * 500, value="*" * 500)

        assert embed.total_length() == 6000


if __name__ == "__main__":
    unittest.main()
