from typing import Optional

import msgspec
import msgspec.json

class Var(msgspec.Struct):
    name: str
    type: str
    params: dict = {}
    inject_vars: Optional[bool] = None
    depends_on: list[str] = []


class Match(msgspec.Struct):
    label: Optional[str] = None
    trigger: Optional[str] = None
    triggers: Optional[list[str]] = None
    regex: Optional[str] = None

    replace: Optional[str] = None
    image_path: Optional[str] = None

    form: Optional[str] = None
    form_fields: dict = {}

    vars: list[Var] = []

    word: Optional[bool] = None
    left_word: Optional[bool] = None
    propagate_case: Optional[bool] = None
    uppercase_style: Optional[bool] = None
    force_clipboard: Optional[bool] = None
    paragraph: Optional[bool] = None

    force_mode: Optional[str] = None
    markdown: Optional[str] = None
    html: Optional[str] = None

    search_terms: list[str] = []


class MatchGroup(msgspec.Struct):
    imports: list[str] = []
    global_vars: list[Var] = []
    matches: list[Match] = []

print(msgspec.json.encode(msgspec.json.schema(MatchGroup)))