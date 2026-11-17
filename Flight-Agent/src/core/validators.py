"""Input validation for flight agent."""

from datetime import date, datetime
from math import isfinite
from .exceptions import ValidationError


def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD) and ensure date is in the future."""
    if not isinstance(date_str, str):
        raise ValidationError("Date must be a string in YYYY-MM-DD format")

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD")

    if parsed_date <= date.today():
        raise ValidationError("Flight date must be in the future")

    return True


def validate_date_range(depart_date: str,return_date: str | None = None,flight_type: int = 2) -> bool:
    """Validate flight dates for one-way and round-trip searches."""

    if isinstance(flight_type, bool):
        raise ValidationError(
            "Flight type must be 1 (round-trip) or 2 (one-way)"
        )

    try:
        flight_type = int(flight_type)
    except (ValueError, TypeError):
        raise ValidationError(
            "Flight type must be 1 (round-trip) or 2 (one-way)"
        )

    if flight_type not in (1, 2):
        raise ValidationError(
            "Flight type must be 1 (round-trip) or 2 (one-way)"
        )

    validate_date(depart_date)

    if flight_type == 1:
        if not return_date:
            raise ValidationError(
                "Return date is required for round-trip flights"
            )

        validate_date(return_date)

        departure = date.fromisoformat(depart_date)
        returning = date.fromisoformat(return_date)

        if returning <= departure:
            raise ValidationError(
                "Return date must be after departure date"
            )

    elif return_date is not None:
        raise ValidationError(
            "Return date should not be provided for one-way flights"
        )

    return True


def validate_search_window(start_date: str,end_date: str) -> bool:
    """Validate a flexible departure date range for award searches."""

    validate_date(start_date)
    validate_date(end_date)

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if end < start:
        raise ValidationError("End date cannot be before start date")

    return True


def validate_city(city: str) -> bool:
    """Validate city names or airport codes."""

    if not isinstance(city, str) or len(city.strip()) < 2:
        raise ValidationError("City name or airport code must be at least 2 characters")

    return True


def validate_airports(origin: str, destination: str) -> bool:
    """Validate origin and destination locations."""

    validate_city(origin)
    validate_city(destination)

    if origin.strip().upper() == destination.strip().upper():
        raise ValidationError("Origin and destination cannot be the same")

    return True


def validate_passengers(num: int | str) -> bool:
    """Validate number of passengers (1–9)."""

    if isinstance(num, bool):
        raise ValidationError(
            "Number of passengers must be between 1 and 9"
        )

    try:
        num = int(num)
    except (ValueError, TypeError):
        raise ValidationError(
            "Number of passengers must be a valid integer"
        )

    if not 1 <= num <= 9:
        raise ValidationError(
            "Number of passengers must be between 1 and 9"
        )

    return True


def validate_budget(budget: float) -> bool:
    """Validate budget."""

    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not isfinite(budget)
        or budget <= 0
    ):
        raise ValidationError("Budget must be a positive finite number")

    return True
