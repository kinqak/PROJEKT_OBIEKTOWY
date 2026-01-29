import streamlit as st
import subprocess
import sys
import io
import time
import unittest
import logging
from data_fetcher import MatchDataFetcher
from models import BasketballTeam
from analysis import BasketAnalysis
from plots import (
    PointsPlotMatplotlib, PointDiffPlotMatplotlib,
    AvgHomeAwayPlotMatplotlib, TopBottomPlotMatplotlib,
    PointsPlotSeaborn, PointDiffPlotSeaborn,
    AvgHomeAwayPlotSeaborn, TopBottomPlotSeaborn,
    PointsPlotPlotly, PointDiffPlotPlotly,
    AvgHomeAwayPlotPlotly, TopBottomPlotPlotly,
)


TEAM_URL = "https://rozgrywki.pzkosz.pl/liga/4/druzyny/d/4119/basket-hills-bielsko-biala/terminarz.html"
TEAM_NAME = "Basket Hills Bielsko-Biała"

st.set_page_config(page_title="Basket Hills – analiza danych", layout="wide")

@st.cache_data
def load_data():
    fetcher = MatchDataFetcher(TEAM_URL, TEAM_NAME)
    return fetcher.fetch_matches()  

menu = st.sidebar.radio(
    "Menu",
    ["Strona główna", "Analiza drużyny", "Wykresy", "Testy jednostkowe"]
)

with st.spinner("Pobieram dane z PZKosz..."):
    try:
        matches, download_time = load_data()
    except Exception as e:
        st.error("Nie udało się pobrać danych (PZKosz).")
        st.exception(e)
        st.stop()
team = BasketballTeam(TEAM_NAME, matches)
analysis = BasketAnalysis(team)
results = analysis.run()
results["longest_win_streak"], results["longest_loss_streak"] = analysis.longest_streak(results["df"])

