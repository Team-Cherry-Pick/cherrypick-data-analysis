FROM python:3.13
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-root

ENV PYTHONPATH=/app/src
EXPOSE 8000

# 실행 명령 (main.py 기준)
CMD ["poetry", "run", "python", "src/cherrypick_recommender/main.py"]






