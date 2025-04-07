poetry install
cd src\cherrypick_ai
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
cmd /k