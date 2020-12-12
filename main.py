import os
import sys
from crawler import extract
from assembler import parse
from doppler import doppler

if __name__ == "__main__":
    try:
        if sys.argv[1] == "populate":
            if not os.path.exists(os.path.join(os.getcwd(), "data")):
                os.mkdir(os.path.join(os.getcwd(), "data"))

            parser = extract.ContentExtractor(
                "http://eclipse-phase.wikia.com",
                "http://eclipse-phase.wikia.com/wiki/Local_Sitemap",
                os.path.join(os.getcwd(), "data"),
                "#mw-content-text",
            )

            parser.parse_sitemap()
            parser.filter_wiki_pages()
            parser.download_and_parse_pages()

            content = parse.ContentDatabase(
                "game_content.db",
                os.path.join(os.getcwd(), "data"),
                os.path.join(os.getcwd(), "data/contents"),
            )
            content.make_content_database()
            content.add_game_system("eclipse phase")
            content.populate_content_table("eclipse phase")

    except IndexError:
        client = doppler.Muse()
        client.run("your token here")
