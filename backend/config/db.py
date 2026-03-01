from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.models import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Load .env from backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# ensure sqlite relative path resolves to an absolute file so that
# the engine always points to the same location regardless of current working
# directory (important for tests).
raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if raw_url.startswith("sqlite:///"):
    # strip prefix and resolve path
    path = raw_url.split("///", 1)[1]
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    DATABASE_URL = f"sqlite:///{path}"
else:
    DATABASE_URL = raw_url

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a SQLAlchemy session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
