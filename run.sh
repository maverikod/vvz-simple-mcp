
#!/bin/bash
source .venv/bin/activate
export $(cat .env | xargs)
uvicorn server:app --host 0.0.0.0 --port 8000
