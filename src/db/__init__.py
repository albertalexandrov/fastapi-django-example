from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


dsn = "postgresql+asyncpg://postgres:postgres@localhost:5433/django-like-repositories"
engine = create_async_engine(dsn, echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
