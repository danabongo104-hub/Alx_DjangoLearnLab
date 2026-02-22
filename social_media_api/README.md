# Social Media API

A RESTful Social Media API built with Django and Django REST Framework.

---

## Project Structure

```
social_media_api/
├── manage.py
├── requirements.txt
├── README.md
├── social_media_api/        ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── accounts/                ← User auth app
    ├── models.py            ← CustomUser model
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/danabongo104-hub/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

> **Note:** Because we set `AUTH_USER_MODEL = 'accounts.CustomUser'` in
> `settings.py` **before** the first migration, Django knows to use our
> custom user table from the start. If you ever change the user model after
> running migrations you'll need to reset the database.

### 3. Start the development server

```bash
python manage.py runserver
```

---

## User Model

`accounts.CustomUser` extends Django's `AbstractUser` with these extra fields:

| Field             | Type            | Description                                      |
|-------------------|-----------------|--------------------------------------------------|
| `bio`             | TextField       | Optional short biography                         |
| `profile_picture` | ImageField      | Stored under `media/profile_pictures/`           |
| `following`       | ManyToManyField | Users this user follows (asymmetric, see below)  |

### Why asymmetric ManyToManyField?

```python
following = models.ManyToManyField(
    'self',
    symmetrical=False,   # A→B does NOT imply B→A
    related_name='followers',
    blank=True,
)
```

- `user.following.all()` → everyone **this user** follows  
- `user.followers.all()` → everyone **following this user**

---

## Authentication

The API uses **Token Authentication**. Every protected endpoint requires:

```
Authorization: Token <your_token_here>
```

---

## API Endpoints

### Register

**POST** `/api/accounts/register/`

No authentication required.

**Request body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "securepassword123",
  "bio": "Hello world!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "bio": "Hello world!",
  "profile_picture": null,
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Login

**POST** `/api/accounts/login/`

No authentication required.

**Request body:**
```json
{
  "username": "alice",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "alice"
}
```

---

### Profile

**GET** `/api/accounts/profile/`  
**PATCH** `/api/accounts/profile/`

Requires authentication. Returns or updates the **currently authenticated** user's profile.

**GET Response:**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "bio": "Hello world!",
  "profile_picture": null,
  "followers_count": 0,
  "following_count": 0
}
```

**PATCH Request (update bio):**
```json
{
  "bio": "Updated bio text"
}
```

---

## Design Decisions

| Decision | Why |
|---|---|
| `AbstractUser` not `AbstractBaseUser` | We only add fields — no need to redesign the full auth system |
| Token auth not JWT | Simpler, no refresh-token logic, perfect for learning projects |
| `IsAuthenticated` as global default | Secure by default; individual views opt out with `AllowAny` |
| `create_user()` not `create()` | Ensures passwords are hashed via Django's password hasher |
| SQLite in development | Zero config; swap for PostgreSQL in production (Task 4) |

---

## Posts & Comments API (Task 1)

All post/comment endpoints require `Authorization: Token <token>`.

### Posts

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/api/posts/` | Required | List posts (paginated, 10/page) |
| POST | `/api/posts/` | Required | Create a post |
| GET | `/api/posts/{id}/` | Required | Retrieve a post |
| PATCH | `/api/posts/{id}/` | Author only | Partial update |
| DELETE | `/api/posts/{id}/` | Author only | Delete post |

**Search & Filter:** `GET /api/posts/?search=django&ordering=-created_at`

**Create Post:**
```json
POST /api/posts/
{ "title": "My first post", "content": "Hello world!" }
```

**Response:**
```json
{
  "id": 1, "author": 1, "author_username": "alice",
  "title": "My first post", "content": "Hello world!",
  "comments_count": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Comments

Filter comments by post: `GET /api/comments/?post=1`

**Create Comment:**
```json
POST /api/comments/
{ "post": 1, "content": "Great post!" }
```

### Task 1 Design Decisions

| Decision | Why |
|---|---|
| `select_related('author')` on queryset | Prevents N+1 queries when serializing author_username for each post |
| Flat `/api/comments/?post=<id>` instead of nested route | Simpler URL structure, same result, standard DRF pattern |
| Custom `IsAuthorOrReadOnly` permission | Reusable across both Post and Comment; keeps views clean |
| `comments_count` not nested comments in PostSerializer | Avoids loading thousands of comments on every list request |
| `auto_now_add` / `auto_now` on timestamps | Zero-effort audit trail — Django sets them automatically |