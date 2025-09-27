# Dockerfile
FROM python:3.12-slim

# Imposta la directory di lavoro
WORKDIR /app

# Aggiorna pip e installa dipendenze di sistema
RUN pip install --upgrade pip

# Copia i file requirements.txt e installa dipendenze
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia il progetto Django
COPY . .

# Espone la porta di sviluppo
EXPOSE 8000

# Comando di default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
