FROM python:3.12

WORKDIR /fastapi_auth

COPY poetry.lock pyproject.toml ./

RUN poetry add pyproject.toml

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]