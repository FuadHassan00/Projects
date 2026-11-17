"""Custom exceptions for flight agent."""


class FlightAgentException(Exception):
    """Base exception for flight agent."""
    pass


class FlightAgentExecutionError(FlightAgentException):
    """Raised when flight agent execution fails."""
    pass


class FlightSearchError(FlightAgentException):
    """Raised when a flight search fails."""
    pass


class ValidationError(FlightAgentException):
    """Raised when input validation fails."""
    pass


class ConfigurationError(FlightAgentException):
    """Raised when flight agent configuration is invalid."""
    pass