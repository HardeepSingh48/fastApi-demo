# FastAPI Production Backend

A production-grade FastAPI application demonstrating best practices for building scalable, secure backend systems with PostgreSQL, SQLModel, JWT authentication, and RBAC authorization.

## 🚀 Features

- ✅ **Strict Type Safety** - Full type hints with Pylance strict mode
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Role-Based Access Control (RBAC)** - Admin and user roles
- ✅ **PostgreSQL + SQLModel** - Type-safe ORM with Pydantic integration
- ✅ **Alembic Migrations** - Database schema version control
- ✅ **Pydantic Settings** - Type-validated configuration
- ✅ **Password Hashing** - Bcrypt for secure password storage
- ✅ **API Schemas** - Separate DB models from API responses
- ✅ **Production-Ready Architecture** - Feature-based folder structure

## 📋 Prerequisites

- Python 3.12.7
- PostgreSQL 15+
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd fastapi
```

### 2. Create virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

```bash
# Create database
createdb fastapi_db

# Or using psql
psql -U postgres
CREATE DATABASE fastapi_db;
\q
```

### 5. Configure environment variables

```bash
# Copy example env file
cp .env.example .env

# Generate a secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env with your settings
```

Required environment variables:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db
JWT_SECRET=your-generated-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run database migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 7. (Optional) Seed database

```bash
python -m app.db.seed
```

This creates an initial admin user:
- Email: `admin@example.com`
- Password: `admin123` (change this in production!)

## 🏃 Running the Application

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## 📁 Project Structure

```
fastapi/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/                # Core functionality
│   │   ├── config.py        # Pydantic settings
│   │   ├── security.py      # Password hashing, JWT
│   │   ├── exception.py     # Custom exceptions
│   │   └── tracing.py       # Request tracing
│   ├── db/                  # Database layer
│   │   ├── engine.py        # Database engine
│   │   ├── session.py       # Session management
│   │   ├── models.py        # SQLModel models
│   │   └── seed.py          # Database seeding
│   ├── auth/                # Authentication
│   │   ├── routes.py        # Auth endpoints
│   │   └── dependencies.py  # Auth dependencies
│   ├── users/               # User management
│   │   ├── routes.py        # User endpoints
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── service.py       # Business logic
│   ├── posts/               # Posts feature
│   │   ├── routes.py
│   │   └── schemas.py
│   └── middlewares/         # Custom middleware
│       └── cors.py
├── alembic/                 # Database migrations
├── docs/                    # Documentation
│   └── tutorial/            # Learning materials
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔐 Security

- **Passwords**: Hashed with bcrypt before storage
- **JWT Tokens**: Signed with HS256 algorithm
- **CORS**: Configured for specific origins only
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection**: Protected by SQLModel/SQLAlchemy

## 🧪 API Endpoints

### Authentication

- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/register` - Register new user

### Users

- `GET /api/users/me` - Get current user (authenticated)
- `GET /api/users/{id}` - Get user by ID
- `PATCH /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user (admin only)

### Posts

- `GET /api/posts` - List all posts
- `POST /api/posts` - Create post (authenticated)
- `GET /api/posts/{id}` - Get post by ID
- `PUT /api/posts/{id}` - Update post (owner or admin)
- `DELETE /api/posts/{id}` - Delete post (owner or admin)

## 📚 Learning Resources

Comprehensive tutorials are available in `docs/tutorial/`:

1. **Python Environment & Strict Typing**
2. **Project Architecture & Setup**
3. **Database Layer**
4. **Models & Schemas**
5. **JWT Authentication**
6. **RBAC Authorization**
7. **Advanced Production Patterns**
8. **Complete Request Flow**

Start with `docs/tutorial/README.md` for the complete guide.

## 🛡️ Type Safety

This project uses strict type checking with Pylance:

```bash
# VS Code settings are configured for:
- Type checking mode: standard
- Report missing imports: error
- Report undefined variables: error
- Report optional member access: error
```

## 🔄 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built following production best practices for:
- FastAPI applications
- PostgreSQL database design
- JWT authentication
- Type-safe Python development
- Clean architecture principles

---

**Happy Coding! 🚀**
