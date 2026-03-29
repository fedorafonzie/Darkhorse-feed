import requests
import re
import sys
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

# --- CONFIGURATIE ---
URL = 'https://www.gocomics.com/darksideofthehorse'
# Exact dezelfde headers die werkten voor Sherman's Lagoon
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

print(f"--- START SCRAPE: Dark Side of the Horse ---")

# Stap 1: Haal de pagina op
try:
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    html = response.text
    print(f"SUCCES: Pagina opgehaald. Status: {response.status_code}")
except Exception as e:
    print(f"FOUT: Verbinding mislukt. {e}")
    sys.exit(1)

# Stap 2: Zoek de 32-cijferige ID achter 'assets/'
# Dit is de methode die technische codes negeert en de strip-ID vindt
match = re.search(r'assets[\\\/]+([a-f0-9]{32})', html)

if match:
    asset_id = match.group(1)
    image_url = f"https://featureassets.gocomics.com/assets/{asset_id}?optimizer=image&width=1400&quality=85"
    print(f"GEVONDEN ID: {asset_id}")
    print(f"URL: {image_url}")
else:
    print("FOUT: Geen strip-ID gevonden in de broncode.")
    sys.exit(1)

# Stap 3: Bouw de RSS-feed
fg = FeedGenerator()
fg.id(URL)
fg.title('Dark Side of the Horse')
fg.link(href=URL, rel='alternate')
fg.description('Dagelijkse strip van Dark Side of the Horse via GoComics')
fg.language('en')

current_date = datetime.now(timezone.utc)
date_str = current_date.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url)
fe.title(f'Dark Side of the Horse - {date_str}')
fe.link(href=URL)
fe.pubDate(current_date)
fe.description(f'<img src="{image_url}" alt="Dark Side of the Horse strip" />')

# Stap 4: Schrijf het XML-bestand weg
try:
    fg.rss_file('darksideofthehorse.xml', pretty=True)
    print("KLAAR: 'darksideofthehorse.xml' is aangemaakt.")
except Exception as e:
    print(f"FOUT bij wegschrijven: {e}")
    sys.exit(1)