# Projekt o fałszywych korelacjach

#### Autorstwa Bogdana Rychlikowskiego i Macieja Bazeli

## Cel

> Korelacja nie oznacza przyczynowości

To zdanie kiedyś słyszeli wszyscy. Nie chcemy z nim polemizować, tylko pokazać kilka jaskrawych przykładów potwierdzających tę tezę.

## Skrypty

```fetcher.py``` - Skrypt pobierający dane z Banku Danych Lokalnych GUS. Dla optymalnego działania wymaga zarejestrowanego klucza API

	
```corelations.py```(sic!) - Skrypt przeszukujący pobrane dane pod kątem fałszywych korelacji. Kandydatów, tj. pary statystyk o dużym prawdopodobieństwie fałszywych korelacji, zapisuje do pliku ```pairs.txt``` w czymś na kształt formatu csv. Skrypt przyjmuje argumenty


- ```-i``` - Zbiór danych, w których szukamy korelacji
- ```-r, --range``` - Zakres lat, z których będziemy korzystać


```plotting.py``` - Tworzy wykresy wszystkich danych w dwóch wersjach: "zmanipulowanej" i "niezmanipulowanej". Zapisuje je do folderów odpowiednio ```results``` i ```real_results```. Dumne dziecko Macieja Bazeli.
