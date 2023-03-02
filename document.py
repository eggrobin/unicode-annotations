import re

class Paragraph:
  def __init__(self, contents: str):
    self.contents = contents

  def __repr__(self):
    return f"{type(self).__name__}({', '.join(f'{key}={value!r}' for key, value, in self.__dict__.items())})"

  def html(self, inner, version=None):
    return f"<p>{inner}</p>"

  def words(self):
    # TODO(egg): Look at UAX #29.
    return re.split(r"\b|(?<=\W)(?=\W)|(?=ing\b)|(?<=\uE000)|(?=\uE000)", self.contents)

class Heading(Paragraph):
  def __init__(self, level: int, contents: str):
    self.level = level
    super(Heading, self).__init__(contents)

  def html(self, inner, version=None):
    return f"<h{self.level}>{inner}</h{self.level}>"

class Rule(Paragraph):
  def html(self, inner, version=None):
    return f"<p class=rule>{inner}</p>"

class Formula(Paragraph):
  def html(self, inner, version=None):
    return f"<p class=formula>{inner}</p>"

class TableRow(Paragraph):
  def html(self, inner, version=None):
    return f"<table><tr><td>{inner}</td></tr></table>"

class CodeLine(Paragraph):
  def html(self, inner, version=None):
    return f"<pre><code>{inner}</code></pre>"
