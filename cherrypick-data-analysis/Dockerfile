FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치 (Chrome 실행을 위한 라이브러리 포함)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg2 unzip fonts-liberation \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxext6 libxi6 \
    libvulkan1 xdg-utils ca-certificates

# Chrome 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Poetry 설치
RUN pip install poetry

# Poetry 설정 및 프로젝트 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# 전체 프로젝트 복사
COPY . .

# 환경 변수 설정
ENV PYTHONPATH=/app/src

EXPOSE 8501

# 진입점(main.py), 인자 받을 수 있도록 ENTRYPOINT + CMD 구성
ENTRYPOINT ["poetry", "run", "python", "src/cherrypick_data_analysis/main.py"]
CMD ["fmkorea"]
