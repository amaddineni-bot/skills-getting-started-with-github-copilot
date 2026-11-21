import copy

import pytest
from fastapi.testclient import TestClient

from app import activities, app


@pytest.fixture
def client():
    # Restore the in-memory database after each test so tests stay isolated
    snapshot = copy.deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(snapshot)
