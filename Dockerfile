FROM python:3.9-slim

RUN pip install flask requests


WORKDIR /app

COPY antares_c2.py .


EXPOSE 8080


ENTRYPOINT ["python", "antares_c2.py"]