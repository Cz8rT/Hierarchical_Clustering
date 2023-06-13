import numpy as np
import matplotlib.pyplot as plt
# Import funkcji pomocniczych zdefiniowanych dla algorytmu w pliku funkcje.py
from funkcje import *

# pobranie danych z pliku '.txt'
spirala_data = open('./data/spirala.txt', "r")
dane = spirala_data.read().split("\n")
spirala_data.close()

# Lista przechowująca próbki
probki_lista = []

# Konwersja i przeformatowanie poszczególnych linii danych
for wiersz in dane:
    linijka = wiersz.split()
    lista_float = []
    # Zamiana stringów na floaty
    for element in linijka:
        lista_float.append(float(element))
    # Lista zawierająca 2-elementowe listy (opisujące próbkę)
    probki_lista.append(lista_float)

# Algorytm grupowania hierarchicznego
# Na początku definiujemy tyle grup ile jest osobników
# Każdy osobnik tworzy swoją grupę
grupy_lista = []
for probka in probki_lista:
    # Dodanie do listy kolejnego wymiaru listy reprezentującego grupę
    # Każda grupa jest listą zawierającą listy opisujące jedną próbkę
    grupy_lista.append([probka])


# zmienna boolowska do sprawdzenia czy zakończyć działanie pętli algorytmu
STOP = False

# Zapisanie początkowych danych do określenia warunków zakończenia algorytmu
liczba_grup = len(grupy_lista)
cala_populacja = len(probki_lista)

# Definiujemy warunki zakończenia (STOP)
# Osiągnięcie minimalnej liczby grup
minimum_grup = 3
# Osiągnięcie maksymalnej liczebności jednej grupy
maksymalna_liczebnosc_grupy = round(0.4*cala_populacja)
# Osiągnięcie określonej liczebności przez najmniejszą grupę
najmniejsza_grupa_populacja = round(0.2*cala_populacja)
# Osiągnięto maksymalne rozproszenie w jednej grupie (oddalenie próbek)
maksymalne_rozproszenie = 2.5
# Osiągnięto maksymalne odchylenie standardowe dla atrybutów
maks_odchy_st = 1.5

# Uruchamiamy pętlę algorytmu
while (not STOP):
    # znajdujemy 2 grupy najbliżej siebie

    # zmienne przechowujące indeksy grup najbliższych sobie
    # oraz dystans między nimi
    indeks_grupy_1 = -1
    indeks_grupy_2 = -1
    najmniejszy_dystans = np.inf  # na początku jest nieskończony
    for i in range(len(grupy_lista)-1):
        for j in range(i + 1,  len(grupy_lista)):
            dystans = dystans_miedzy(srodek_grupy(
                grupy_lista[i]), srodek_grupy(grupy_lista[j]))
            if (dystans < najmniejszy_dystans):
                najmniejszy_dystans = dystans
                indeks_grupy_1 = i
                indeks_grupy_2 = j

    # Sprawdzenie poprawności odnalezienia najbliższych grup
    # Wyjście z algorytmu w razie błędu
    if (indeks_grupy_1 == -1 or indeks_grupy_2 == -1 or najmniejszy_dystans == np.inf):
        print("BŁĄD!!! - Nie znaleziono najbliższych grup!")
        break

    # Połączenie najbliższych grup w jedną i usunięcie zbędnej
    grupy_lista[indeks_grupy_1] += grupy_lista[indeks_grupy_2]
    grupy_lista.pop(indeks_grupy_2)

    # Sprawdzenie czy doszło do spełnienia jakiegoś warunku zakończenia (STOP)
    # !!! Sprawdzam każdy warunek oddzielnie, by całość była bardziej przejrzysta !!!
    # !!! ale odbywa się to kosztem wydajności algorytmu !!!
    # Sprawdzenie minimalnej liczby grup
    if (len(grupy_lista) <= minimum_grup):
        print("Osiągnięto minimalną liczbę grup: ", minimum_grup)
        print("STOP!")
        STOP = True
    # Sprawdzenie maksymalnej liczebności jednej grupy
    for grupa in grupy_lista:
        liczebnosc_grupy = len(grupa)
        if (liczebnosc_grupy >= maksymalna_liczebnosc_grupy):
            print("Osiągnięto maksymalną liczebność jednej grupy: ", liczebnosc_grupy)
            print("STOP!")
            STOP = True
    # Sprawdzenie określonej liczebności przez najmniejszą grupę
    liczebnosc = liczebnosc_najmniejszej_grupy(grupy_lista)
    if (liczebnosc >= najmniejsza_grupa_populacja):
        print("Osiągnięto maksymalną liczebność najmniejszej grupy: ", liczebnosc)
        print("STOP!")
        STOP = True
    # Sprawdzenie maksymalnego rozproszenia w jednej grupie
    for grupa in grupy_lista:
        rozproszenie = maksymalne_rozproszenie_w_grupie(grupa)
        if (rozproszenie >= maksymalne_rozproszenie):
            print("Osiągnięto maksymalne rozproszenie w grupie: ", rozproszenie)
            print("STOP!")
            STOP = True
    # Sprawdzenie maksymalnego odchylenia standardowego dla atrybutów
    for grupa in grupy_lista:
        odchylenie = maksymalne_odchylenie_standardowe(grupa)
        if (odchylenie[0] >= maks_odchy_st or odchylenie[1] >= maks_odchy_st):
            print(
                "Osiągnięto maksymalne odchylenie standardowe jednego z atrybutów w grupie: ", odchylenie)
            print("STOP!")
            STOP = True

    # Wypisanie końcowych statystyk algorytmu
    if (STOP):
        print("Otrzymany podział grup:")
        for i in range(len(grupy_lista)):
            print("Grupa {}:\n{}".format(i+1, grupy_lista[i]))
            print("*************************************************************")


# *******************************************************************************
# Rysowanie wykresu
# *******************************************************************************
for grupa in grupy_lista:
    x = []
    y = []
    for probka in grupa:
        x.append(probka[0])
        y.append(probka[1])
    plt.scatter(x, y)

plt.show()
