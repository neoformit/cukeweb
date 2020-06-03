"""Custom exception classes for the cukeweb repository."""


class DuplicateCukeError(ValueError):
    """A cucumber with this ID is already registered in the database."""
