import cloudscraper
import re
import sys
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = 'https://www.gocomics.com/darksideofthehorse'

print(f"--- SCRAPE START: Dark Side of the Horse ---")

# We maken een scraper aan die zich gedraagt als een echte browser
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

try:
    response = scraper.get(URL, timeout=20)
    html = response.text
    
    if "Establishing a secure connection" in html:
        print("FOUT: Zelfs cloudscraper werd geblokkeerd door de beveiligingsmuur.")
        sys.exit(1)
        
    print(f"SUCCES: Pagina geladen (Status {response.status_code})")
except Exception as e:
    print(f"FOUT: Verbinding mislukt. {e}")
    sys.exit(1)

# We zoeken specifiek naar de ID die in de assets-map staat.
# Dit zorgt ervoor dat we exact de 9a17... (of vergelijkbare) strip-ID pakken.
match = re.search(r'assets[\\\/]+([a-f0-9]{32})', html)

if match:
    asset_id = match.group(1)
    image_url = f"https://featureassets.gocomics.com/assets/{asset_id}?optimizer=image&width=1400&quality=85"
    print(f"GEVONDEN ID: {asset_id}")
    
    # RSS opbouw
    fg = FeedGenerator()
    fg.id(URL)
    fg.title('Dark Side of the Horse')
    fg.link(href=URL, rel='alternate')
    fg.description('Dagelijkse strip via Cloudscraper Bypass')
    
    fe = fg.add_entry()
    fe.id(image_url)
    fe.title(f'Dark Side of the Horse - {datetime.now().strftime("%Y-%m-%d")}')
    fe.link(href=URL)
    fe.description(f'<img src="{image_url}" />')
    
    fg.rss_file('darksideofthehorse.xml', pretty=True)
    print("SUCCES: 'darksideofthehorse.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)