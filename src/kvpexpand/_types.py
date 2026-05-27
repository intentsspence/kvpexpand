from typing import Callable

ParsedPairs = dict[str, str]
ExpandedPairs = dict[str, object]
ValueParser = Callable[[str], ParsedPairs | None]
ScalarParser = Callable[[str], object]
KeyGenerator = Callable[[str, str], str]
