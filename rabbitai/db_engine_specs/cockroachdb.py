from rabbitai.db_engine_specs.postgres import PostgresEngineSpec


class CockroachDbEngineSpec(PostgresEngineSpec):
    engine = "cockroachdb"
    engine_name = "CockroachDB"
    default_driver = ""
