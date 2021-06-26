"""
Here is where we create the app which ends up being shared across all tests. A future
optimization will be to create a separate app instance for each test class.
"""
from rabbitai.app import create_app

app = create_app()
