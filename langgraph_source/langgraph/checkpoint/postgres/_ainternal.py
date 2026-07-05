from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool
# fmt: off  MC8yOmFIVnBZMlhsaUpqbWxvYzZPSEY2Ync9PTo3ZTQ3Y2NmMA==

Conn = AsyncConnection[DictRow] | AsyncConnectionPool[AsyncConnection[DictRow]]


@asynccontextmanager
async def get_connection(
    conn: Conn,
) -> AsyncIterator[AsyncConnection[DictRow]]:
    if isinstance(conn, AsyncConnection):
        yield conn
    elif isinstance(conn, AsyncConnectionPool):
        async with conn.connection() as conn:
            yield conn
    else:
        raise TypeError(f"Invalid connection type: {type(conn)}")
# pragma: no cover  MS8yOmFIVnBZMlhsaUpqbWxvYzZPSEY2Ync9PTo3ZTQ3Y2NmMA==
