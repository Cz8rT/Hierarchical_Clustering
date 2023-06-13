import numpy as np


# Funkcja wyznaczająca liczebność najmniejszej grupy
def liczebnosc_najmniejszej_grupy(lista):
    najmniejsza = len(lista)
    for grupa in lista:
        if (len(grupa) < najmniejsza):
            najmniejsza = len(grupa)
    return najmniejsza


def srodek_grupy(grupa):  # Funkcja wyznaczająca środek ciężkości grupy
    liczebnosc = len(grupa)
    srodek = [0, 0]
    for probka in grupa:
        srodek[0] += probka[0]
        srodek[1] += probka[1]
    # Wyliczenie średniej arytmetycznej
    srodek[0] = srodek[0] / liczebnosc
    srodek[1] = srodek[1] / liczebnosc
    return srodek


# Funkcja licząca dystans między 2 grupami lub 2 próbkami
def dystans_miedzy(srodek_grupy_1, srodek_grupy_2):
    # Odległość euklidesowa
    dystans = np.sqrt(
        ((srodek_grupy_1[0]-srodek_grupy_2[0])**2 + (srodek_grupy_1[1]-srodek_grupy_2[1])**2))
    return dystans


# Funkcja licząca maksymalne rozproszenie między próbkami w grupie
def maksymalne_rozproszenie_w_grupie(grupa):
    max_rozproszenie = 0
    # Porównanie każdej z każdą
    # indeks i kończy się na przedostatnim indeksie
    for i in range(len(grupa)-1):
        # By nie porównywać 2 razy tych samych próbek
        # indeks j zaczyna się od i + 1
        for j in range(i + 1,  len(grupa)):
            rozproszenie = dystans_miedzy(grupa[i], grupa[j])
            if (rozproszenie > max_rozproszenie):
                max_rozproszenie = rozproszenie
    return max_rozproszenie


# Funkcja licząca maksymalne odchylenie standardowe między atrybutami w grupie
def maksymalne_odchylenie_standardowe(grupa):
    if (len(grupa) == 1):
        return [0, 0]
    srednia_x = 0
    srednia_y = 0
    for i in range(len(grupa)):
        srednia_x += grupa[i][0]
        srednia_y += grupa[i][1]
    srednia_x = srednia_x/len(grupa)
    srednia_y = srednia_y/len(grupa)
    suma_x = 0
    suma_y = 0
    for i in range(len(grupa)):
        suma_x += (grupa[i][0] - srednia_x)**2
        suma_y += (grupa[i][1] - srednia_y)**2
    suma_x = np.sqrt(suma_x/(len(grupa)-1))
    suma_y = np.sqrt(suma_y/(len(grupa)-1))
    return [suma_x, suma_y]
