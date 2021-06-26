import pytest
from sqlalchemy.engine.url import make_url

from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.security.analytics_db_safety import check_sqlalchemy_uri
from tests.base_tests import RabbitaiTestCase


class TestDBConnections(RabbitaiTestCase):
    def test_check_sqlalchemy_uri_ok(self):
        check_sqlalchemy_uri(make_url("postgres://user:password@test.com"))

    def test_check_sqlalchemy_url_sqlite(self):
        with pytest.raises(RabbitaiSecurityException) as excinfo:
            check_sqlalchemy_uri(make_url("sqlite:///home/rabbitai/bad.db"))
        assert (
            str(excinfo.value)
            == "SQLiteDialect_pysqlite cannot be used as a data source for security reasons."
        )

        with pytest.raises(RabbitaiSecurityException) as excinfo:
            check_sqlalchemy_uri(make_url("shillelagh:///home/rabbitai/bad.db"))
        assert (
            str(excinfo.value)
            == "shillelagh cannot be used as a data source for security reasons."
        )
