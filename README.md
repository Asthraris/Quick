# ⚡ Quick  — View-Once Media Sharing API

A lightweight, high-performance **FastAPI** backend powering a temporary, view-once media sharing platform (Snapchat-style stories) with bidirectional friend relationship management, automated image expiration, and atomic view logging.

---

## 📐 Architecture & System Flow

### 1. Friends Management Flow

Friendships are stored bidirectionally in PostgreSQL. An accepted friendship allows users to access each other's active, non-expired media feeds.

```text
  ┌──────────┐                        ┌──────────┐
  │  User A  │ ────── Request ──────> │  User B  │
  └──────────┘                        └──────────┘
       │                                   │
       │ status: PENDING                   │
       └───────────────────────────────────┘
                         │
                   User B Accepts
                         │
                         ▼
             ┌──────────────────────┐
             │ status: ACCEPTED     │
             │ (Bidirectional Link) │
             └──────────────────────┘

```

---

### 2. View-Once Logic & Audit Log Lifecycle

To prevent client-side exploits and unauthorized caching, media URLs are hidden until the user explicitly requests to view an image. Viewing an image atomically writes an audit record to PostgreSQL, permanently locking out subsequent view attempts.

```text
 ┌──────────┐                               ┌──────────┐                          ┌────────────┐
 │  Client  │                               │  FastAPI │                          │ PostgreSQL │
 └────┬─────┘                               └────┬─────┘                          └─────┬──────┘
      │                                          │                                      │
      │ 1. GET /feed                │                                      │
      │─────────────────────────────────────────>│                                      │
      │                                          │  Query: friend's media Unviewed & Non-Expired       │
      │                                          │─────────────────────────────────────>│
      │                                          │  (LEFT JOIN media_audit == NULL)     │
      │                                          │<─────────────────────────────────────│
      │ 2. Returns [{ id, uploader_id, date , type }]   │                                      │
      │    (NO Media URLs exposed)               │                                      │
      │<─────────────────────────────────────────│                                      │
      │                                          │                                      │
      │ 3. POST /media/{id}/view   │                                      │
      │─────────────────────────────────────────>│                                      │
      │                                          │ 4. Check expiries_at & image_audit   │
      │                                          │─────────────────────────────────────>│
      │                                          │<─────────────────────────────────────│
      │                                          │                                      │
      │                                          │ 5. INSERT into image_audit           │
      │                                          │─────────────────────────────────────>│
      │                                          │                                      │
      │ 6. Returns { "url": "https://s3..." }    │                                      │
      │<─────────────────────────────────────────│                                      │
      │                                          │                                      │
      │ 7. POST /media/{id}/view   │                                      │
      │    (Re-view attempt)                     │                                      │
      │─────────────────────────────────────────>│ 8. Audit Record Exists               │
      │                                          │─────────────────────────────────────>│
      │ 9. 403 Forbidden                         │<─────────────────────────────────────│
      │<─────────────────────────────────────────│                                      │

```

---

## 🛠️ Stack Overview

* **Framework:** FastAPI (Python 3.11+)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy (Async/Sync Sessions)
* **Database Migrations:** Alembic
* **Data Validation:** Pydantic v2

---

## 🚀 Quickstart & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Asthraris/quick.git
cd quick

```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
# linux / mac
source .venv/bin/activate

#windows
.venv/Script/Activate

#dev requirements for now
pip install -r backend/requirements/dev.txt

```

---

## 🐘 Starting PostgreSQL

##### Using Docker Locally postgres(provided by the repo)

configure `docker-compose.yaml` as per You:

start postgreSQL : `docker compose up -d`
stop postgreSQL : `docker compose down`

##### Can also use Cloud PostgreSQL 

---

## 🔑 Environment Configuration

Create a `.env` file in the `/backend`:

```env
JWT_SECRET_KEY = 
JWT_ALGORITHM = 
DATABASE_URL = 


```

---

## 🔄 Database Migrations (Alembic)

I have uploaded my `migrations/` along side which is separted outside of backend but its using the same .venv to work and its source is set to `backend/` thus showing include errors (just work with it , i just wanted to separte it from backend)

### Running Migrations

```bash
#if not provided
# Generate migration script automatically from model changes
alembic revision --autogenerate -m "describe_changes_here"
# Apply pending migrations to the database
alembic upgrade head

```


---

## 🏃 Running the Application

```bash
cd backend
fastapi run OR dev
```

Once running, access the interactive API docs at:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

---

## 🔮 To Be Added Later

* [ ] S3 Direct Multipart / Presigned Upload Endpoint
* [ ] Automated Worker Thread (Celery / APScheduler) for deleting expired S3 assets and also deleting the media after 24 hours right now the access is removed but the the media is not deleted itself
* [ ] Rate limiting on media feed endpoints