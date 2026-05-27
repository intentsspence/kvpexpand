import unittest

import kvpexpand.parsers.delimited_parser as delimited_parser
import kvpexpand.constants as constants


class TestDelimitedParserConfig(unittest.TestCase):
    def test_default_config(self):
        config = delimited_parser.DelimitedParserConfig()
        self.assertEqual(config.delimiters, constants.DEFAULT_DELIMITERS)
        self.assertEqual(config.separator, constants.DEFAULT_KVP_SEPARATOR)
        self.assertEqual(config.wrappers, constants.DEFAULT_WRAPPERS)
        self.assertTrue(config.trim_wrappers)


class TestDelimitedParser(unittest.TestCase):
    def setUp(self):
        self.parser = delimited_parser.build()

    def test_parse_delimited_string_with_multiple_pairs(self):
        result = self.parser("key1=value1,key2=value2")
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    def test_parse_delimited_string_with_single_pair(self):
        result = self.parser("key1=value1")
        self.assertEqual(result, {"key1": "value1"})

    def test_parse_non_delimited_string(self):
        result = self.parser("key1value1")
        self.assertEqual(result, None)

    def test_parse_delimited_string_without_kvp_separator(self):
        result = self.parser("key1,value1")
        self.assertEqual(result, None)

    def test_parse_delimited_string_with_wrappers(self):
        result = self.parser("(key1=value1,key2=value2)")
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})


class TestDelimitedParserNoTrimWrappers(unittest.TestCase):
    def setUp(self):
        config = delimited_parser.DelimitedParserConfig(trim_wrappers=False)
        self.parser = delimited_parser.build(config=config)

    def test_parse_delimited_string_with_wrappers(self):
        result = self.parser("(key1=value1,key2=value2)")
        self.assertEqual(result, {"(key1": "value1", "key2": "value2)"})
