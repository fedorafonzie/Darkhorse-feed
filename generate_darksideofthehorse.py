import requests
import re
import sys
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = 'https://www.gocomics.com/darksideofthehorse'

# We gebruiken een sessie om cookies te onthouden (belangrijk voor beveiliging)
session = requests.Session()

# We bootsen een iPhone na. Beveiligingssystemen laten mobiele gebruikers 
# vaker door zonder JavaScript-challenge om batterij te sparen.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
}

print(f"--- START SCRAPE: Dark Side of the Horse (Mobile Simulation) ---")

try:
    # We doen eerst een 'bezoek' aan de hoofdpagina om een cookie te krijgen
    session.get('https://www.gocomics.com/', headers=HEADERS, timeout=10)
    
    # Nu halen we de werkelijke pagina op
    response = session.get(URL, headers=HEADERS, timeout=15)
    html = response.text
    
    if "Establishing a secure connection" in html:
        print("FOUT: De mobiele emulatie is ook geblokkeerd door Bunny Shield.")
        # Als laatste redmiddel: print de URL die in de foutpagina staat, soms zit de ID daar in.
        sys.exit(1)
        
    print(f"SUCCES: Pagina geladen (Status {response.status_code})")

except Exception as e:
    print(f"FOUT: Verbinding mislukt. {e}")
    sys.exit(1)

# Zoek de 32-cijferige ID achter 'assets/'
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
    fg.description('Dagelijkse strip')
    
    fe = fg.add_entry()
    fe.id(image_url)
    fe.title(f'Dark Side of the Horse - {datetime.now().strftime("%Y-%m-%d")}')
    fe.link(href=URL)
    fe.description(f'<img src="{image_url}" />')
    
    fg.rss_file('darksideofthehorse.xml', pretty=True)
    print("XML bestand succesvol aangemaakt.")
else:
    print("FOUT: Geen strip-ID gevonden in de broncode.")
    sys.exit(1)
