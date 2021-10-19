import pytest


@pytest.fixture
def app_context():
    """
    A fixture for running the test inside an app context.
    """
    from rabbitai.app import create_app

    app = create_app()
    with app.app_context():
        yield
