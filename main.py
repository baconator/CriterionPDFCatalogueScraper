import codecs
from catalogue import Catalogue
import argparse
import config

__author__ = 'Bacon'

# Do some argument parsing.
parser = argparse.ArgumentParser(description="Fetch and scrape the most recent Criterion Pictures DVD catalogue PDF.")
parser.add_argument("--dest",
                    dest="destination",
                    help="The destination file (overwritten if exists).")
parser.add_argument("--src",
                    dest="source",
                    help="The source PDF file. Defaults to the most recent one in Criterion's catalogue.",
                    default="")

args = parser.parse_args()

destination = args.destination
source = args.source
if not args.source:
    # If no source is passed, pull down a fresh copy of the DVD catalogue.
    import requests
    try:
        response = requests.get("http://www.criterionpic.com/CPL/mm/criterion_dvd.pdf")
        with open(config.DEFAULT_DOWNLOAD_LOCATION, "wb") as pdf:
            pdf.write(response.content)
        source = config.DEFAULT_DOWNLOAD_LOCATION
    except requests.exceptions.HTTPError:
        raise Exception("Couldn't download the DVD catalogue.")

with codecs.open(destination, "w", encoding="utf-8") as output:
    catalogue = Catalogue(source)
    output.writelines(map(unicode, catalogue.movies))