from rabbitai.db_engine_specs.postgres import PostgresBaseEngineSpec


class VerticaEngineSpec(PostgresBaseEngineSpec):
    engine = "vertica"
    engine_name = "Vertica"
