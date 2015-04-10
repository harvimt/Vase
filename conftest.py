import sys
import os.path
import pytest
import asyncio
sys.path.append(os.path.dirname(__file__))


@pytest.fixture(autouse=True)
def always_event_loop():
    try:
        asyncio.get_event_loop()
    except:
        asyncio.set_event_loop(asyncio.new_event_loop())
