import pytest
from pydantic import ValidationError
from types import SimpleNamespace

from app.schemas import Event as EventSchema
from app.schemas import EventCreate


# mutant 8: description default None -> ""
def test_description_defaults_to_none(sample_event_dict):
    del sample_event_dict["description"]
    assert EventCreate(**sample_event_dict).description is None


# mutant 9: location min_length 2 -> 3
def test_location_two_chars_is_valid(sample_event_dict):
    sample_event_dict["location"] = "ab"
    assert EventCreate(**sample_event_dict).location == "ab"


# mutant 10: location max_length 100 -> 101
def test_location_100_chars_ok_101_rejected(sample_event_dict):
    sample_event_dict["location"] = "a" * 100
    assert len(EventCreate(**sample_event_dict).location) == 100
    sample_event_dict["location"] = "a" * 101
    with pytest.raises(ValidationError):
        EventCreate(**sample_event_dict)


# mutant 11: location Field(...) removed -> default None
def test_location_is_required(sample_event_dict):
    del sample_event_dict["location"]
    with pytest.raises(ValidationError):
        EventCreate(**sample_event_dict)


def test_location_one_char_is_rejected(sample_event_dict):
    sample_event_dict["location"] = "a"
    with pytest.raises(ValidationError):
        EventCreate(**sample_event_dict)


# mutants 15 and 16: from_attributes=True removed
def test_event_schema_reads_object_attributes(sample_event_dict):
    obj = SimpleNamespace(id=1, **sample_event_dict)
    e = EventSchema.model_validate(obj)
    assert e.id == 1
    assert e.title == sample_event_dict["title"]
    assert e.capacity == sample_event_dict["capacity"]
