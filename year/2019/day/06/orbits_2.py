from operator import methodcaller
from readers import FileReader


COM = "COM"
YOU = "YOU"
SAN = "SAN"


def main():
    raw_orbits = list(map(methodcaller("split", ")"), map(str.strip, FileReader.read_input_as_list())))
    orbits = {o[1]: o[0] for o in raw_orbits}

    you_planets = set_of_planets_to_home(YOU, orbits, set())
    santa_planets = set_of_planets_to_home(SAN, orbits, set())

    print(f"Total number jumps to santa: {len(you_planets ^ santa_planets) - 2}")


def set_of_planets_to_home(planet, orbits, planets):
    if planet in orbits:
        planets.add(planet)
        if orbits[planet] == COM:
            print(f"{len(planets)} planets to home")
            return planets
        return set_of_planets_to_home(orbits[planet], orbits, planets)
    print(f"This is odd, did not expect to get here! Processing: {planet}")
    return planets


if __name__ == "__main__":
    main()
