class Humanity:
    def __init__(self, name, population, language):
        self.name = name
        self._population = population
        self.language = language

    def show_info(self):
        return f"{self.name}: population {self._population}, language: {self.language}"

    def communicate(self):
        return f"{self.name} communicates using {self.language}"

    def increase_population(self, amount):
        if amount > 0:
            self._population += amount

    def get_population(self):
        return self._population


class Nation(Humanity):
    def __init__(self, name, population, language, country, capital):
        super().__init__(name, population, language)
        self.country = country
        self.__capital = capital

    def show_info(self):
        return (
            f"Nation: {self.name}, country: {self.country}, "
            f"capital: {self.__capital}, population: {self.get_population()}, "
            f"language: {self.language}"
        )

    def communicate(self):
        return f"{self.name} use {self.language} in {self.country}"

    def get_capital(self):
        return self.__capital

    def set_capital(self, new_capital):
        if new_capital:
            self.__capital = new_capital


if __name__ == "__main__":
    ukrainians = Nation("Ukrainians", 40000000, "Ukrainian", "Ukraine", "Kyiv")

    print(ukrainians.show_info())
    print(ukrainians.communicate())

    ukrainians.increase_population(100000)
    ukrainians.set_capital("Kyiv")

    print("Population:", ukrainians.get_population())
    print("Capital:", ukrainians.get_capital())
