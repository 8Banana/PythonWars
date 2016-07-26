#!/usr/bin/env python3
import colorama
import inflection
import mistune
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

__all__ = ["_AttributesFromJson", "markdown_to_ansi"]


class AnsiRenderer(mistune.Renderer):
    def block_code(self, code, language=None):
        if not language:
            return "\n<pre><code>{}</code></pre>\n".format(mistune.escape(code))
        lexer = get_lexer_by_name(language, stripall=True)
        return pygments.highlight(code, lexer, TerminalFormatter())

    # MISSING: block_quote(text), block_html(html)

    def header(self, text, level, raw=None):
        # TODO: Care about level?
        return colorama.Style.BRIGHT + text + colorama.Style.RESET_ALL + "\n"

    # MISSING: hrule()

    def list(self, body, ordered=True):
        items = body.splitlines()
        if ordered:
            return "\n".join("{}. {}".format(i, x)
                             for i, x in enumerate(items, start=1)) + "\n"
        else:
            return "\n".join("* {}".format(x) for x in items) + "\n"

    def list_item(self, text):
        return text + "\n"

    def paragraph(self, text):
        return text + "\n"

    # MISSING: table(header, body), table_row(content), table_cell(content,
    # **flags)

    def autolink(self, link, is_email=False):
        return "<{}>".format(link)

    def codespan(self, text):
        return colorama.Fore.GREEN + text + colorama.Style.RESET_ALL + "\n"

    def double_emphasis(self, text):
        return colorama.Fore.BRIGHT + text + colorama.Style.RESET_ALL + "\n"

    def emphasis(self, text):
        return colorama.Fore.BRIGHT + text + colorama.Style.RESET_ALL + "\n"

    def image(self, src, title, alt_text):
        # XXX: What should we do here?
        return colorama.Fore.RED + alt_text + colorama.Style.RESET_ALL + "\n"

    def linebreak(self):
        return "\n"

    def newline(self):
        return "\n"

    def link(self, link, title, content):
        # XXX: What should we do here?
        return "{} ({})".format(content, link) + "\n"

    def strikethrough(self, text):
        return colorama.Style.STRIKE + text + colorama.Style.RESET_ALL + "\n"

    def text(self, text):
        return text

    def inline_html(self, text):
        return self.code(text)


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
    return mistune.markdown(md_text, renderer=AnsiRenderer())
