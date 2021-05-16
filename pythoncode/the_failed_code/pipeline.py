from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf
from pyflink.datastream import StreamExecutionEnvironment

import tokenizer
import pandas as pd
from gensim.models.ldamodel import LdaModel
from gensim.corpora import Dictionary


ddl_jdbc_source = """CREATE TABLE words (
                            word VARCHAR(50)
                    ) WITH (
                        'connector'= 'kafka',                        
                        'topic' = 'test',
                        'properties.bootstrap.servers' = 'localhost:9092',
                        'scan.startup.mode' = 'latest-offset',
                        'format' = 'json'                        
                    )"""


ddl_jdbc_sink = """INSERT INTO the_database.the_table (word) VALUES (
                        word VARCHAR(50)
                ) WITH (
                    'connector'= 'jdbc',
                    'url' = 'jdbc:postgresql://postgres:5432/postgres',
                    'table-name' = 'the_database.the_table',
                    'username' = 'postgres',
                    'password' = 'postgres'
                )"""


if __name__ == '__main__':

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    t_env = StreamTableEnvironment.create(env)

    config = t_env.get_config().get_configuration().set_string("pipeline.jars",
                                                               "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")
    config.set_string("taskmanager.memory.task.off-heap.size", "80mb")  # 512mb

    create_jdbc_source = t_env.execute_sql(ddl_jdbc_source)
    create_jdbc_sink = t_env.execute_sql(ddl_jdbc_sink)
