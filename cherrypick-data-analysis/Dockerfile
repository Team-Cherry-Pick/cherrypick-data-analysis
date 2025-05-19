FROM python:3.11-slim
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-root

ENV PYTHONPATH=/app/src
EXPOSE 8501

# 실행 명령 (main.py 기준)
ENTRYPOINT ["poetry", "run", "python", "src/cherrypick_data_analysis/main.py"]
CMD ["fmkorea"]






