from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()
try:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Provide a database session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WalletRequest(Base):
    """Database model for wallet requests."""
    __tablename__ = "wallet_requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    raise RuntimeError(f"Failed to initialize database schema: {e}")

def create_wallet_request(db: Session, address: str) -> WalletRequest:
    """Create a wallet request."""
    db_wallet_request = WalletRequest(address=address)
    db.add(db_wallet_request)
    db.commit()
    db.refresh(db_wallet_request)
    return db_wallet_request
