# AuraNova

**AI-Powered Healthcare & Telemedicine Platform**

AuraNova is a Flask-based web application scaffold for a modern healthcare and telemedicine platform. This repository contains the initial project structure — business logic, authentication, and database models will be added in subsequent phases.

## Tech Stack

| Component        | Technology        |
|------------------|-------------------|
| Web Framework    | Python Flask      |
| ORM              | Flask-SQLAlchemy  |
| Migrations       | Flask-Migrate     |
| Authentication   | Flask-Login       |
| Configuration    | python-dotenv     |
| Database         | MySQL (PyMySQL)   |
| Frontend         | Bootstrap 5       |

## Project Structure

```
AuraNova/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extension instances
│   ├── auth/                # Authentication blueprint
│   ├── admin/               # Admin portal blueprint
│   ├── doctor/              # Doctor portal blueprint
│   ├── patient/             # Patient portal blueprint
│   ├── ai/                  # AI services blueprint
│   ├── models/              # SQLAlchemy models (future)
│   ├── services/            # Business logic layer (future)
│   ├── utils/               # Shared utilities
│   ├── static/              # CSS, JS, images
│   └── templates/           # Jinja2 templates
├── uploads/                 # User-uploaded files
├── database/                # Database files and migrations
├── docs/                    # Project documentation
├── tests/                   # Test suite
├── requirements.txt
├── run.py                   # Application entry point
├── .env.example             # Environment variable template
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+ (for production; not required to view the homepage)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd AuraNova
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # macOS / Linux
   ```

   Edit `.env` and set your `SECRET_KEY` and `DATABASE_URI`.

5. **Run the development server**

   ```bash
   python run.py
   ```

   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Database Setup (when ready)

Once MySQL is configured and models are defined:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running Tests

```bash
pip install pytest
pytest
```

## Environment Variables

| Variable       | Description                              | Example                                              |
|----------------|------------------------------------------|------------------------------------------------------|
| `FLASK_APP`    | Flask application entry point            | `run.py`                                             |
| `FLASK_ENV`    | Environment name                         | `development`                                        |
| `SECRET_KEY`   | Flask secret key for sessions            | `your-random-secret-key`                             |
| `DATABASE_URI` | SQLAlchemy database connection string    | `mysql+pymysql://user:pass@localhost:3306/aauranova` |

## License

Proprietary — All rights reserved.