if menu == "Strona główna":
    st.title("Projekt zaliczeniowy")

    st.subheader("Analiza wyników drużyny koszykarskiej Basket Hills Bielsko-Biała w rozgrywkach 2 Ligi Mężczyzn na podstawie danych ze strony PZKosz.")
    st.markdown(
    """
    **Autorzy:** Julia Matyja, Kinga Kołodziej  
    **Przedmiot:** Zaawansowane programowanie w języku Python  
    **Rok akademicki:** 2025/2026  
    """
    )

    st.divider()

    st.header("Opis projektu")

    st.subheader("Cel i zakres")
    st.markdown("""
Aplikacja służy do automatycznego pobierania danych meczowych ze strony internetowej, uporządkowania ich do postaci tabelarycznej
oraz wykonania analizy wyników drużyny **Basket Hills Bielsko-Biała**. Opracowane wyniki są prezentowane w formie tabel i wykresów
w aplikacji webowej (Streamlit), co ułatwia ich interpretację i porównywanie w trakcie sezonu.

ZZakres analizy obejmuje:
- chronologiczne zestawienie spotkań (data, przeciwnik, zdobyte i stracone punkty, rezultat, miejsce rozegrania),
- statystyki ogólne sezonu, w tym bilans zwycięstw i porażek oraz średnią liczbę punktów zdobytych i straconych,
- porównanie wyników w zależności od miejsca rozegrania meczu (*u siebie* / *na wyjeździe*),
- analizę różnicy punktowej w kolejnych spotkaniach,
- identyfikację najlepszych i najsłabszych meczów pod względem liczby zdobytych punktów,
- wyznaczenie najdłuższej serii zwycięstw i najdłuższej serii porażek w sezonie.
""")

    st.subheader("Źródło danych")
    st.markdown(
    "Dane są pobierane automatycznie z publicznie dostępnej strony rozgrywek **PZKosz**: "
    "[rozgrywki.pzkosz.pl](https://rozgrywki.pzkosz.pl). "
    "Wykorzystywana jest podstrona z terminarzem i wynikami spotkań drużyny **Basket Hills Bielsko-Biała**."
)

    st.subheader("Zakres pozyskiwanych informacji i struktura rekordu meczu")
    st.markdown("""
Dla każdego spotkania tworzony jest pojedynczy rekord (wiersz danych) zawierający następujące pola:
- **Data i godzina meczu** - po wczytaniu konwertowana do formatu daty/czasu,
- **Przeciwnik** - nazwa drużyny przeciwnej,
- **Punkty Basket Hills** - liczba punktów zdobytych przez analizowaną drużynę,
- **Punkty przeciwnika** - liczba punktów zdobytych przez rywala,
- **Wynik meczu** - klasyfikacja rezultatu (Wygrana / Porażka),
- **Miejsce meczu** - informacja o lokalizacji spotkania (U siebie / Na wyjeździe).
""")

    st.subheader("Funkcjonalności dostępne w aplikacji")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### Interfejs\n**Streamlit**")

    with c2:
        st.markdown("### Analiza danych\n**Pandas**")

    with c3:
        st.markdown("### Wizualizacja\n**Matplotlib**  \n**Seaborn**  \n**Plotly**")

    with c4:
        st.markdown("### Weryfikacja\n**Unittest**")

    st.markdown("""
Aplikacja została podzielona na moduły widoczne w menu, które odpowiadają kolejnym etapom pracy z danymi:

- **Analiza drużyny** - prezentacja wyników obliczeń w formie metryk i tabel (m.in. bilans, średnie punkty, podział dom/wyjazd,
  najdłuższe serie zwycięstw i porażek), wraz z informacją o czasie pozyskania danych ze źródła.
- **Wykresy** - wizualizacja przebiegu sezonu: trend punktów zdobytych i straconych, różnica punktowa w czasie,
  porównanie wyników dom/wyjazd oraz zestawienie najlepszych i najsłabszych spotkań.
- **Testy jednostkowe** - uruchamianie testów bezpośrednio z poziomu aplikacji oraz prezentacja podsumowania
  (liczba testów, zaliczone/niezaliczone/błędy/pominięte) z możliwością rozwinięcia szczegółów.
""")

    st.subheader("Podział projektu na moduły (pliki) i odpowiedzialności")
    st.markdown("""
Projekt został podzielony na moduły odpowiadające kolejnym etapom przetwarzania danych: pozyskaniu, modelowaniu, analizie,
wizualizacji oraz prezentacji wyników.

1. **`data_fetcher.py` - pozyskiwanie danych (web scraping)**  
   - Klasa `MatchDataFetcher` pobiera kod HTML strony przy użyciu biblioteki `requests` oraz wyodrębnia dane z tabeli z meczami
     (`BeautifulSoup`).  
   - Na podstawie układu spotkania (drużyna po lewej lub po prawej stronie wyniku `x:y`) przypisuje zdobyte i stracone punkty.  
   - Wyznacza miejsce rozegrania (U siebie / Na wyjeździe) oraz rezultat (Wygrana / Porażka).  
   - Zwraca dane w postaci: `(lista_meczy, czas_pobrania_html)`.

2. **`decorators.py` - funkcje pomocnicze dla warstwy pobierania danych**  
   - Zawiera dekorator `log_call`, który mierzy czas wykonania wybranej metody i zapisuje go w atrybucie `self.download_time`.  
   - Dekorator jest wykorzystywany w `MatchDataFetcher._download_html()` do pomiaru czasu pobrania HTML.

3. **`models.py` - warstwa modelu (reprezentacja obiektowa danych)**  
   - `SportsTeam` jest klasą abstrakcyjną definiującą minimalny interfejs obiektu drużyny (`get_name()`, `get_matches()`).  
   - `BasketballTeam` stanowi konkretną implementację: przechowuje nazwę drużyny oraz listę meczów i udostępnia je warstwie analizy.

4. **`analysis.py` - warstwa analityczna**  
   - `BasketAnalysis` konwertuje listę meczów do postaci `DataFrame`, następnie wykonuje przygotowanie danych:
     konwersję dat, konwersję wartości punktowych, odfiltrowanie rekordów niepoprawnych oraz sortowanie chronologiczne.  
   - Metody analityczne obliczają m.in. bilans zwycięstw i porażek, średnie punkty, zestawienia dom/wyjazd,
     różnicę punktową w czasie oraz wskazanie najlepszych i najsłabszych spotkań.

5. **`plots.py` - warstwa wizualizacji**  
   - `BasePlot` jest klasą abstrakcyjną definiującą wspólną metodę `draw(data)`.  
   - Dla każdej biblioteki (**Matplotlib, Seaborn, Plotly**) istnieją osobne klasy wykresów:
     `PointsPlot`, `PointDiffPlot`, `AvgHomeAwayPlot`, `TopBottomPlot`.  
   - Dzięki temu aplikacja umożliwia wybór biblioteki wizualizacji w interfejsie,
     przy zachowaniu wspólnego interfejsu i tej samej logiki danych.
                
6. **`app.py` - interfejs użytkownika**  
   - Odpowiada za strukturę aplikacji: menu, układ stron, prezentację tabel i wykresów oraz uruchamianie testów jednostkowych
     wraz z czytelnym podsumowaniem wyników.

7. **`main.py` - uruchamianie aplikacji**  
   - Plik startowy wywołujący aplikację poleceniem: `streamlit run app.py`.

8. **`test_analysis.py` oraz `test_fetcher.py` - testy jednostkowe**  
   - `test_analysis.py` weryfikuje poprawność obliczeń w `BasketAnalysis` na kontrolnym zbiorze danych.  
   - `test_fetcher.py` sprawdza poprawność parsowania HTML w `MatchDataFetcher`, z wykorzystaniem mockowania `requests.get`
     (testy nie wymagają połączenia z internetem).
""")

    st.subheader("Testy jednostkowe")
    st.markdown("""
W projekcie znajdują się dwa zestawy testów: dla modułu analizy danych oraz dla modułu pobierania danych.

### 1) `test_analysis.py` - testy modułu analitycznego (`BasketAnalysis`)
Ten plik sprawdza poprawność obliczeń wykonywanych na danych meczowych zapisanych w DataFrame:

- **`test_win_loss_ratio`** - czy bilans zwycięstw i porażek jest policzony poprawnie (liczba Wygrana i Porażka).
- **`test_avg_points_scored`** - czy średnia liczba punktów zdobytych jest wyliczana poprawnie.
- **`test_avg_points_conceded`** - czy średnia liczba punktów straconych jest wyliczana poprawnie.
- **`test_home_away_results`** - czy wyniki są poprawnie zliczane w podziale na U siebie / Na wyjeździe.
- **`test_avg_points_home_away`** - czy średnia liczba punktów zależnie od miejsca rozegrania meczu jest poprawna.
- **`test_win_loss_home_away`** - czy tabela przestawna (wygrane/porażki vs miejsce meczu) ma poprawne wartości.
- **`test_point_difference`** - czy różnica punktów w każdym meczu (`Punkty Basket Hills - Punkty przeciwnika`) jest poprawna.
- **`test_top_bottom_games`** - czy wybierane są poprawnie najlepsze i najsłabsze mecze pod względem zdobytych punktów.
- **`test_run_method`** - czy metoda `run()` zwraca komplet wyników oraz czy wybrane wartości są zgodne.

Wszystkie te testy działają na sztucznym, kontrolnym zestawie danych zdefiniowanym w `setUp()`,
dzięki czemu wyniki są powtarzalne i niezależne od aktualnych danych z internetu.

### 2) `test_fetcher.py` - testy modułu pobierania danych (`MatchDataFetcher`)
Ten plik sprawdza, czy parser HTML poprawnie tworzy rekordy meczów. Testy nie łączą się z internetem,
ponieważ wykorzystują mockowanie (`unittest.mock.patch`) funkcji `requests.get`:

- **`test_fetch_matches_parses_single_match_home`** - czy pojedynczy mecz, w którym Basket Hills jest po lewej stronie tabeli,
  zostaje poprawnie rozpoznany jako mecz u siebie, a punkty są przypisane właściwie.
- **`test_fetch_matches_parses_single_match_away`** - czy mecz, w którym Basket Hills jest po prawej stronie tabeli,
  zostaje poprawnie rozpoznany jako mecz na wyjeździe, z prawidłowym odwróceniem punktów.
- **`test_fetch_matches_skips_rows_without_team`** - czy wiersze, które nie dotyczą Basket Hills, są pomijane
  (czyli parser nie dodaje ich do listy wyników).



### Uruchamianie i prezentacja w aplikacji
Testy można uruchomić z poziomu zakładki **Testy jednostkowe**.
Aplikacja pokazuje podsumowanie (liczba testów, zaliczone/nieudane/błędy/pominięte) oraz szczegóły w rozwijanych sekcjach.
""")

    st.subheader("Zastosowane elementy programowania obiektowego")
    st.markdown("""
W projekcie wykorzystano następujące elementy programowania obiektowego:

- **Abstrakcję (klasy i metody abstrakcyjne)** - `SportsTeam` oraz `BasePlot` definiują minimalny interfejs,
  który musi zostać zaimplementowany w klasach pochodnych (np. `get_matches()`, `draw()`).
  Dzięki temu pozostałe części aplikacji mogą korzystać z obiektów w ujednolicony sposób.

- **Dziedziczenie** - `BasketballTeam` dziedziczy po `SportsTeam`, a klasy wykresów (`PointsPlot`, `PointDiffPlot`,
  `AvgHomeAwayPlot`, `TopBottomPlot`) dziedziczą po `BasePlot`. Pozwala to współdzielić wspólne elementy
  (np. atrybut `title`) oraz zapewnia spójną strukturę klas.

- **Polimorfizm** - różne klasy wykresów udostępniają tę samą metodę `draw(data)`, ale realizują ją inaczej
  (inne typy wizualizacji). W praktyce aplikacja wywołuje wykresy w jednakowy sposób, niezależnie od konkretnej klasy.

- **Enkapsulację (zamknięcie stanu i operacji w obiektach)** - dane oraz logika są skupione w klasach zgodnie z ich rolą:
  `MatchDataFetcher` przechowuje m.in. `url`, `team_name` i `download_time` oraz odpowiada za pobranie i wstępne przygotowanie danych,
  `BasketballTeam` przechowuje dane drużyny i listę meczów,
  a `BasketAnalysis` utrzymuje DataFrame i wykonuje obliczenia statystyczne.
  Inne moduły korzystają z tych informacji przez metody, zamiast operować bezpośrednio na „surowych” strukturach.

- **Dekorator** - `log_call` pełni rolę narzędzia pomocniczego : mierzy czas wykonania pobrania HTML
  i zapisuje wynik w `download_time`, bez mieszania tej funkcjonalności z właściwą logiką parsowania danych.
""")

