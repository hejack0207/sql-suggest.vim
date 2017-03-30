from vim_sql_suggest import *

import os
import sys
import unittest

class RunPTestCase(unittest.TestCase):
    def setUp(self):
        print("setup ...")

    def test_get_db_type_sqlplus(self):
        db_type = get_db_type("sqlplus64 sys/password")
        self.assertEquals(db_type, "oracle")

    def test_get_db_type_sqlplus2(self):
        db_type = get_db_type("sqlplus")
        self.assertEquals(db_type, "oracle")

if __name__ == '__main__':
    unittest.main()
