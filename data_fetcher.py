import requests
from bs4 import BeautifulSoup
from decorators import log_call

# Klasa odpowiedzialna za pobieranie i parsowanie danych meczowych ze strony internetowej
class MatchDataFetcher:
    def __init__(self, url, team_name):
        self.url = url
        self.team_name = team_name
        self.download_time = None  

    # dekorator mierzący czas pobrania HTML 
    @log_call
    def _download_html(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    
    def fetch_matches(self):
        html = self._download_html()

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table tbody tr")

        data = []
        for r in rows:
            cols = [c.get_text(strip=True) for c in r.find_all("td")]
            if len(cols) >= 5:
                left_team = cols[1]
                score = cols[2]
                right_team = cols[3]
                date = cols[4]

                if ":" not in score or "–" in score or "-" in score:
                    continue

                try:
                    left_pts, right_pts = [int(x) for x in score.split(":")]
                except:
                    continue

                if self.team_name.lower() in left_team.lower():
                    opponent = right_team
                    my_pts = left_pts
                    opp_pts = right_pts
                    location = "U siebie"
                elif self.team_name.lower() in right_team.lower():
                    opponent = left_team
                    my_pts = right_pts
                    opp_pts = left_pts
                    location = "Na wyjeździe"
                else:
                    continue

                data.append({
                    "Data i godzina meczu": date,
                    "Przeciwnik": opponent,
                    "Punkty Basket Hills": my_pts,
                    "Punkty przeciwnika": opp_pts,
                    "Wynik meczu": "Wygrana" if my_pts > opp_pts else "Porażka",
                    "Miejsce meczu": location
                })

        return data, self.download_time