elif menu == "Analiza drużyny":

    st.info(f"Czas pobierania danych ze strony: {download_time:.3f} s")

    st.header("Pytania badawcze i odpowiedzi")

    st.subheader("1. Jaki jest bilans zwycięstw i porażek drużyny?")
    df1 = results["wins_losses"].reset_index()
    df1.columns = ["Wynik meczu", "Ilość"]
    st.dataframe(df1, width=300, hide_index=True)

    st.subheader("2. Ile średnio punktów drużyna zdobywa i traci na mecz?")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Średnia liczba punktów zdobytych", results["avg_scored"])
    with col2:
        st.metric("Średnia liczba punktów straconych", results["avg_conceded"])

    st.subheader("3. Jak wyglądały wyniki w kolejnych meczach?")
    st.dataframe(results["df"], width="stretch")

    st.subheader("4. Czy drużyna osiąga lepsze wyniki u siebie czy na wyjeździe?")
    df4 = results["home_away"].reset_index()
    df4.columns = ["Miejsce meczu", "Wynik meczu", "Ilość"]
    st.dataframe(df4, width=400, hide_index=True)

    st.subheader("5. Jakie były najdłuższe serie zwycięstw i porażek?")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Najdłuższa seria wygranych", results["longest_win_streak"])
    with col2:
        st.metric("Najdłuższa seria porażek", results["longest_loss_streak"])

