FROM python:3.10-slim
WORKDIR /app
RUN pip install flask requests
# Copiem tot proiectul în container
COPY . .
# Expunem portul default
EXPOSE 8080
# Rulăm direct prin antares.py pentru a păstra consistența
ENTRYPOINT ["python", "antares.py", "--mode", "server", "--set-port", "8080"]