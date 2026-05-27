from . import _types, key_generator
from .parsers import delimited_parser, scalar_parser


class KVPExpander:
    def __init__(
        self,
        parser_chain: tuple[_types.ValueParser, ...] = (delimited_parser.build(),),
        key_generator: _types.KeyGenerator = key_generator.build(),
        scalar_parser: _types.ScalarParser = scalar_parser.build(),
        recursive: bool = False,
    ):
        self.parser_chain: tuple[_types.ValueParser, ...] = parser_chain
        self.key_generator: _types.KeyGenerator = key_generator
        self.scalar_parser: _types.ScalarParser = scalar_parser
        self.recursive: bool = recursive

    def expand_key_value_pairs(
        self, mapping: dict[str, object]
    ) -> _types.ExpandedPairs:
        expanded: _types.ExpandedPairs = {}
        for key, value in mapping.items():
            expanded.update(self.expand_key_value_pair(key, value))
        return expanded

    def expand_key_value_pair(
        self, original_key: str, original_value: object
    ) -> _types.ExpandedPairs:
        if not isinstance(original_value, str):
            return {}

        if self.recursive:
            return self._expand_recursive(original_key, original_value)
        else:
            parsed = self._run_parser_chain(original_value)
            if parsed is None:
                return {}

            expanded: _types.ExpandedPairs = {}
            for child_key, child_value in parsed.items():
                expanded_key = self.key_generator(original_key, child_key)
                expanded[expanded_key] = self.scalar_parser(child_value)
            return expanded

    def _expand_recursive(
        self, original_key: str, original_value: str
    ) -> _types.ExpandedPairs:
        expanded: _types.ExpandedPairs = {}
        parsed = self._run_parser_chain(original_value)

        if parsed is None:
            return {}

        for child_key, child_value in parsed.items():
            expanded_key = self.key_generator(original_key, child_key)

            nested = self._expand_recursive(expanded_key, child_value)
            if nested:
                expanded.update(nested)
            else:
                expanded[expanded_key] = self.scalar_parser(child_value)

        return expanded

    def _run_parser_chain(self, value: str) -> _types.ParsedPairs | None:
        for parser in self.parser_chain:
            parsed = parser(value)

            if parsed is not None:
                return parsed
        return None
