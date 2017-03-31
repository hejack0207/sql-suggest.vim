from string import find
import subprocess

ORACLE_TABLES_QUERY= """{0} 2> /dev/null <<< "select table_name from all_user_table where schema_name = '{1}';" """
ORACLE_COLUMNS_QUERY= """{0} 2> /dev/null <<< "select column_name from  all_user_columns where table_name = '{1}';" """
PSQL_TABLES_QUERY= """{0} -c "select tablename from pg_tables where schemaname = 'public'" {1} 2> /dev/null """
PSQL_COLUMNS_QUERY= """{0} -c "select column_name from information_schema.columns where table_name = {1}" 2> /dev/null """
MYSQL_TABLES_QUERY= """{0} -e 'SHOW tables;' {1} 2> /dev/null """
MYSQL_COLUMNS_QUERY= """{0} -e 'SHOW COLUMNS FROM {1}' 2> /dev/null """

def get_db_specific_query_statements(suggest_db):
    queries = {
        "oracle_tables": ORACLE_TABLES_QUERY,
        "oracle_columns": ORACLE_COLUMNS_QUERY,
        "psql_tables": PSQL_TABLES_QUERY,
        "psql_columns": PSQL_COLUMNS_QUERY,
        "mysql_tables": MYSQL_TABLES_QUERY,
        "mysql_columns": MYSQL_COLUMNS_QUERY
    }
    db_type = get_db_type(suggest_db)
    return (queries[db_type + "_tables"], queries[db_type + "_columns"])

def get_db_type(suggest_db):
    db_type = suggest_db.split(" ")[0]
    if find(db_type,"sqlplus") != 0:
        return db_type
    else:
        return "oracle"

def check_command_output(query_string):
    return subprocess.check_output(query_string, shell=True)

def get_table_names(suggest_db):
    get_tables_query, _ = get_db_specific_query_statements(suggest_db)
    schema_name = "schema"
    query_string = get_tables_query.format(suggest_db, schema_name)
    print "query string:"+query_string
    tables = check_command_output(query_string)
    db_type = get_db_type(suggest_db)
    if db_type == "mysql":
        return [{"word": table} for table in tables.rstrip().split("\n")[1:]]
    elif db_type == "psql":
        return [{"word": table.strip()} for table in tables.rstrip().split("\n")[2:-1]]
    elif db_type == "oracle":
        return [{"word": table} for table in tables.rstrip().split("\n")[1:]]


def create_column_name_list(suggest_db, tables, prefix=""):
    table_cols = []
    db_type = get_db_type(suggest_db)
    for table in tables:
        table = table["word"]
        query_string = get_db_specific_query_statements(suggest_db)[1].format(suggest_db, table)
        print "query string:"+query_string
        columns = check_command_output(query_string)
        if db_type == "mysql":
            table_cols.extend([{"word": prefix + column.split("\t")[0], "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[1:]])
        elif db_type == "psql":
            table_cols.extend([{"word": prefix + column.strip(), "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[2:-1]])
        elif db_type == "oracle":
            table_cols.extend([{"word": prefix + column.strip(), "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[2:-1]])
    return table_cols


def get_column_names(suggest_db, word_to_complete):
    if word_to_complete.endswith("."):
        return create_column_name_list(suggest_db, [{"word": word_to_complete[:-1]}], ".")
    else:
        return create_column_name_list(suggest_db, get_table_names(suggest_db))
