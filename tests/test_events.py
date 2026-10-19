import pytest
from pydantic import ValidationError

from app.schemas import EventCreate
from app.search import filter_events_by_location, filter_events_by_title


def test_valid_event_is_created(sample_event_dict):
    event = EventCreate(**sample_event_dict)
    assert event.capacity == 100


def test_filter_by_location_is_case_insensitive(prepopulated_event_store):
    result = filter_events_by_location(prepopulated_event_store, "bLiDa")
    assert len(result) == 1
    assert result[0].location == "Blida"


def test_filter_by_title_is_case_insensitive(prepopulated_event_store):
    result = filter_events_by_title(prepopulated_event_store, "SECURITY")
    assert len(result) == 1
    assert result[0].title == "Cybersecurity Summit"

def test_capacity_1_ok(sample_event_dict):
    sample_event_dict["capacity"] = 1
    assert EventCreate(**sample_event_dict).capacity == 1


def test_capacity_10000_ok(sample_event_dict):
    sample_event_dict["capacity"] = 10000
    assert EventCreate(**sample_event_dict).capacity == 10000


def test_title_3_chars_ok(sample_event_dict):
    sample_event_dict["title"] = "abc"
    assert EventCreate(**sample_event_dict).title == "abc"


def test_short_title_rejected(sample_event_dict):
    sample_event_dict["title"] = "ab"
    with pytest.raises(ValidationError):
        EventCreate(**sample_event_dict)


@pytest.mark.parametrize("bad", [0, -5, 10001])
def test_bad_capacity_rejected(sample_event_dict, bad):
    sample_event_dict["capacity"] = bad
    with pytest.raises(ValidationError):
        EventCreate(**sample_event_dict)