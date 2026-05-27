from dataclasses import dataclass
from enum import Enum

from . import _types, constants


class KeyGeneratorMode(str, Enum):
    PREFIX = "prefix"
    SUFFIX = "suffix"
    CHILD_ONLY = "child_only"
    TEMPLATE = "template"
    CUSTOM = "custom"


@dataclass(frozen=True)
class KeyGeneratorConfig:
    mode: KeyGeneratorMode = KeyGeneratorMode.PREFIX
    separator: str = constants.DEFAULT_KEY_SEPARATOR
    template: str = constants.DEFAULT_KEY_TEMPLATE
    custom_builder: _types.KeyGenerator | None = None

    def __post_init__(self):
        if self.mode == KeyGeneratorMode.CUSTOM and self.custom_builder is None:
            raise ValueError("custom_builder attribute is required for CUSTOM mode")


def build(config: KeyGeneratorConfig = KeyGeneratorConfig()) -> _types.KeyGenerator:
    if config.mode == KeyGeneratorMode.CUSTOM:
        assert config.custom_builder is not None
        return config.custom_builder

    if config.mode == KeyGeneratorMode.PREFIX:
        return lambda original, child: f"{original}{config.separator}{child}"

    if config.mode == KeyGeneratorMode.SUFFIX:
        return lambda original, child: f"{child}{config.separator}{original}"

    if config.mode == KeyGeneratorMode.CHILD_ONLY:
        return lambda _, child: child

    if config.mode == KeyGeneratorMode.TEMPLATE:
        return lambda original, child: config.template.format(
            original=original, child=child
        )

    raise ValueError(f"Unsupported key generation mode: {config.mode}")
