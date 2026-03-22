# Tugas 2: Authentication & Authorization

### Kelas: PKPL C
### Nama Kelompok: PhiLia093

**Anggota Kelompok:**
- Nathanael Leander Herdanatra (2406421320)
- Raihana Nur Azizah (2406413426)
- Rochelle Marchia Arisandi (2406429014)
- Dibrienna Rauseuky (2406429834)
- Ardyana Feby Pratiwi (2406398274)

### Deployment Link
[https://nathanaeru.pythonanywhere.com/](https://nathanaeru.pythonanywhere.com/)

### How to Run the Project

1. Clone this repo.

2. Navigate to the project directory and create a virtual environment:

   **For Windows:**
   ```powershell
   python -m venv env
   ```

   **For Unix/Linux or MacOS:**
   ```bash
   python3 -m venv env
   ```
   
3. Activate the virtual environment:

   **For Windows:**
   ```powershell
    env\Scripts\activate
    ```
   
   **For Unix/Linux or MacOS:**
   ```bash
   source env/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Migrate the database:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
    python manage.py runserver
    ```
7. Open the localhost URL provided in the terminal (usually http://127.0.0.1:8000) in your web browser to see the application running.

### How to Set Up Google OAuth2 (Local & Production)

To enable Google Login, you need to configure the Google Cloud Console and Django Admin.

#### Step 1: Google Cloud Console Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
- Navigate to APIs & Services > OAuth consent screen.
  - Choose External and fill in the required app details (App name, support email, developer contact).
- Navigate to APIs & Services > Credentials.
  - Click Create Credentials > OAuth client ID.
  - Select Web application as the application type.
- Set up the Authorized JavaScript origins:
  - For local: `http://127.0.0.1:8000`
  - For production: `https://nathanaeru.pythonanywhere.com`
- Set up the Authorized redirect URIs:
  - For local: `http://127.0.0.1:8000/accounts/google/login/callback/`
  - For production: `https://nathanaeru.pythonanywhere.com/accounts/google/login/callback/`
- Click Create and save the generated Client ID and Client Secret.

#### Step 2: Django Admin Setup
- Create a superuser to access the Django admin:
  ```bash
  python manage.py createsuperuser
  ```
- Run the development server
  ```bash
  python manage.py runserver
  ```
- Log in to the admin panel at `http://127.0.0.1:8000/admin/`
- Go to Sites > Sites:
   - Edit the default `example.com` entry.
   - Change both Domain name and Display name to `127.0.0.1:8000 `(for local) or `nathanaeru.pythonanywhere.com` (for production). Do not include `http://` or trailing slashes.
- Go to Social Accounts > Social applications:
   - Click Add social application.
   - Provider: Choose Google.
   - Name: Enter `Google Login`.
   - Client id: Paste the Client ID from Google Cloud.
   - Secret key: Paste the Client Secret from Google Cloud.
   - Sites: Move your configured site (127.0.0.1:8000 or the production domain) from the "Available" box to the "Chosen" box.
   - Click Save.