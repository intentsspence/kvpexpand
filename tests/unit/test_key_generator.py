import unittest

import kvpexpand.key_generator as key_generator
import kvpexpand.constants as constants


class TestKeyGeneratorConfig(unittest.TestCase):
    def test_default_config(self):
        config = key_generator.KeyGeneratorConfig()
        self.assertEqual(config.mode, key_generator.KeyGeneratorMode.PREFIX)
        self.assertEqual(config.separator, constants.DEFAULT_KEY_SEPARATOR)
        self.assertEqual(config.template, constants.DEFAULT_KEY_TEMPLATE)
        self.assertEqual(config.custom_builder, None)


class TestKeyGenerator(unittest.TestCase):
    def setUp(self):
        self.original_key = "original"
        self.child_key = "child"

    def build_and_generate_key(self, config: key_generator.KeyGeneratorConfig):
        return key_generator.build(config)(self.original_key, self.child_key)

    def test_prefix_key_generator(self):
        expected_key = (
            f"{self.original_key}{constants.DEFAULT_KEY_SEPARATOR}{self.child_key}"
        )
        mode = key_generator.KeyGeneratorMode.PREFIX
        key_generator_config = key_generator.KeyGeneratorConfig(mode=mode)
        generated_key = self.build_and_generate_key(key_generator_config)
        self.assertEqual(generated_key, expected_key)

    def test_suffix_key_generator(self):
        expected_key = (
            f"{self.child_key}{constants.DEFAULT_KEY_SEPARATOR}{self.original_key}"
        )
        mode = key_generator.KeyGeneratorMode.SUFFIX
        key_generator_config = key_generator.KeyGeneratorConfig(mode=mode)
        generated_key = self.build_and_generate_key(key_generator_config)
        self.assertEqual(generated_key, expected_key)

    def test_child_only_key_generator(self):
        expected_key = f"{self.child_key}"
        mode = key_generator.KeyGeneratorMode.CHILD_ONLY
        key_generator_config = key_generator.KeyGeneratorConfig(mode=mode)
        generated_key = self.build_and_generate_key(key_generator_config)
        self.assertEqual(generated_key, expected_key)

    def test_template_key_generator(self):
        expected_key = f"{self.original_key}_{self.child_key}"
        mode = key_generator.KeyGeneratorMode.TEMPLATE
        key_generator_config = key_generator.KeyGeneratorConfig(mode=mode)
        generated_key = self.build_and_generate_key(key_generator_config)
        self.assertEqual(generated_key, expected_key)

    def test_custom_builder_key_generator(self):
        expected_key = f"{self.original_key}{self.child_key}"

        def custom_builder(original, child):
            return f"{original}{child}"

        key_generator_config = key_generator.KeyGeneratorConfig(
            mode=key_generator.KeyGeneratorMode.CUSTOM, custom_builder=custom_builder
        )
        generated_key = self.build_and_generate_key(key_generator_config)
        self.assertEqual(generated_key, expected_key)

    def test_custom_builder_mode_without_custom_builder(self):
        with self.assertRaises(ValueError):
            key_generator.KeyGeneratorConfig(mode=key_generator.KeyGeneratorMode.CUSTOM)

    def test_unsupported_key_generation_mode(self):
        with self.assertRaises(ValueError):
            key_generator_config = key_generator.KeyGeneratorConfig(
                mode="unsupported_mode"
            )
            self.build_and_generate_key(key_generator_config)
