DEFAULT_FLOAT_IDENTIFIERS = (".", "e", "E")
DEFAULT_DELIMITERS = (",",)
DEFAULT_KVP_SEPARATOR = "="
DEFAULT_WRAPPERS = (("(", ")"), ("[", "]"), ("{", "}"))
DEFAULT_LITERAL_MAP = {
    "true": True,
    "false": False,
    "null": None,
}
DEFAULT_REGEX_PATTERN = r"([^,=]+)=([^=,\n]+)"
DEFAULT_REGEX_KEY_GROUP = 1
DEFAULT_REGEX_VALUE_GROUP = 2
DEFAULT_KEY_SEPARATOR = "_"
DEFAULT_KEY_TEMPLATE = "{original}_{child}"
