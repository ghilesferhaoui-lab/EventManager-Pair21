from datetime import date

import pytest

from app.schemas import Event as EventSchema


# ---------------------------------------------------------------------------
# Data generators
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_event_dict():
    """A clean, valid event payload."""
    return {
        "title": "Python Conference",
        "description": "Annual Python meetup",
        "date": date(2030, 1, 15),
        "location": "Algiers",
        "capacity": 100,
    }


@pytest.fixture
def sample_participant_dict():
    """A clean, valid participant payload."""
    return {
        "name": "Alice Benali",
        "email": "alice@example.com",
    }


# ---------------------------------------------------------------------------
# State & teardown
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_event_store():
    """In-memory list acting as an event repository."""
    store = []
    yield store          
    store.clear()        


@pytest.fixture
def prepopulated_event_store(mock_event_store):
    """Chained fixture: the store above, pre-filled with 3 events."""
    events = [
        EventSchema(
            id=1,
            title="Python Conference",
            description="Annual Python meetup",
            date=date(2030, 1, 15),
            location="Algiers",
            capacity=100,
        ),
        EventSchema(
            id=2,
            title="DevOps Workshop",
            description="CI/CD hands-on",
            date=date(2030, 2, 20),
            location="Oran",
            capacity=50,
        ),
        EventSchema(
            id=3,
            title="Cybersecurity Summit",
            description="Security talks",
            date=date(2030, 3, 10),
            location="Blida",
            capacity=200,
        ),
    ]
    mock_event_store.extend(events)
    return mock_event_store


# ---------------------------------------------------------------------------
# Autouse
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def global_environment_logger(request):
    """Runs around EVERY test and prints setup/teardown markers (use -s to see)."""
    print(f"\n[SETUP]    starting  {request.node.name}")
    yield
    print(f"\n[TEARDOWN] finished  {request.node.name}")