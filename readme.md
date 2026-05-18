# Booking System API

A RESTful API for a comprehensive booking and appointment management system built with FastAPI, PostgreSQL, and Celery.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Task Queue | Celery + Redis |
| Authentication | JWT (Access + Refresh Tokens) |
| Email | SendGrid |
| Payments | Stripe |
| Containerization | Docker Compose |

## Features

- **User Authentication**: Register, login, forgot password, reset password with JWT tokens
- **Business Management**: Business owners can create and manage their businesses
- **Services**: Define and manage business services with pricing & time
- **Appointments**: Full appointment booking system with status tracking
- **Business Hours**: Configurable operating hours per business
- **Customer Management**: Manage walk-in customers
- **Payments**: Stripe integration for appointment deposits
- **Background Tasks**: Automated no-show detection via Celery

## Project Structure

```
bookingSystem/
├── app/
│   ├── api/v1/          # API endpoints
│   │   ├── auth.py
│   │   ├── business.py
│   │   ├── appointments.py
│   │   ├── business_hours.py
│   │   ├── services.py
│   │   ├── business_customers.py
│   │   └── payments.py
│   ├── core/            # Core configurations
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── db/              # Database setup
│   │   ├── session.py
│   │   └── base.py
│   ├── models/          # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Utilities
│   └── workers/        # Celery tasks
├── alembic/            # Database migrations
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and setup virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r app/requirements.txt
```

3. **Create .env file**

Copy `.env.example` to `.env` and configure:

```
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=your-email@example.com
SQLALCHEMY_DATABASE_URL=postgresql://postgres:12345@localhost:5400/bookingSystem
STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-webhook-secret
```

4. **Start services**

```bash
# Start PostgreSQL and Redis (or use Docker)
docker-compose up -d postgres redis
```

5. **Run migrations**

```bash
cd app
alembic upgrade head
```

6. **Start the application**

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3: Start FastAPI
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Start all services
docker-compose up --build

# Services will be available at:
# - API: http://localhost:8000
# - Flower (Celery monitor): http://localhost:5555
# - Frontend: http://localhost:3000
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login (returns JWT) |
| POST | `/auth/refresh-token` | Refresh access token |
| POST | `/auth/forgot-password` | Request password reset |
| POST | `/auth/reset-password` | Reset password with OTP |
| POST | `/auth/logout` | Logout |

### Business
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/business` | Create business |
| GET | `/business` | Get current user's business |
| PUT | `/business` | Update business |
| DELETE | `/business` | Delete business |

### Business Hours
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/business-hours` | Get business hours |
| POST | `/business-hours` | Set business hours |
| PUT | `/business-hours/{id}` | Update hours |
| DELETE | `/business-hours/{id}` | Delete hours |

### Services
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/services` | Get business services |
| POST | `/services` | Create service |
| PUT | `/services/{id}` | Update service |
| DELETE | `/services/{id}` | Delete service |

### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/appointments` | Get user's appointments |
| GET | `/appointments/{id}` | Get appointment by ID |
| POST | `/appointments` | Book appointment |
| PUT | `/appointments/{id}` | Update appointment |
| DELETE | `/appointments/{id}` | Cancel appointment |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | Get business customers |
| POST | `/customers` | Add customer |
| PUT | `/customers/{id}` | Update customer |
| DELETE | `/customers/{id}` | Delete customer |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/checkout` | Create Stripe checkout session |
| POST | `/payments/webhook` | Stripe webhook handler |
| GET | `/payments/{id}` | Get payment status |

## Testing Celery

```bash
# Test endpoint to verify Celery is working
curl http://localhost:8000/test-task
```

## Stripe Webhook (Development)

```bash
# Login to Stripe CLI
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/payments/webhook
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SENDGRID_API_KEY` | SendGrid API key for emails | Required |
| `FROM_EMAIL` | Email sender address | Required |
| `SQLALCHEMY_DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Optional |
| `STRIPE_SECRET_KEY` | Stripe secret key | Optional |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | Optional |
| `CORS_ORIGINS` | Allowed CORS origins | `localhost:5173,localhost:3000,localhost:8080` |

