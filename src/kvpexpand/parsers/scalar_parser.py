from dataclasses import dataclass, field
from typing import Mapping

from .. import constants, _types


@dataclass(frozen=True)
class ScalarParserConfig:
    literal_map: Mapping[str, object] = field(
        default_factory=lambda: constants.DEFAULT_LITERAL_MAP.copy()
    )
    parse_numbers: bool = True
    float_identifiers: tuple[str, ...] = constants.DEFAULT_FLOAT_IDENTIFIERS


def build(config: ScalarParserConfig = ScalarParserConfig()) -> _types.ScalarParser:
    def parser(value: str) -> object:
        lowered = value.lower()

        # Check literal map first
        if lowered in config.literal_map:
            return config.literal_map[lowered]

        # Parse numbers if enabled
        if config.parse_numbers:
            try:
                if any(char in value for char in config.float_identifiers):
                    return float(value)
                return int(value)
            except ValueError:
                pass

        return value

    return parser
