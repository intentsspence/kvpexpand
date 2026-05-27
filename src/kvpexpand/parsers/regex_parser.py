from dataclasses import dataclass
import re

from .. import _types, constants


@dataclass(frozen=True)
class RegexParserConfig:
    pattern: str = constants.DEFAULT_REGEX_PATTERN
    key_group: int | str = constants.DEFAULT_REGEX_KEY_GROUP
    value_group: int | str = constants.DEFAULT_REGEX_VALUE_GROUP


def build(config: RegexParserConfig = RegexParserConfig()) -> _types.ValueParser:
    pattern = re.compile(config.pattern)

    def parser(raw_value: str) -> _types.ParsedPairs | None:
        matches = list(pattern.finditer(raw_value))
        if not matches:
            return None

        parsed: _types.ParsedPairs = {}
        for match in matches:
            child_key = match.group(config.key_group).strip()
            child_value = match.group(config.value_group).strip()
            if not child_key:
                return None
            parsed[child_key] = child_value
        return parsed or None

    return parser
