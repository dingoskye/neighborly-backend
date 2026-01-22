# Neighborly Connect Backend

This is the FastAPI backend for the Neighborly Connect application.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Seeding Data

To populate the database with initial mock data (Users, Posts, Events), run:

```bash
python seed.py
```

## Running the Server

Start the development server on port 8001:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`.
You can view the interactive API documentation at `http://localhost:8001/docs`.
