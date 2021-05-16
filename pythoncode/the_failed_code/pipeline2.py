from pyflink.table import TableEnvironment, EnvironmentSettings

def log_processing():
    env_settings = EnvironmentSettings.new_instance().use_blink_planner().is_streaming_mode().build()
    t_env = TableEnvironment.create(env_settings)
    # specify connector and format jars
    t_env.get_config().get_configuration().set_string("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")
    
    source_ddl = """
            CREATE TABLE source_table(
                a VARCHAR,
                b SERIAL
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'topic',
              'properties.bootstrap.servers' = 'localhost:9092',
              'properties.group.id' = 'testGroup'
              'scan.startup.mode' = 'latest-offset',
              'format' = 'json'
            )
            """

    sink_ddl = """
            CREATE TABLE sink_table(
                a VARCHAR
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'topic2',
              'properties.bootstrap.servers' = 'kafka:9092',
              'format' = 'json'
            )
            """

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    t_env.sql_query("SELECT a FROM source_table") \
        .execute_insert("sink_table").wait()


if __name__ == '__main__':
    log_processing()
