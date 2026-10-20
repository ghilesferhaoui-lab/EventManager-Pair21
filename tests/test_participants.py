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

# ---------------------------------------------------------------------------
# Lab 3 - mutation killers (Student B)
# ---------------------------------------------------------------------------
from types import SimpleNamespace

from app.schemas import Participant as ParticipantSchema
from app.schemas import Registration as RegistrationSchema


def test_name_max_length_100_is_valid(sample_participant_dict):
    sample_participant_dict["name"] = "a" * 100
    assert len(ParticipantCreate(**sample_participant_dict).name) == 100


def test_name_101_chars_is_rejected(sample_participant_dict):
    sample_participant_dict["name"] = "a" * 101
    with pytest.raises(ValidationError):
        ParticipantCreate(**sample_participant_dict)


def test_zero_capacity_has_no_seat():
    assert has_available_capacity(0, 0) is False


def test_first_seat_is_available():
    assert has_available_capacity(0, 1) is True


def test_duplicate_error_message_names_the_id():
    with pytest.raises(ValueError) as excinfo:
        check_duplicate_registration([7], 7)
    assert str(excinfo.value) == "Participant 7 is already registered."


def test_duplicate_guard_on_empty_list_does_not_raise():
    check_duplicate_registration([], 1)


def test_participant_schema_reads_object_attributes():
    obj = SimpleNamespace(id=1, name="Amine", email="amine@example.com")
    p = ParticipantSchema.model_validate(obj)
    assert (p.id, p.name, p.email) == (1, "Amine", "amine@example.com")


def test_registration_schema_reads_object_attributes():
    obj = SimpleNamespace(id=5, event_id=2, participant_id=3)
    r = RegistrationSchema.model_validate(obj)
    assert (r.id, r.event_id, r.participant_id) == (5, 2, 3)


def test_email_is_kept_exactly_as_given(sample_participant_dict):
    assert ParticipantCreate(**sample_participant_dict).email == "alice@example.com"
