import houdini as h
import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(
                h.escape_html(text.strip()))

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(m.smartypants(text), lexer, formatter)


def transfer(text):
    renderer = HighlighterRenderer()
    md = m.Markdown(renderer, extensions=('fenced-code',
                                          'tables',
                                          'no-intra-emphasis'))
    return md(text)
