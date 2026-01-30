import pandas as pd

# Klasa do analizy danych meczowych drużyny koszykarskiej
class BasketAnalysis:
    def __init__(self, team):
        self.team = team
        self.df = pd.DataFrame(team.get_matches())

        # Konwersja kolumn do odpowiednich typów
        self.df["Data i godzina meczu"] = pd.to_datetime(
            self.df["Data i godzina meczu"], dayfirst=True, errors="coerce"
        )
        self.df["Punkty Basket Hills"] = pd.to_numeric(self.df["Punkty Basket Hills"], errors="coerce")
        self.df["Punkty przeciwnika"] = pd.to_numeric(self.df["Punkty przeciwnika"], errors="coerce")

        # Usunięcie błędnych rekordów i sortowanie chronologiczne
        self.df = self.df.dropna(subset=["Data i godzina meczu", "Punkty Basket Hills", "Punkty przeciwnika"])
        self.df = self.df.sort_values("Data i godzina meczu").reset_index(drop=True)

    # Metoda statyczna do obliczania stosunku wygranych do przegranych
    @staticmethod
    def win_loss_ratio(df):
        return df["Wynik meczu"].value_counts()

    # Metoda statyczna do obliczania średniej liczby punktów zdobytych na mecz
    @staticmethod
    def avg_points_scored(df):
        return df["Punkty Basket Hills"].mean()

    # Metoda statyczna do obliczania średniej liczby punktów straconych na mecz
    @staticmethod
    def avg_points_conceded(df):
        return df["Punkty przeciwnika"].mean()

    # Metoda statyczna do analizy wyników meczów u siebie i na wyjeździe
    @staticmethod
    def home_away_results(df):
        return df.groupby("Miejsce meczu")["Wynik meczu"].value_counts()

    # Metoda statyczna do obliczania średniej liczby punktów zdobytych u siebie i na wyjeździe
    @staticmethod
    def avg_points_home_away(df):
        return df.groupby("Miejsce meczu")["Punkty Basket Hills"].mean()

    # Metoda statyczna do analizy stosunku wygranych do przegranych u siebie i na wyjeździe
    @staticmethod
    def win_loss_home_away(df):
        return df.pivot_table(
            index="Miejsce meczu",
            columns="Wynik meczu",
            aggfunc="size",
            fill_value=0
        )

    # Metoda statyczna do obliczania różnicy punktowej w każdym meczu
    @staticmethod
    def point_difference(df):
        df = df.copy()
        df["Różnica punktów"] = df["Punkty Basket Hills"] - df["Punkty przeciwnika"]
        return df[["Data i godzina meczu", "Różnica punktów"]]

    # Metoda statyczna do identyfikacji najlepszych i najsłabszych meczów drużyny
    @staticmethod
    def top_bottom_games(df, n=5):
        top = df.nlargest(n, "Punkty Basket Hills")[["Data i godzina meczu", "Przeciwnik", "Punkty Basket Hills"]]
        bottom = df.nsmallest(n, "Punkty Basket Hills")[["Data i godzina meczu", "Przeciwnik", "Punkty Basket Hills"]]
        return top, bottom

    # Metoda statyczna do obliczanie najdłuższą serię wygranych i najdłuższą serię porażek w sezonie
    @staticmethod
    def longest_streak(df):
        groups = (df["Wynik meczu"] != df["Wynik meczu"].shift()).cumsum()
        streaks = df.groupby(groups)["Wynik meczu"].agg(["first", "size"])
        longest_wins = streaks[streaks["first"] == "Wygrana"]["size"].max()
        longest_losses = streaks[streaks["first"] == "Porażka"]["size"].max()
        return longest_wins, longest_losses

    def run(self):
        return {
            "wins_losses": self.win_loss_ratio(self.df),
            "avg_scored": round(self.avg_points_scored(self.df), 2),
            "avg_conceded": round(self.avg_points_conceded(self.df), 2),
            "home_away": self.home_away_results(self.df),
            "avg_home_away": self.avg_points_home_away(self.df),
            "win_loss_home_away": self.win_loss_home_away(self.df),
            "point_diff": self.point_difference(self.df),
            "top_games": self.top_bottom_games(self.df)[0],
            "bottom_games": self.top_bottom_games(self.df)[1],
            "streaks": self.longest_streak(self.df),  
            "df": self.df
        }