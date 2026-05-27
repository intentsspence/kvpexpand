import unittest

import kvpexpand.parsers.regex_parser as regex_parser
import kvpexpand.constants as constants


class TestRegexParserConfig(unittest.TestCase):
    def setUp(self):
        self.parser = regex_parser.build()

    def test_default_config(self):
        config = regex_parser.RegexParserConfig()
        self.assertEqual(config.pattern, constants.DEFAULT_REGEX_PATTERN)
        self.assertEqual(config.key_group, constants.DEFAULT_REGEX_KEY_GROUP)
        self.assertEqual(config.value_group, constants.DEFAULT_REGEX_VALUE_GROUP)

    def test_parse_matching_regex_string_with_multiple_pairs(self):
        result = self.parser("key1=value1,key2=value2")
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    def test_parse_matching_regex_string_with_single_pair(self):
        result = self.parser("key1=value1")
        self.assertEqual(result, {"key1": "value1"})

    def test_parse_matching_regex_string_with_invalid_key(self):
        pattern = r"([\s]+)=([^=,\n]+)"
        config = regex_parser.RegexParserConfig(pattern=pattern)
        parser = regex_parser.build(config)
        result = parser(" =value1")
        self.assertEqual(result, None)

    def test_parse_non_matching_regex_string(self):
        result = self.parser("key1value1")
        self.assertEqual(result, None)
