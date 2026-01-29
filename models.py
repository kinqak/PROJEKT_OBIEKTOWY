from abc import ABC, abstractmethod

# klasa abstrakcyjna - wspólny interfejs dla wszystkich drużyn sportowych
class SportsTeam(ABC):
    def __init__(self, name):
        self.name = name

    # metoda abstrakcyjna nazwy drużyny
    @abstractmethod
    def get_name(self):
        pass

    # metoda abstrakcyjna pobierania meczów drużyny
    @abstractmethod
    def get_matches(self):
        pass

# dziedziczenie - BasketballTeam dziedziczy po SportsTeam
class BasketballTeam(SportsTeam):
    def __init__(self, name, matches):
        super().__init__(name)
        self.matches = matches

    def get_name(self):
        return self.name

    def get_matches(self):
        return self.matches