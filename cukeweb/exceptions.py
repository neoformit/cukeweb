"""Custom exception classes for the cukeweb repository."""


class DuplicateCucumberError(ValueError):
    """A cucumber with this ID is already registered in the database."""
