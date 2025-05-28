FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    wget curl gnupg2 unzip fonts-liberation \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxext6 libxi6 \
    libvulkan1 xdg-utils ca-certificates

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

ENV PYTHONPATH=/app/src
ENV CHROMIUM_PATH=/usr/bin/chromium

EXPOSE 8501

ENTRYPOINT ["poetry", "run", "python", "src/cherrypick_data_analysis/main.py"]
CMD ["serve", "1254308182"]
