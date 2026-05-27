from dataclasses import dataclass

from kvpexpand import constants, _types


@dataclass(frozen=True)
class DelimitedParserConfig:
    delimiters: tuple[str, ...] = constants.DEFAULT_DELIMITERS
    separator: str = constants.DEFAULT_KVP_SEPARATOR
    wrappers: tuple[tuple[str, str], ...] = constants.DEFAULT_WRAPPERS
    trim_wrappers: bool = True


def build(
    config: DelimitedParserConfig = DelimitedParserConfig(),
) -> _types.ValueParser:

    def parser(raw_value: str) -> _types.ParsedPairs | None:
        normalized = raw_value.strip()
        if config.trim_wrappers:
            for left, right in config.wrappers:
                if normalized.startswith(left) and normalized.endswith(right):
                    normalized = normalized[
                        len(left) : len(normalized) - len(right)
                    ].strip()
                    break

        for delimiter in config.delimiters:
            if delimiter not in normalized:
                continue
            parsed = _parse_chunks(
                [chunk.strip() for chunk in normalized.split(delimiter)],
                config.separator,
            )
            if parsed is not None:
                return parsed

        if normalized.count(config.separator) == 1:
            return _parse_chunks([normalized], config.separator)

        return None

    return parser


def _parse_chunks(
    chunks: list[str], key_value_separator: str
) -> _types.ParsedPairs | None:
    parsed: _types.ParsedPairs = {}
    for chunk in chunks:
        if key_value_separator not in chunk:
            return None
        child_key, child_value = chunk.split(key_value_separator, 1)
        parsed[child_key.strip()] = child_value.strip()
    return parsed or None
