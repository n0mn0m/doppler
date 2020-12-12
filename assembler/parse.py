import sqlite3
import datetime
import os


class ContentDatabase:
    """
    Create a sqlite database of the content extracted by the crawler.
    This database will then be used by doppler to query keywords
    provided by users and return the associated content.
    """

    def __init__(self, db, data_dir, content_dir):
        self.db = db
        self.data_dir = data_dir
        self.content_dir = content_dir

    def make_content_database(self):
        print(self.data_dir)
        conn = sqlite3.connect(os.path.join(self.data_dir, self.db))
        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS game
                     (id INTEGER PRIMARY KEY, system TEXT)"""
        )

        c.execute(
            """CREATE TABLE IF NOT EXISTS content
                     (system_id INTEGER, page TEXT PRIMARY KEY, content TEXT, keywords TEXT, updated DATETIME DEFAULT CURRENT_TIMESTAMP)"""
        )

        conn.commit()
        conn.close()

    def add_game_system(self, system):
        conn = sqlite3.connect(os.path.join(self.data_dir, self.db))
        c = conn.cursor()

        c.execute("INSERT INTO game(system) VALUES (?)", (system,))

        conn.commit()
        conn.close()

    def populate_content_table(self, system):
        now = datetime.datetime.now()

        conn = sqlite3.connect(os.path.join(self.data_dir, self.db))
        c = conn.cursor()

        c.execute("select id from game where system=:system", {"system": system})
        system_id = c.fetchone()

        with os.scandir(self.content_dir) as content_dir:
            for path_object in content_dir:
                if os.path.isfile(path_object):
                    with open(path_object, "r") as content_file:
                        file_text = content_file.read()
                        c.execute(
                            "INSERT INTO content(system_id, page, content) VALUES (?, ?, ?)",
                            (system_id[0], path_object.name, file_text),
                        )
                        conn.commit()
        conn.close()

    def update_content_database(self, age):
        """
        Using the updated column the crawler will refresh page content that hasn't been updated
        in X days.
        """
        raise NotImplementedError


if __name__ == "__main__":
    content = ContentDatabase(
        "game_content.db",
        os.path.join(os.getcwd(), "data"),
        os.path.join(os.getcwd(), "data/contents"),
    )
    content.make_content_database()
    content.add_game_system("eclipse phase")
    content.populate_content_table("eclipse phase")

    conn = sqlite3.connect(os.path.join(os.getcwd(), "data/game_content.db"))
    cur = conn.cursor()

    with conn:
        cur.execute("SELECT * FROM game")
        for row in cur:
            print(row)

    with conn:
        cur.execute("SELECT * FROM content")
        for row in cur:
            print(row)
