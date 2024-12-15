# Login API
Dette repository indeholder en Flask-baseret Login API, der bruger JWT (JSON Web Tokens) til at autentificere brugere. API'en giver mulighed for at registrere og logge ind på en brugerkonto, samt leverer adgangstokens til autoriserede brugere.

## Kom godt i gang
Følg disse trin for at få en kopi af projektet op at køre på din lokale maskine til udviklings- og testformål.

## Installation
Klon dette repository til din lokale maskine:

```bash
git clone <repository_url>
cd <repository_folder>
``

Installer de nødvendige Python-pakker:
```bash
pip install flask flask-jwt-extended python-dotenv
```

Initialiser databasen ved at oprette følgende tabel i SQLite:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

Start applikationen:

```bash
python app.py
```

## API Endpoints
### 1. Registrer en bruger
- **URL:** `/register`
- **Method:** `POST`
- **Request Body:** JSON

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **Response:**
**201 Created:** Bruger registreret succesfuldt
**400 Bad Request:** Manglende eller ugyldige data
  
## 2. Login
- **URL:** `/login`
- **Method:** `POST`
- **Request Body:** JSON

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **Response:****
**200 OK:** Returnerer en JWT token til autorisation

```json
Kopier kode
{
  "access_token": "<JWT_TOKEN>"
}
```

**400 Bad Request:** Manglende eller ugyldige data
**401 Unauthorized:** Ugyldigt brugernavn eller password

## 3. Home (Test Endpoint)
- **URL:** `/`
- **Method:** `GET`
- **Response:**

**200 OK:** Viser en simpel velkomstbesked

Welcome to the Login API. Use `/register` or `/login`for functionality.

### Konfiguration
- **Miljøvariabler:**
API'en bruger en .env-fil til at gemme den hemmelige nøgle til JWT-signering. Filen skal have følgende format:
```bash
KEY=din_hemmelige_nøgle
```

### Bemærkninger
**JWT Token Udløb:** Tokens er konfigureret til aldrig at udløbe i denne prototype, men dette bør ændres for sikkerhedsformål i produktionsbrug.
**Database:** API'en bruger en SQLite-database (user_database.db). I produktionsbrug anbefales en mere robust løsning.
**Sikkerhed:** Passwords gemmes som ren tekst i denne prototype. Dette skal erstattes med hash-metoder som bcrypt i produktion.

Licens
MIT License

