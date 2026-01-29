import unittest
from models import BasketballTeam
from analysis import BasketAnalysis

# Testy jednostkowe dla klasy BasketAnalysis
class TestBasketAnalysis(unittest.TestCase):

    def setUp(self):
        self.matches = [
            {
                "Data i godzina meczu": "01.01.2024",
                "Przeciwnik": "Team A",
                "Punkty Basket Hills": 80,
                "Punkty przeciwnika": 70,
                "Wynik meczu": "Wygrana",
                "Miejsce meczu": "U siebie"
            },
            {
                "Data i godzina meczu": "05.01.2024",
                "Przeciwnik": "Team B",
                "Punkty Basket Hills": 65,
                "Punkty przeciwnika": 75,
                "Wynik meczu": "Porażka",
                "Miejsce meczu": "Na wyjeździe"
            },
            {
                "Data i godzina meczu": "10.01.2024",
                "Przeciwnik": "Team C",
                "Punkty Basket Hills": 90,
                "Punkty przeciwnika": 85,
                "Wynik meczu": "Wygrana",
                "Miejsce meczu": "U siebie"
            },
        ]
        team = BasketballTeam("Basket Hills", self.matches)
        self.analysis = BasketAnalysis(team)
        self.df = self.analysis.df

    def test_win_loss_ratio(self):
        result = BasketAnalysis.win_loss_ratio(self.df)
        self.assertEqual(result["Wygrana"], 2)
        self.assertEqual(result["Porażka"], 1)

    def test_avg_points_scored(self):
        result = BasketAnalysis.avg_points_scored(self.df)
        self.assertEqual(result, (80 + 65 + 90) / 3)

    def test_avg_points_conceded(self):
        result = BasketAnalysis.avg_points_conceded(self.df)
        self.assertEqual(result, (70 + 75 + 85) / 3)

    def test_home_away_results(self):
        result = BasketAnalysis.home_away_results(self.df)
        self.assertEqual(result["U siebie"]["Wygrana"], 2)
        self.assertEqual(result["Na wyjeździe"]["Porażka"], 1)

    def test_avg_points_home_away(self):
        result = BasketAnalysis.avg_points_home_away(self.df)
        self.assertEqual(result["U siebie"], (80 + 90) / 2)
        self.assertEqual(result["Na wyjeździe"], 65)

    def test_win_loss_home_away(self):
        result = BasketAnalysis.win_loss_home_away(self.df)
        self.assertEqual(result.loc["U siebie", "Wygrana"], 2)
        self.assertEqual(result.loc["Na wyjeździe", "Porażka"], 1)

    def test_point_difference(self):
        df = BasketAnalysis.point_difference(self.df)
        self.assertEqual(df["Różnica punktów"].tolist(), [10, -10, 5])

    def test_top_bottom_games(self):
        top, bottom = BasketAnalysis.top_bottom_games(self.df, n=1)
        self.assertEqual(top.iloc[0]["Przeciwnik"], "Team C")
        self.assertEqual(bottom.iloc[0]["Przeciwnik"], "Team B")

    def test_run_method(self):
        results = self.analysis.run()
        self.assertIn("avg_scored", results)
        self.assertEqual(results["avg_scored"], round((80 + 65 + 90) / 3, 2))


if __name__ == "__main__":
    unittest.main()