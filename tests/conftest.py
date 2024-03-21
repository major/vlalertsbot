"""Pytest fixtures for the tests."""

import os
from glob import glob

import pytest


def get_email_types():
    """Get sample emails for fixtures."""
    return [os.path.splitext(os.path.basename(x))[0] for x in glob("tests/alerts/*.txt")]


@pytest.fixture(scope="session", params=get_email_types())
def real_emails(request):
    """Fixture to get sample emails."""
    print("doot")
    with open(f"tests/alerts/{request.param}.txt") as email:
        return email.read()
