import os, httpx, time
from typing import Iterator

OPENAQ_BASE_URL = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v2")

def batched(iterable, n) -> Iterator[list]:
    batch = []
    for x in iterable:
        batch.append(x)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch
