#!/usr/bin/env python3
import collections

import inflection
import parsley

__all__ = ["_AttributesFromJson", "markdown_to_ansi"]

GRAMMAR_FUNCTIONS = {
    "bold": "\033[1m{}\033[0m".format,
    "italic": "\033[3m{}\033[0m".format,
    "header": "\033[4m{}\033[0m".format,
    "code": "\033[32m{}\033[0m".format,
    # TODO: Add some sort of highlighting
    "multiline_code": lambda c, _: GRAMMAR_FUNCTIONS["code"](c)
}
MARKDOWN_GRAMMAR = parsley.makeGrammar("""
nonspecial = anything:x ?(x not in '*_`') -> x
bold = '*' '*' <nonspecial+>:x '*' '*' -> bold(x)
italic = '_' <nonspecial+>:x '_' -> italic(x)
header = ('#' <anything+>:x | <anything+>:y '\n' '='+) -> header(x or y)
code = '`' <nonspecial+>:x '`' -> code(x)
multiline_code = '`'{3} <anything*>:lang '\n' <anything*>:code '\n' '`'{3} -> multiline_code(code, lang)
text = (header | bold | italic | code | multiline_code | <nonspecial+>)+
""", GRAMMAR_FUNCTIONS)


class _AttributesFromJson(object):
    attr_keys = []

    def __init__(self, json_data):
        for key in self.attr_keys:
            tree = key.split("/")
            leaf = tree.pop()
            look_in = json_data
            for inner_key in tree:
                look_in = look_in[inner_key]
            setattr(self, inflection.underscore(leaf), look_in[leaf])


def markdown_to_ansi(md_text):
    return "".join(MARKDOWN_GRAMMAR(md_text).text())
