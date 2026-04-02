"""
Database Server Manager
Handles SQLAlchemy connection and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from database.models import Base
import logging

logger = logging.getLogger(__name__)


class SQLManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        """Initialize database manager."""
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.AsyncSessionLocal = None
        self._db_url = self._get_database_url()
    
    def _get_database_url(self) -> str:
        """Get database URL from environment or config."""
        db_type = os.getenv("DB_TYPE", "postgresql").lower()
        
        if db_type == "postgresql":
            user = os.getenv("DB_USER", "postgres")
            password = os.getenv("DB_PASSWORD", "")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            database = os.getenv("DB_NAME", "econ_discord")
            
            if password:
                return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
            else:
                return f"postgresql+asyncpg://{user}@{host}:{port}/{database}"
        
        elif db_type == "sqlite":
            db_path = os.getenv("DB_PATH", "econ_discord.db")
            return f"sqlite+aiosqlite:///{db_path}"
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    async def authenticate(self):
        """Authenticate and establish database connection."""
        try:
            self.async_engine = create_async_engine(
                self._db_url,
                echo=os.getenv("SQL_ECHO", "false").lower() == "true",
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20
            )
            
            self.AsyncSessionLocal = async_sessionmaker(
                self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Test connection
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("Database authenticated successfully")
        except Exception as e:
            logger.error(f"Failed to authenticate database: {e}")
            raise
    
    async def sync_database(self, force: bool = False):
        """Sync database schema with models."""
        if not self.async_engine:
            raise RuntimeError("Database not authenticated")
        
        try:
            async with self.async_engine.begin() as conn:
                if force:
                    logger.warning("Force syncing database - dropping all tables")
                    await conn.run_sync(Base.metadata.drop_all)
                
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("Database synced successfully")
        except Exception as e:
            logger.error(f"Failed to sync database: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get an async database session."""
        if not self.AsyncSessionLocal:
            raise RuntimeError("Database not authenticated")
        
        return self.AsyncSessionLocal()
    
    async def close(self):
        """Close database connections."""
        if self.async_engine:
            await self.async_engine.dispose()
            logger.info("Database connections closed")


# Global database instance
db_manager = SQLManager()


async def get_db_session() -> AsyncSession:
    """Dependency for getting database session."""
    async with db_manager.AsyncSessionLocal() as session:
        yield session