elif menu == "Wykresy":
    st.header("Wizualizacja danych")

    library = st.radio(
        "Wybierz bibliotekę wykresów:",
        ["Matplotlib", "Seaborn", "Plotly"],
        index = 2,
        horizontal=True
    )

    if library == "Matplotlib":
        plots = [
            ("1. Trend punktów zdobytych i straconych w sezonie",
             PointsPlotMatplotlib("Punkty Basket Hills i przeciwników w kolejnych meczach"),
             results["df"]),
            ("2. Różnica punktowa w kolejnych meczach",
             PointDiffPlotMatplotlib("Różnica punktów w sezonie"),
             results["point_diff"]),
            ("3. Średnia liczba punktów: u siebie vs na wyjeździe",
             AvgHomeAwayPlotMatplotlib("Średnia punktów: dom vs wyjazd"),
             results["avg_home_away"]),
            ("4. Najlepsze i najsłabsze mecze punktowo",
             TopBottomPlotMatplotlib("Najwyższe i najniższe zdobycze punktowe"),
             {"top": results["top_games"], "bottom": results["bottom_games"]}),
        ]

    elif library == "Seaborn":
        plots = [
            ("1. Trend punktów zdobytych i straconych w sezonie",
             PointsPlotSeaborn("Punkty Basket Hills i przeciwników w kolejnych meczach"),
             results["df"]),
            ("2. Różnica punktowa w kolejnych meczach",
             PointDiffPlotSeaborn("Różnica punktów w sezonie"),
             results["point_diff"]),
            ("3. Średnia liczba punktów: u siebie vs na wyjeździe",
             AvgHomeAwayPlotSeaborn("Średnia punktów: dom vs wyjazd"),
             results["avg_home_away"]),
            ("4. Najlepsze i najsłabsze mecze punktowo",
             TopBottomPlotSeaborn("Najwyższe i najniższe zdobycze punktowe"),
             {"top": results["top_games"], "bottom": results["bottom_games"]}),
        ]

    else:  # Plotly
        plots = [
            ("1. Trend punktów zdobytych i straconych w sezonie",
             PointsPlotPlotly("Punkty Basket Hills i przeciwników w kolejnych meczach"),
             results["df"]),
            ("2. Różnica punktowa w kolejnych meczach",
             PointDiffPlotPlotly("Różnica punktów w sezonie"),
             results["point_diff"]),
            ("3. Średnia liczba punktów: u siebie vs na wyjeździe",
             AvgHomeAwayPlotPlotly("Średnia punktów: dom vs wyjazd"),
             results["avg_home_away"]),
            ("4. Najlepsze i najsłabsze mecze punktowo",
             TopBottomPlotPlotly("Najwyższe i najniższe zdobycze punktowe"),
             {"top": results["top_games"], "bottom": results["bottom_games"]}),
        ]

    for header, plot_obj, data in plots:
        st.subheader(header)
        plot_obj.draw(data)

