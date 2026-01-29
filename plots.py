import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import streamlit as st
from abc import ABC, abstractmethod


# Polimorfizm: każda klasa wykresu ma tę samą metodę draw(),
# ale inną implementację
# klasa abstrakcyjna - narzuca wspólny interfejs dla wszystkich wykresów
class BasePlot(ABC):
    def __init__(self, title: str):
        self.title = title  # atrybut wspólny dla wszystkich wykresów

    @abstractmethod
    def draw(self, data):  # metoda abstrakcyjna do implementacji w klasach dziedziczących
        pass


# MATPLOTLIB

# dziedziczenie - PointsPlotMatplotlib dziedziczy po BasePlot
class PointsPlotMatplotlib(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        x = range(len(df))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, df["Punkty Basket Hills"], marker="o",
                label="Basket Hills", color="darkred")
        ax.plot(x, df["Punkty przeciwnika"], marker="o",
                label="Przeciwnik", color="black")

        ax.set_xticks(x)
        ax.set_xticklabels(df["Data"], rotation=90, fontsize=8)

        ax.set_title(self.title)
        ax.set_ylabel("Punkty")
        ax.set_xlabel("Data")
        ax.legend()
        st.pyplot(fig)


# dziedziczenie - PointDiffPlotMatplotlib dziedziczy po BasePlot
class PointDiffPlotMatplotlib(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        x = range(len(df))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, df["Różnica punktów"], marker="o", color="#800020")
        ax.axhline(0, linestyle="--", color="gray")

        ax.set_xticks(x)
        ax.set_xticklabels(df["Data"], rotation=90, fontsize=8)

        ax.set_title(self.title)
        ax.set_ylabel("Różnica punktów")
        ax.set_xlabel("Data")
        st.pyplot(fig)


# dziedziczenie - AvgHomeAwayPlotMatplotlib dziedziczy po BasePlot
class AvgHomeAwayPlotMatplotlib(BasePlot):
    def draw(self, data):
        series = data
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(series.index, series.values, color="darkred")

        ax.set_title(self.title)
        ax.set_ylabel("Średnia liczba punktów")
        ax.set_xlabel("Miejsce meczu")
        ax.tick_params(axis="x", rotation=0)
        st.pyplot(fig)


# dziedziczenie - TopBottomPlotMatplotlib dziedziczy po BasePlot
class TopBottomPlotMatplotlib(BasePlot):
    def draw(self, data):
        top_df = data["top"]
        bottom_df = data["bottom"]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(top_df["Przeciwnik"], top_df["Punkty Basket Hills"],
               label="Najlepsze mecze", color="darkred")
        ax.bar(bottom_df["Przeciwnik"], bottom_df["Punkty Basket Hills"],
               label="Najsłabsze mecze", color="black")

        ax.set_title(self.title)
        ax.set_ylabel("Punkty")
        ax.set_xlabel("Przeciwnik")
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=90, labelsize=8)
        st.pyplot(fig)


# SEABORN

