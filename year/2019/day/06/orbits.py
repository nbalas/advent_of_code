from operator import methodcaller
from readers import FileReader


COM = "COM"


def main():
    raw_orbits = list(map(methodcaller("split", ")"), map(str.strip, FileReader.read_input_as_list())))
    orbits = {o[1]: o[0] for o in raw_orbits}

    total_orbits = 0
    for planet in orbits.keys():
        print(f"Getting count of orbits for planet {planet}")
        total_orbits += count_total_path_home(planet, orbits)

    print(f"Total number of orbits: {total_orbits}")


def count_total_path_home(planet, orbits, count=0):
    if planet in orbits:
        count += 1
        if orbits[planet] == COM:
            print(f"{count} orbits for this planet")
            return count
        return count_total_path_home(orbits[planet], orbits, count)
    print(f"This is odd, did not expect to get here! Processing: {planet}")
    return count


if __name__ == "__main__":
    main()
