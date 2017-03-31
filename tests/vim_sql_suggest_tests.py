import unittest
from mock import patch

import autoload.vim_sql_suggest as sut


class VimSqlSuggestTests(unittest.TestCase):

    def test_get_db_type_sqlplus64(self):
        db_type = sut.get_db_type("sqlplus64 sys/password")
        self.assertEquals(db_type, "oracle")

    def test_get_db_type_sqlplus(self):
        db_type = sut.get_db_type("sqlplus")
        self.assertEquals(db_type, "oracle")

    def test_check_command_output(self):
        output = sut.check_command_output("""cat <<< "hi" """)
        self.assertEquals(output, "hi\n")

    def test_get_db_specific_query_statuments_with_mysql_database_connection(self):
        table_query, column_query = sut.get_db_specific_query_statements("mysql -u root test")
        self.assertEqual(table_query,sut.MYSQL_TABLES_QUERY)
        self.assertEqual(column_query, sut.MYSQL_COLUMNS_QUERY)

    def test_get_db_specific_query_statuments_with_psql_database_connection(self):
        table_query, column_query = sut.get_db_specific_query_statements("psql -U Jrock test")
        self.assertEqual(table_query, sut.PSQL_TABLES_QUERY)
        self.assertEqual(column_query, sut.PSQL_COLUMNS_QUERY)

    @patch('subprocess.check_output')
    def test_get_table_names_for_oracle(self, sb_output):
        sb_output.return_value = "Tables_in_test\ntable1\ntable2\ntable3"
        table_list = sut.get_table_names("sqlplus64 test/12345678:192.168.0.1:1251/orcl")
        self.assertEqual(table_list, [{"word": "table1"}, {"word": "table2"}, {"word": "table3"}])

    @patch('subprocess.check_output')
    def test_get_table_names_for_mysql(self, sb_output):
        sb_output.return_value = "Tables_in_test\ntable1\ntable2\ntable3"
        table_list = sut.get_table_names("mysql -u root test")
        self.assertEqual(table_list, [{"word": "table1"}, {"word": "table2"}, {"word": "table3"}])

    @patch('subprocess.check_output')
    def test_get_table_names_for_psql(self, sb_output):
        sb_output.return_value = " tablename\n----------\n table1\n table2\n table3\n(3 rows)"
        table_list = sut.get_table_names("psql -U Jrock test")
        self.assertEqual(table_list, [{"word": "table1"}, {"word": "table2"}, {"word": "table3"}])

    @patch('subprocess.check_output')
    def test_get_column_names_for_mysql(self, sb_output):
        with patch('subprocess.check_output', side_effect=["Tables_in_test\ntable1\ntable2",
                                                           "Field\tType\tNull\tKey\tDefault\tExtra\nid\tint(11)\tNO\tPRI\tNULL\tauto_increment\nthing\tvarchar(100)\tNO\tNULL\t",
                                                           "Field\tType\tNull\tKey\tDefault\tExtra\nid\tint(11)\tNO\tPRI\tNULL\tauto_increment\nthing\tvarchar(100)\tNO\tNULL\t"]):
            col_list = sut.get_column_names("mysql -u root test", "dummy")
            expected_return_val = [{'dup': 1, 'menu': 'table1', 'word': 'id'},
                                   {'dup': 1, 'menu': 'table1', 'word': 'thing'},
                                   {'dup': 1, 'menu': 'table2', 'word': 'id'},
                                   {'dup': 1, 'menu': 'table2', 'word': 'thing'}]
            self.assertEqual(col_list, expected_return_val)

    @patch('subprocess.check_output')
    def test_get_column_names_for_psql(self, sb_output):
        with patch('subprocess.check_output', side_effect=[" tablename\n----------\n table1\n table2\n(2 rows)",
                                                           " column_name\n----------\n id\n thing\n(2 rows)",
                                                           " column_name\n----------\n id\n stuff\n(2 rows)"]):
            col_list = sut.get_column_names("psql -U Jrock test", "dummy")
            expected_return_val = [{'dup': 1, 'menu': 'table1', 'word': 'id'},
                                   {'dup': 1, 'menu': 'table1', 'word': 'thing'},
                                   {'dup': 1, 'menu': 'table2', 'word': 'id'},
                                   {'dup': 1, 'menu': 'table2', 'word': 'stuff'}]
            self.assertEqual(col_list, expected_return_val)

    @patch('subprocess.check_output')
    def test_get_column_names_for_mysql_when_word_to_complete_ends_with_a_dot(self, sb_output):
        with patch('subprocess.check_output', side_effect=["Field\tType\tNull\tKey\tDefault\tExtra\nid\tint(11)\tNO\tPRI\tNULL\tauto_increment\nthing\tvarchar(100)\tNO\tNULL\t",
                                                           "Field\tType\tNull\tKey\tDefault\tExtra\nid\tint(11)\tNO\tPRI\tNULL\tauto_increment\nthing\tvarchar(100)\tNO\tNULL\t"]):
            col_list = sut.get_column_names("mysql -u root test", "table1.")
            expected_return_val = [{'dup': 1, 'menu': 'table1', 'word': '.id'},
                                   {'dup': 1, 'menu': 'table1', 'word': '.thing'}]
            self.assertEqual(col_list, expected_return_val)

    @patch('subprocess.check_output')
    def test_get_column_names_for_psql_when_word_to_complete_ends_with_a_dot(self, sb_output):
        with patch('subprocess.check_output', side_effect=[" column_name\n----------\n id\n thing\n(2 rows)",
                                                           " column_name\n----------\n id\n stuff\n(2 rows)"]):
            col_list = sut.get_column_names("psql -U Jrock test", "table1.")
            expected_return_val = [{'dup': 1, 'menu': 'table1', 'word': '.id'},
                                   {'dup': 1, 'menu': 'table1', 'word': '.thing'}]
            self.assertEqual(col_list, expected_return_val)
