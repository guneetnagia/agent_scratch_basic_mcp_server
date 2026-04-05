"""
Database Connection Manager

Handles async PostgreSQL connection pooling.
"""

import asyncpg
import os
from typing import Optional


class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/idea_hub"),
                min_size=1,
                max_size=10
            )

            # 👇 RUN MIGRATIONS ON STARTUP
            await cls.run_migrations()
    @classmethod
    async def disconnect(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            await cls.connect()
        return cls._pool
    
    @classmethod
    async def run_migrations(cls):
        async with cls._pool.acquire() as conn:
            with open("migrations/001_init.sql") as f:
                await conn.execute(f.read())


# -------------------------
# Helper (what your repo expects)
# -------------------------
async def get_db():
    return await Database.get_pool()