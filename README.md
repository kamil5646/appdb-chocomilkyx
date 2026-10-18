# Zbiorcze repo dla appdb

Adres do dodania jako repo AltStore w appdb:

https://raw.githubusercontent.com/kamil5646/appdb-chocomilkyx/main/repo.json

Katalog scala źródła wymienione w [chocomilkyX](https://github.com/gablilli/chocomilkyX/blob/main/static/global-repos.json). Aktualizacja jest zaplanowana co 6 godzin oraz dostępna ręcznie w GitHub Actions.

`status.json` zawiera czas aktualizacji, liczbę aplikacji i błędy poszczególnych źródeł. Niedostępne źródła są pomijane podczas danej aktualizacji. Dla powtarzających się identyfikatorów aplikacji wygrywa pierwsze źródło zgodnie z kolejnością listy. Linki IPA prowadzą bezpośrednio do zewnętrznych dostawców; pliki aplikacji nie są przechowywane w tym repozytorium. Katalog nie oznacza weryfikacji bezpieczeństwa ani zgodności aplikacji z urządzeniem.

## Odtworzenie

Python 3, bez dodatkowych zależności:

```sh
python3 scripts/update.py
```
