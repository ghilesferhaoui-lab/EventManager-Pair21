import pytest
from pydantic import ValidationError

from app.registration import check_duplicate_registration, has_available_capacity
from app.schemas import ParticipantCreate


# Happy path
def test_valid_participant_creation(sample_participant_dict):
    p = ParticipantCreate(**sample_participant_dict)
    assert p.name == sample_participant_dict["name"]
    assert p.email == sample_participant_dict["email"]


def test_has_available_capacity_when_seats_left():
    assert has_available_capacity(10, 100) is True


def test_check_duplicate_registration_accepts_new_id():
    check_duplicate_registration([1, 2, 3], 4)  # must not raise


# Boundary values
def test_capacity_current_is_max_minus_one():
    assert has_available_capacity(99, 100) is True


def test_capacity_current_equals_max():
    assert has_available_capacity(100, 100) is False


def test_capacity_current_greater_than_max():
    assert has_available_capacity(101, 100) is False


def test_name_minimum_length_two_is_valid(sample_participant_dict):
    sample_participant_dict["name"] = "Al"
    assert ParticipantCreate(**sample_participant_dict).name == "Al"


# Negative tests
@pytest.mark.parametrize("bad_email", ["not-an-email", "missing@tld", "@no-user.com", ""])
def test_invalid_email_raises_validation_error(sample_participant_dict, bad_email):
    sample_participant_dict["email"] = bad_email
    with pytest.raises(ValidationError):
        ParticipantCreate(**sample_participant_dict)


def test_short_name_raises_validation_error(sample_participant_dict):
    sample_participant_dict["name"] = "A"
    with pytest.raises(ValidationError):
        ParticipantCreate(**sample_participant_dict)


def test_duplicate_registration_raises_value_error():
    with pytest.raises(ValueError):
        check_duplicate_registration([1, 2, 3], 2)