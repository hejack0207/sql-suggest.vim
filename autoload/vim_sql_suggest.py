import subprocess


def get_db_specific_query_statements(suggest_db):
    queries = {
        "oracle_tables": """{0} 2> /dev/null <<< "select table_name from all_user_table where schema_name = '{1}';" """,
        "oracle_columns": """{0} 2> /dev/null <<< "select column_name from  all_user_columns where table_name = '{1}';" """,
        "psql_tables": """{0} -c "select tablename from pg_tables where schemaname = 'public'" 2> /dev/null """,
        "psql_columns": """{0} -c "select column_name from information_schema.columns where table_name = {1}" 2> /dev/null """,
        "mysql_tables": """{0} -e 'SHOW tables;' 2> /dev/null """,
        "mysql_columns": """{0} -e 'SHOW COLUMNS FROM {1}' 2> /dev/null """
    }
    db_type = get_db_type(suggest_db)
    return (queries[db_type + "_tables"], queries[db_type + "_columns"])

def get_db_type(sugget_db):
    db_type = suggest_db.split(" ")[0]
    if(find(db_type,"sqlplus") != 0)
        return db_type
    else:
        return "oracle"

def get_table_names(suggest_db):
    get_tables_query, _ = get_db_specific_query_statements(suggest_db)
    #query_string = "{0} {1}".format(suggest_db, get_tables_query)
    schema_name = ""
    query_string = get_tables_query.format(suggest_db, schema_name)
    #tables = subprocess.check_output(query_string + " 2> /dev/null", shell=True)
    tables = subprocess.check_output(query_string, shell=True)
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
        if db_type == "mysql":
            #query_string = "{0} {1} {2}' 2> /dev/null".format(suggest_db, get_db_specific_query_statements(suggest_db)[1], table)
            query_string = get_db_specific_query_statements(suggest_db)[1].format(suggest_db, table)
            columns = subprocess.check_output(query_string, shell=True)
            table_cols.extend([{"word": prefix + column.split("\t")[0], "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[1:]])
        elif db_type == "psql":
            #query_string = "{0} {1} '{2}'\" 2> /dev/null".format(suggest_db, get_db_specific_query_statements(suggest_db)[1], table)
            query_string = get_db_specific_query_statements(suggest_db)[1].format(suggest_db, table)
            columns = subprocess.check_output(query_string, shell=True)
            table_cols.extend([{"word": prefix + column.strip(), "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[2:-1]])
        elif db_type == "oracle":
            #query_string = "{0} {1} '{2}'\" 2> /dev/null".format(suggest_db, get_db_specific_query_statements(suggest_db)[1], table)
            query_string = get_db_specific_query_statements(suggest_db)[1].format(suggest_db, table)
            columns = subprocess.check_output(query_string, shell=True)
            table_cols.extend([{"word": prefix + column.strip(), "menu": table, "dup": 1} for column in columns.rstrip().split("\n")[2:-1]])
    return table_cols


def get_column_names(suggest_db, word_to_complete):
    if word_to_complete.endswith("."):
        return create_column_name_list(suggest_db, [{"word": word_to_complete[:-1]}], ".")
    else:
        return create_column_name_list(suggest_db, get_table_names(suggest_db))
