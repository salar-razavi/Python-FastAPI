from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.engine import URL
import logging
from app.config import setting

logging.basicConfig(
    filename="db.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

db_url = URL.create(
    "postgresql+asyncpg",
    username=setting.username,
    password=setting.password,
    host=setting.host,
    port=setting.port,
    database=setting.database,
)



""" create Engine """
engine = create_async_engine(db_url,echo=False,pool_pre_ping=True,pool_size=5,max_overflow=10)

""" Create Session """
SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)


Base = declarative_base()

async def get_db():
    async  with SessionLocal() as session:
        yield session