elif menu == "Testy jednostkowe":

    st.header("Testy jednostkowe")
    st.markdown("Kliknij przycisk, aby uruchomić testy jednostkowe.")

    def run_tests():
        logging.disable(logging.INFO)  

        start = time.perf_counter()
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=".", pattern="test_*.py")  

        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        result = runner.run(suite)

        elapsed = time.perf_counter() - start
        output = stream.getvalue()

        logging.disable(logging.NOTSET)  
        return result, elapsed, output

    if st.button("Uruchom testy"):
        result, elapsed, output = run_tests()

        total = result.testsRun
        failed = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Łącznie", total)
        c2.metric("Zaliczone", total - failed - errors - skipped)
        c3.metric("Nieudane", failed)
        c4.metric("Błędy", errors)
        c5.metric("Pominięte", skipped)

        st.caption(f"Czas wykonania: {elapsed:.3f} s")

        if failed == 0 and errors == 0:
            st.success("Wszystkie testy zakończone sukcesem")
        else:
            st.error("Część testów nie przeszła pomyślnie")

        if result.failures:
            with st.expander("Nieudane (kliknij, aby zobaczyć)"):
                for test, traceback in result.failures:
                    st.markdown(f"**{test}**")
                    st.code(traceback)

        if result.errors:
            with st.expander("Błędy (kliknij, aby zobaczyć)"):
                for test, traceback in result.errors:
                    st.markdown(f"**{test}**")
                    st.code(traceback)

        with st.expander("Pełny log z testów"):
            st.code(output)
    