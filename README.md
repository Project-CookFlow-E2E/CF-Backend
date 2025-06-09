# CookFlow Backend

This is the backend for the CookFlow project, powered by Django and PostgreSQL.

## 🚀 Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the repository

`git clone https://github.com/Final-Project-CookFlow/cookflow-backend.git`
`cd cookflow-backend`

### 2. Create a virtual environment

`python -m venv venv`

3. Activate the virtual environment
   On macOS/Linux:
   `source venv/bin/activate`
   On Windows:
   `source venv/Scripts/activate`
   On Windows PowerShell:
   `.\venv\Scripts\Activate.ps1`

4. Install dependencies

`pip install -r requirements.txt`

### 3. 🛠️ Database Setup (PostgreSQL)

1. Create a new database.
   Create a new database named cookflow_db in your PostgreSQL.

2. Create a new role/user.
   Name: admin
   Password: admin
   Under Privileges, select all available options
   Save the new role

3. Run migrations.
   `python manage.py makemigrations`
   `python manage.py migrate`

## Alternative way Database Setup (PostgreSQL)

1. Access PostgreSQL as superuser (adjust psql command if needed).
   `psql -U postgres -h localhost`

2. Inside psql shell, run these commands (replace with your password if desired):

**PostgreSQL setup:**

```sql
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE cookflow_db OWNER admin;
GRANT ALL PRIVILEGES ON DATABASE cookflow_db TO admin;
\c cookflow_db;
GRANT USAGE ON SCHEMA public TO admin;
GRANT CREATE ON SCHEMA public TO admin;
\q
```

**PowerShell env variables:**

```powershell
$env:DJANGO_DB_USER="admin"
$env:DJANGO_DB_PASSWORD="admin"
$env:DJANGO_DB_NAME="cookflow_db"
$env:DJANGO_DB_HOST="localhost"
$env:DJANGO_DB_PORT="5432"
```

3. Run Django migrations

`python manage.py migrate`
