FROM python:3.10-slim
WORKDIR /app
RUN pip install flask requests

COPY . .

EXPOSE 8080

ENTRYPOINT ["python", "antares.py", "--mode", "server", "--set-port", "8080"]