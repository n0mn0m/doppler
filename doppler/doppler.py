import os
import sqlite3
from textwrap import wrap
from .utilities import shift_table
import discord


class Muse(discord.Client):
    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    async def on_message(self, message):
        """
        Route to Muse function based on call.
        """
        if message.content.startswith("!search"):
            term = message.content
            term = term.split(None, 1)[1]
            await self.search(message, term)
        if message.content.startswith("!shift"):
            await self.send_message(message.channel, shift_table())
        if message.content.startswith("!muse_help"):
            await self.muse_help(message)

    async def muse_help(self, message):
        commands = {
            "": "Commands start with !. For example !search gargoyle",
            "roll_fate": "provides the results from rolling 4 FATE dice",
            "search": "provided a term with search and provide the results from the game system content database",
            "shift": "provides a summary of the FATE shift table",
        }
        for k, v in commands.items():
            await self.send_message(message.channel, f"{k} {v}")

    async def roll_fate(self):
        raise NotImplementedError

    async def search(self, message, term):
        conn = sqlite3.connect(os.path.join(os.getcwd(), "data/game_content.db"))
        cur = conn.cursor()

        with conn:
            cur.execute(f'SELECT content FROM content where page like "%{term}%"')
            content = cur.fetchone()[0]
            if content:
                if len(content) > 1999:
                    await self.send_message(message.channel, f"Results for {term} \n\n")
                    chunks = wrap(content, 1999)
                    for chunk in chunks:
                        await self.send_message(message.channel, f"{chunk}")
                else:
                    await self.send_message(
                        message.channel, f"Results for {term} \n {content}"
                    )
            else:
                await self.send_message(message.channel, f"No results for {term}")


if __name__ == "__main__":
    client = Muse()
    client.run("your token here")
