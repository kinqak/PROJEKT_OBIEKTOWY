import unittest
from unittest.mock import patch, Mock
from data_fetcher import MatchDataFetcher


class TestMatchDataFetcher(unittest.TestCase):
    @patch("data_fetcher.requests.get")
    def test_fetch_matches_parses_single_match_home(self, mock_get):
        html = """
        <html><body>
        <table><tbody>
          <tr>
            <td>1</td>
            <td>Basket Hills Bielsko-Biała</td>
            <td>80:70</td>
            <td>Team A</td>
            <td>01.01.2024</td>
          </tr>
        </tbody></table>
        </body></html>
        """

        mock_resp = Mock()
        mock_resp.text = html
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        f = MatchDataFetcher("http://example.com", "Basket Hills Bielsko-Biała")
        data, download_time = f.fetch_matches()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Przeciwnik"], "Team A")
        self.assertEqual(data[0]["Punkty Basket Hills"], 80)
        self.assertEqual(data[0]["Punkty przeciwnika"], 70)
        self.assertEqual(data[0]["Wynik meczu"], "Wygrana")
        self.assertEqual(data[0]["Miejsce meczu"], "U siebie")

    @patch("data_fetcher.requests.get")
    def test_fetch_matches_parses_single_match_away(self, mock_get):
        html = """
        <html><body>
        <table><tbody>
          <tr>
            <td>1</td>
            <td>Team B</td>
            <td>65:75</td>
            <td>Basket Hills Bielsko-Biała</td>
            <td>05.01.2024</td>
          </tr>
        </tbody></table>
        </body></html>
        """

        mock_resp = Mock()
        mock_resp.text = html
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        f = MatchDataFetcher("http://example.com", "Basket Hills Bielsko-Biała")
        data, download_time = f.fetch_matches()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Przeciwnik"], "Team B")
        self.assertEqual(data[0]["Punkty Basket Hills"], 75)   # bo Basket Hills jest po prawej
        self.assertEqual(data[0]["Punkty przeciwnika"], 65)
        self.assertEqual(data[0]["Wynik meczu"], "Wygrana")
        self.assertEqual(data[0]["Miejsce meczu"], "Na wyjeździe")

    @patch("data_fetcher.requests.get")
    def test_fetch_matches_skips_rows_without_team(self, mock_get):
        html = """
        <html><body>
        <table><tbody>
          <tr>
            <td>1</td>
            <td>Team X</td>
            <td>80:70</td>
            <td>Team Y</td>
            <td>01.01.2024</td>
          </tr>
        </tbody></table>
        </body></html>
        """

        mock_resp = Mock()
        mock_resp.text = html
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        f = MatchDataFetcher("http://example.com", "Basket Hills Bielsko-Biała")
        data, download_time = f.fetch_matches()

        self.assertEqual(data, [])  


if __name__ == "__main__":
    unittest.main()