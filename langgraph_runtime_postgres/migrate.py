import asyncio
from pathlib import Path
# fmt: off  MC8yOmFIVnBZMlhsaUpqbWxvYzZPRVJWZHc9PTplYzU3YTY2YQ==

from langgraph_runtime_postgres import database
from langgraph_runtime_postgres.database import (
    create_pool,
    migrate,
    migrate_vector_index,
)


async def migrate_for_tests():
    database._pg_pool = create_pool()
    database.config.MIGRATIONS_PATH = Path(__file__).parent / ".." / "migrations"
    # confirm connectivity
    await database._pg_pool.open(wait=True)

    await migrate()
    await migrate_vector_index()


if __name__ == "__main__":
    asyncio.run(migrate_for_tests())
# type: ignore  MS8yOmFIVnBZMlhsaUpqbWxvYzZPRVJWZHc9PTplYzU3YTY2YQ==
