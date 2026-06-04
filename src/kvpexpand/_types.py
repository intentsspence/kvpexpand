from typing import Callable

ParsedPairs = dict[str, str]
ExpandedPairs = dict[str, object]
ValueParser = Callable[[object], ParsedPairs | None]
ScalarParser = Callable[[object], object]
KeyGenerator = Callable[[str, str], str]
