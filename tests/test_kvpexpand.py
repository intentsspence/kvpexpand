import unittest

import kvpexpand.kvpexpand as kvpexpand
import kvpexpand.parsers as parsers


class TestKVPExpander(unittest.TestCase):
    def setUp(self):
        self.kvpexpander = kvpexpand.KVPExpander()
        self.key = "test_key"
        self.value = "sub_key1=sub_value1,sub_key2=sub_value2"
        self.key_value_pairs = {self.key: self.value}

    def test_expand_key_value_pair(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, self.value)
        expected = {
            "test_key_sub_key1": "sub_value1",
            "test_key_sub_key2": "sub_value2",
        }
        self.assertEqual(result, expected)

    def test_expand_key_value_pairs(self):
        result = self.kvpexpander.expand_key_value_pairs(self.key_value_pairs)
        expected = {
            "test_key_sub_key1": "sub_value1",
            "test_key_sub_key2": "sub_value2",
        }
        self.assertEqual(result, expected)

    def test_expand_key_value_pair_with_no_match(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, "sub_key3:sub_value3")
        expected = {}
        self.assertEqual(result, expected)

    def test_expand_key_value_pair_with_non_string_value(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, 123)
        expected = {}
        self.assertEqual(result, expected)


class TestRecursiveKVPExpander(unittest.TestCase):
    def setUp(self):
        delimiters = [";", ","]
        delimited_parser_config = parsers.delimited_parser.DelimitedParserConfig(
            delimiters=delimiters
        )
        delimited_parser = parsers.delimited_parser.build(delimited_parser_config)
        self.kvpexpander = kvpexpand.KVPExpander(
            parser_chain=(delimited_parser,),
            recursive=True,
        )
        self.key = "test_key"
        self.value = "sub_key1=sub_sub_key1=sub_sub_value1,sub_sub_key2=sub_sub_value2;sub_key2=sub_value2"  # noqa: E501
        self.key_value_pairs = {self.key: self.value}

    def test_expand_key_value_pair(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, self.value)
        expected = {
            "test_key_sub_key1_sub_sub_key1": "sub_sub_value1",
            "test_key_sub_key1_sub_sub_key2": "sub_sub_value2",
            "test_key_sub_key2": "sub_value2",
        }
        self.assertEqual(result, expected)

    def test_expand_key_value_pair_with_no_match(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, "sub_key3:sub_value3")
        expected = {}
        self.assertEqual(result, expected)

    def test_expand_key_value_pair_with_non_string_value(self):
        result = self.kvpexpander.expand_key_value_pair(self.key, 123)
        expected = {}
        self.assertEqual(result, expected)

    def test_expand_key_value_pairs(self):
        result = self.kvpexpander.expand_key_value_pairs(self.key_value_pairs)
        expected = {
            "test_key_sub_key1_sub_sub_key1": "sub_sub_value1",
            "test_key_sub_key1_sub_sub_key2": "sub_sub_value2",
            "test_key_sub_key2": "sub_value2",
        }
        self.assertEqual(result, expected)