# dziedziczenie - PointsPlotSeaborn dziedziczy po BasePlot
class PointsPlotSeaborn(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df, x="Data", y="Punkty Basket Hills",
                     marker="o", label="Basket Hills", color="darkred", ax=ax)
        sns.lineplot(data=df, x="Data", y="Punkty przeciwnika",
                     marker="o", label="Przeciwnik", color="black", ax=ax)

        ax.set_title(self.title)
        ax.set_ylabel("Punkty")
        ax.set_xlabel("Data")
        ax.tick_params(axis="x", rotation=90, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        st.pyplot(fig)


# dziedziczenie - PointDiffPlotSeaborn dziedziczy po BasePlot
class PointDiffPlotSeaborn(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df, x="Data", y="Różnica punktów",
                     marker="o", color="#800020", ax=ax)
        ax.axhline(0, linestyle="--", color="gray")

        ax.set_title(self.title)
        ax.set_ylabel("Różnica punktów")
        ax.set_xlabel("Data")
        ax.tick_params(axis="x", rotation=90, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        st.pyplot(fig)


# dziedziczenie - AvgHomeAwayPlotSeaborn dziedziczy po BasePlot
class AvgHomeAwayPlotSeaborn(BasePlot):
    def draw(self, data):
        series = data
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=series.index, y=series.values, color="darkred", ax=ax)

        ax.set_title(self.title)
        ax.set_ylabel("Średnia liczba punktów")
        ax.set_xlabel("Miejsce meczu")
        ax.tick_params(axis="x", rotation=0)
        st.pyplot(fig)


# dziedziczenie - TopBottomPlotSeaborn dziedziczy po BasePlot
class TopBottomPlotSeaborn(BasePlot):
    def draw(self, data):
        top_df = data["top"]
        bottom_df = data["bottom"]

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=top_df, x="Przeciwnik", y="Punkty Basket Hills",
                    color="darkred", label="Najlepsze mecze", ax=ax)
        sns.barplot(data=bottom_df, x="Przeciwnik", y="Punkty Basket Hills",
                    color="black", label="Najsłabsze mecze", ax=ax)

        ax.set_title(self.title)
        ax.set_ylabel("Punkty")
        ax.set_xlabel("Przeciwnik")
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=90, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        st.pyplot(fig)


# PLOTLY

# dziedziczenie - PointsPlotPlotly dziedziczy po BasePlot
class PointsPlotPlotly(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        fig = px.line(
            df,
            x="Data",
            y=["Punkty Basket Hills", "Punkty przeciwnika"],
            markers=True,
            title=self.title,
            color_discrete_map={
                "Punkty Basket Hills": "darkred",
                "Punkty przeciwnika": "black",
            },
        )
        fig.update_layout(xaxis_title="Data", yaxis_title="Punkty")
        fig.update_xaxes(tickangle=90)
        st.plotly_chart(fig, use_container_width=True)


# dziedziczenie - PointDiffPlotPlotly dziedziczy po BasePlot
class PointDiffPlotPlotly(BasePlot):
    def draw(self, data):
        df = data.copy()
        df["Data"] = df["Data i godzina meczu"].dt.date

        fig = px.line(
            df,
            x="Data",
            y="Różnica punktów",
            markers=True,
            title=self.title,
            color_discrete_sequence=["#800020"],
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.update_layout(xaxis_title="Data", yaxis_title="Różnica punktów")
        fig.update_xaxes(tickangle=90)
        st.plotly_chart(fig, use_container_width=True)


# dziedziczenie - AvgHomeAwayPlotPlotly dziedziczy po BasePlot
class AvgHomeAwayPlotPlotly(BasePlot):
    def draw(self, data):
        series = data.reset_index()
        fig = px.bar(
            series,
            x=series.columns[0],
            y=series.columns[1],
            title=self.title,
            color_discrete_sequence=["darkred"],
        )
        fig.update_layout(
            xaxis_title="Miejsce meczu",
            yaxis_title="Średnia liczba punktów",
        )
        st.plotly_chart(fig, use_container_width=True)


# dziedziczenie - TopBottomPlotPlotly dziedziczy po BasePlot
class TopBottomPlotPlotly(BasePlot):
    def draw(self, data):
        top_df = data["top"].copy()
        bottom_df = data["bottom"].copy()

        top_df["Typ"] = "Najlepsze mecze"
        bottom_df["Typ"] = "Najsłabsze mecze"
        combined = pd.concat([top_df, bottom_df])

        fig = px.bar(
            combined,
            x="Przeciwnik",
            y="Punkty Basket Hills",
            color="Typ",
            title=self.title,
            color_discrete_map={
                "Najlepsze mecze": "darkred",
                "Najsłabsze mecze": "black",
            },
        )
        fig.update_xaxes(tickangle=90)
        fig.update_layout(xaxis_title="Przeciwnik", yaxis_title="Punkty")
        st.plotly_chart(fig, use_container_width=True)