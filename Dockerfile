FROM python:3.11

WORKDIR /auth

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]