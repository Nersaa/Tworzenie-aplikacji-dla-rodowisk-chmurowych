System Zarządzania Biblioteką

---

## Temat projektu

Webowa aplikacja do zarządzania biblioteką (system zarządzania książkami, autorami, użytkownikami oraz recenzjami), uruchamiana w środowisku kontenerowym przy pomocy `docker compose up`.

## Autorzy / Uczestnicy

- **Autor**: Mykyta Kostiukov  
- **Numer indeksu**: 50745


## Wprowadzenie

Projekt przedstawia prosty system zarządzania biblioteką, napisany w Pythonie z użyciem frameworka Flask.  
System umożliwia zarządzanie książkami, autorami, osobami wypożyczającymi, recenzjami oraz śledzenie wypożyczeń.  
Architektura projektu opiera się na wzorcu Model-View-Controller (MVC), co zapewnia przejrzystość i łatwość rozbudowy.

## Zaimplementowane funkcjonalności

Minimum dwie kompletne funkcjonalności wymagane w zadaniu zostały spełnione (w praktyce jest ich więcej):

1. **Zarządzanie książkami (CRUD)**  
   - Dodawanie nowych książek (`/book/new`)  
   - Edytowanie istniejących książek (`/book/<id>/edit`)  
   - Usuwanie książek (`/book/<id>/delete`)  
   - Przeglądanie listy książek z poziomu strony głównej (`/`)

2. **System recenzji książek**  
   - Dodawanie recenzji z oceną (1–5 gwiazdek) i komentarzem (`/book/<id>/add_review`)  
   - Przypisanie recenzji do konkretnej osoby (osoby zakładane automatycznie)  
   - Wyświetlanie recenzji na stronie szczegółów książki (`/book/<id>`)

3. **Dodatkowe funkcjonalności **  
   - **Wyszukiwanie książek** po tytule i autorze (pole wyszukiwania na stronie głównej)  
   - **Zarządzanie autorami** – autor tworzy się automatycznie przy dodawaniu książki z nowym autorem  
   - **Zarządzanie osobami** – osoby (czytelnicy/recenzenci) tworzone są automatycznie przy dodawaniu recenzji lub wypożyczeniu  
   - **Śledzenie wypożyczeń** – przykładowe wypożyczenia dodawane są przez skrypt `add_test_data.py`

## Struktura projektu (MVC)

- **Model** – logika danych i interakcje z bazą danych (`app/models/`):
  - `Book`, `Author`, `Person`, `Borrowing`, `Review`
- **Controller** – obsługa żądań HTTP, logika biznesowa (`app/controllers/`):
  - `book_controller.py` – główny kontroler aplikacji
- **View** – szablony HTML (`app/templates/`) oraz statyczne pliki CSS/JS (`app/static/`).

Główne pliki:

- `config.py` – konfiguracja aplikacji (Flask + SQLAlchemy)
- `run.py` – uruchomienie aplikacji
- `init_db.py` – inicjalizacja bazy danych
- `add_test_data.py` – dodanie przykładowych danych
- `requirements.txt` – zależności projektu
- `docker-compose.yml` – konfiguracja środowiska kontenerowego
- `Dockerfile` – definicja obrazu aplikacji

## Technologie

- **Backend**: Flask (Python), Flask-SQLAlchemy, SQLAlchemy  
- **Baza danych**: PostgreSQL (w kontenerze Dockera, połączenie przez `DATABASE_URL`)  
- **Frontend**: Jinja2, Bootstrap 5  
- **Infrastruktura**: Docker, Docker Compose

## Instrukcje uruchomienia aplikacji 

Założenie z treści zadania: *całość aplikacji uruchamiana jest przy pomocy `docker compose up`*.

### Wymagania wstępne

- Zainstalowany **Docker** i **Docker Compose**

### Kroki uruchomienia

1. **Sklonuj repozytorium** (lub pobierz projekt):

   ```bash
   git clone <URL_do_repozytorium>
   cd Mvc-Project-master
   ```

2. **Zbuduj i uruchom środowisko** (aplikację + bazę danych PostgreSQL) przy pomocy Docker Compose:

   ```bash
   docker compose up --build
   ```

   - Kontener `db` (PostgreSQL) zostanie uruchomiony automatycznie.  
   - Kontener `web`:
     - Zainstaluje zależności z `requirements.txt`
     - Zainicjalizuje bazę danych (`python init_db.py`)
     - Doda przykładowe dane (`python add_test_data.py`)
     - Uruchomi aplikację Flask (`flask run --host=0.0.0.0`)

3. **Wejdź w przeglądarce** pod adres:

   - `http://127.0.0.1:5000/`

To wszystko – nie są potrzebne dodatkowe ręczne kroki (tworzenie wirtualnego środowiska, ręczne uruchamianie skryptów inicjalizujących itp.).  
Wszystko odbywa się automatycznie w kontenerach po wykonaniu `docker compose up`.

## Alternatywne uruchomienie (bez Dockera – opcjonalne)

Tylko w celach deweloperskich, można uruchomić aplikację lokalnie bez Dockera:

1. Utwórz i aktywuj wirtualne środowisko
2. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

3. Zainicjuj bazę danych i dodaj dane testowe:

   ```bash
   python init_db.py
   python add_test_data.py
   ```

4. Uruchom aplikację:

   ```bash
   python run.py
   ```

5. Otwórz przeglądarkę i przejdź pod adres:

   - `http://127.0.0.1:5000/`

