import unittest

import kvpexpand.parsers.scalar_parser as scalar_parser
import kvpexpand.constants as constants


class TestScalarParserConfig(unittest.TestCase):
    def test_default_config(self):
        config = scalar_parser.ScalarParserConfig()
        self.assertEqual(config.literal_map, constants.DEFAULT_LITERAL_MAP)
        self.assertTrue(config.parse_numbers)
        self.assertEqual(config.float_identifiers, constants.DEFAULT_FLOAT_IDENTIFIERS)


class TestScalarParser(unittest.TestCase):
    def setUp(self):
        self.parser = scalar_parser.build()

    def test_parse_true_strings_in_default_literal_map(self):
        result = self.parser("TRUE")
        self.assertEqual(result, True)
        result = self.parser("true")
        self.assertEqual(result, True)

    def test_parse_false_strings_in_default_literal_map(self):
        result = self.parser("FALSE")
        self.assertEqual(result, False)
        result = self.parser("false")
        self.assertEqual(result, False)

    def test_parse_null_strings_in_default_literal_map(self):
        result = self.parser("NULL")
        self.assertEqual(result, None)
        result = self.parser("null")
        self.assertEqual(result, None)

    def test_parse_strings_in_custom_literal_map(self):
        literal_map = {"none": None}
        config = scalar_parser.ScalarParserConfig(literal_map=literal_map)
        parser = scalar_parser.build(config)

        result = parser("NONE")
        self.assertEqual(result, None)

        result = parser("none")
        self.assertEqual(result, None)

    def test_parse_string_not_in_literal_map(self):
        result = self.parser("NOT_IN_MAP")
        self.assertEqual(result, "NOT_IN_MAP")

    def test_parse_integer(self):
        result = self.parser("42")
        self.assertEqual(result, 42)

    def test_parse_float_with_dot_notation(self):
        result = self.parser("3.14")
        self.assertEqual(result, 3.14)

    def test_parse_float_with_e_notation(self):
        result = self.parser("1e10")
        self.assertEqual(result, 1e10)

    def test_parse_float_with_E_notation(self):
        result = self.parser("1E10")
        self.assertEqual(result, 1e10)

    def test_parse_string_with_float_identifier(self):
        result = self.parser("TEST")
        self.assertEqual(result, "TEST")

    def test_parse_float_with_custom_notation(self):
        float_identifiers = ["inf"]
        config = scalar_parser.ScalarParserConfig(float_identifiers=float_identifiers)
        parser = scalar_parser.build(config)

        result = parser("inf")
        self.assertEqual(result, float("inf"))

    def test_parse_numbers_as_strings(self):
        config = scalar_parser.ScalarParserConfig(parse_numbers=False)
        parser = scalar_parser.build(config)

        result = parser("42")
        self.assertEqual(result, "42")
