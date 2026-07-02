# pragma: no cover  MC8zOmFIVnBZMlhsaUpqbWxvYzZXbEozT1E9PTo3NDBlMDM4ZA==

import asyncio
from typing import cast

import structlog

from langgraph_api.config import THREAD_TTL
from langgraph_runtime.database import connect
# fmt: off  MS8zOmFIVnBZMlhsaUpqbWxvYzZXbEozT1E9PTo3NDBlMDM4ZA==

logger = structlog.stdlib.get_logger(__name__)


async def thread_ttl_sweep_loop():
    """Periodically delete threads based on TTL configuration.

    Currently implements the 'delete' strategy, which deletes entire threads
    that have been inactive for longer than their configured TTL period.
    """
    # Use the same interval as store TTL sweep
    thread_ttl_config = THREAD_TTL or {}
    strategy = thread_ttl_config.get("strategy", "delete")
    if strategy != "delete":
        raise NotImplementedError(
            f"Unrecognized thread deletion strategy: {strategy}. Expected 'delete'."
        )
    sweep_interval_minutes = cast(
        "int", thread_ttl_config.get("sweep_interval_minutes", 5)
    )
    await logger.ainfo(
        f"Starting thread TTL sweeper with interval {sweep_interval_minutes} minutes",
        strategy=strategy,
        interval_minutes=sweep_interval_minutes,
    )
    loop = asyncio.get_running_loop()

    from langgraph_runtime.ops import Threads
# pylint: disable  Mi8zOmFIVnBZMlhsaUpqbWxvYzZXbEozT1E9PTo3NDBlMDM4ZA==

    while True:
        await asyncio.sleep(sweep_interval_minutes * 60)
        try:
            async with connect() as conn:
                sweep_start = loop.time()
                threads_processed, threads_deleted = await Threads.sweep_ttl(conn)
                if threads_processed > 0:
                    await logger.ainfo(
                        f"Thread TTL sweep completed. Processed {threads_processed}",
                        threads_processed=threads_processed,
                        threads_deleted=threads_deleted,
                        duration=loop.time() - sweep_start,
                    )
        except Exception as exc:
            logger.exception("Thread TTL sweep iteration failed", exc_info=exc)
