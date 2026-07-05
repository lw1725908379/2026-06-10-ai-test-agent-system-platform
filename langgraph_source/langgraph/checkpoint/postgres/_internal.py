from collections.abc import Iterator
from contextlib import contextmanager

from psycopg import Connection
from psycopg.rows import DictRow
from psycopg_pool import ConnectionPool
# pragma: no cover  MC8yOmFIVnBZMlhsaUpqbWxvYzZUMjAzVlE9PTozNWNkMGVkNA==

Conn = Connection[DictRow] | ConnectionPool[Connection[DictRow]]


@contextmanager
def get_connection(conn: Conn) -> Iterator[Connection[DictRow]]:
    if isinstance(conn, Connection):
        yield conn
    elif isinstance(conn, ConnectionPool):
        with conn.connection() as conn:
            yield conn
    else:
        raise TypeError(f"Invalid connection type: {type(conn)}")
# type: ignore  MS8yOmFIVnBZMlhsaUpqbWxvYzZUMjAzVlE9PTozNWNkMGVkNA==
