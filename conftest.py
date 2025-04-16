import os

def pytest_configure():
    os.environ.setdefault("USE_SQLITE_FOR_TESTS", "1")
