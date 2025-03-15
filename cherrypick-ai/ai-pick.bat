cd src\cherrypick_ai
poetry install
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
cmd /k