from collections import Counter
from typing import List, Tuple
from historical_diff import Version
from document import Paragraph, Heading, Rule, Formula, TableRow, CodeLine
import glob
import html
from html.parser import HTMLParser
import pprint
import re
import sys

revisions = {int(re.search(r"-(\d+).html", filename).group(1)): filename
             for filename in glob.glob("tr14-*.html")}

def parse_version(s):
  match = re.search(r"(?:Unicode )?(\d+)\.(\d)\.(\d)", s)
  if match:
    return Version(*(int(v) for v in match.groups()))

ID_REMAPPINGS = {
  "Line Breaking Algorithm": "Algorithm",
  "ResolveLineBreakClasses": "ResolveLineBreakingClasses",
  "ConjoiningJamo": "KoreanSyllableBlocks",
}

EXPECTED_STRAY_PARAGRAPHS = [
  "All line breaking classes are informative, except for the line breaking classes marked with a * in Table 1 Line Breaking Properties. The interpretation of characters with normative line breaking classes by all conforming implementations must be consistent with the specification of the normative property.",
  "Change from Revision 12:",
  "[Revision 11, being a proposed update, is superseded and no longer publicly available]",
  "[Revision 16, being a proposed update, is superseded and no longer publicly available. Only modifications between revisions 10 and 12 are tracked here.]",
  "[Revision 11, being a proposed update, is superseded and no longer publicly available. Only modifications between revisions 10 and 12 are tracked here.]",
  "UAX14-HL3. Override any rule in Section 6.2,Tailorable Line Breaking Rules, or add new rules to that section.",
  "Revision 18 being a proposed update, only changes between revisions 17 and 19 are noted here.",
  "Revision 16 being a proposed update, only changes between revisions 17 and 15 are noted here.",
  "Revision 11 being a proposed update, only changes between revisions 12 and 14 are noted here.",
  "Revision 11, being a proposed update, only changes between revisions 10 and 12 are noted here.]",
  "Note: To determine a break it is generally not sufficient to just test the two adjacent characters.",
  "Revisions 20 and 21 being a proposed update, only changes between revisions 19 and 22 are noted here.",
  "Revision 23 being a proposed update, only changes between revisions 22 and 24 are noted here.",
]

_NUMERALS = {
  "toc": lambda n: "",
  "ul": lambda n: "• ",
  "1": lambda n: str(n) + ". ",
  "a": lambda n: chr(ord("a") + n) + ". ",
  "A": lambda n: chr(ord("A") + n) + ". ",
  "i": lambda n: ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"][n] + ". ",
  "I": lambda n: ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][n] + ". ",
}

class TR14Parser(HTMLParser):
  def __init__(self, version=None):
    super().__init__()
    self.paragraphs = []
    self.line_tag = None
    self.line_id = None
    self.line = ""
    self.line_is_all_bold = True
    self.bold = False
    self.centred = False
    self.in_uax = False
    self.in_algorithm = False
    self.version = version
    self.removed_tag = None
    self.list_stack : List[Tuple[int, str]] = []

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    if "class" in attrs and "removed" in attrs["class"]:
      self.removed_tag = tag
      return
    if tag == "tr":
      self.end_line()
      self.line_tag = tag
    if tag == "br":
      self.handle_data("\u2028")
      return
    if tag == "b":
      self.bold = True
    if tag in ("td", "th") and self.line.strip():
      self.line = self.line.rstrip() + '\uE000'
    if tag in ("ol", "ul"):
      self.list_stack.append(
          (int(attrs.get("start", "1")) - 1,
           ("toc" if attrs.get("class", "") == "toc" else "ul") if tag == "ul"
           else attrs.get("type", "1")))
    if (tag in ("p", "li", "pre", "blockquote") and self.line_tag != "tr") or re.match(r"h\d", tag):
      self.end_line()
      self.line_tag = tag
      if (("align", "center") in attrs.items() or
          ("style", "text-align:center") in attrs.items()):
        self.centred = True
    if tag == "li" and not self.removed_tag:
      if not self.list_stack:
        print(self.paragraphs[-1])
      [i, t] = self.list_stack[-1]
      i += 1
      self.list_stack[-1] = (i, t)
      self.line += _NUMERALS[t](i)
    elif tag == "a" and self.line_tag and self.line_tag.startswith("h") and "id" in attrs or "name" in attrs:
      self.line_id = attrs.get("id") or attrs.get("name")
      self.line_id = ID_REMAPPINGS.get(self.line_id) or self.line_id

  def handle_endtag(self, tag):
    if self.removed_tag:
      if tag == self.removed_tag:
        self.removed_tag = None
      return
    if tag in ("ol", "ul"):
      self.list_stack.pop()
    if tag == "b":
      self.bold = False
    if re.match(r"h\d", tag):
      self.in_uax = True
    if tag == "h2":
      self.in_algorithm = self.line == "6 Line Breaking Algorithm"
    if (tag in ("p", "li", "pre") and self.line_tag != "tr") or tag == "tr" or re.match(r"h\d", tag):
      self.end_line()

  def handle_data(self, data):
    if self.removed_tag:
      return
    if not self.version:
      self.version = parse_version(data)
    if data.strip() and not self.bold:
      self.line_is_all_bold = False
    if self.line_tag == "tr" and self.line.endswith("\uE000"):
      self.line += data.lstrip()
    else:
      self.line += data

  def end_line(self):
    if not self.version:
      self.version = parse_version(self.line)
    if self.line_tag == "pre":
      for line in self.line.splitlines():
        self.paragraphs.append(CodeLine(html.unescape(line)))
    else:
      if re.fullmatch(r"•\s+", self.line):
        # Deal with <ul> <p> by sticking the bullet in the paragraph.
        return
      self.line = re.sub(r'\s+', ' ', self.line.strip())
      if not self.line:
        return
      if self.in_uax:
        if not self.line_tag:
          if self.line in EXPECTED_STRAY_PARAGRAPHS:
            self.line_tag = "p"
          else:
            print(self.paragraphs)
            raise ValueError("Stray text: %s\n%r" % (self.line, self.line))
        if self.line_tag == "tr":
          self.paragraphs.append(TableRow(self.line))
        elif self.line_tag.startswith("h"):
          tag = self.line_tag
          id = self.line_id
          if self.line_tag == "h4" and not id and self.version <= Version(4, 0, 1):
            tag = "h3"
            id = "BreakingRules"
          self.paragraphs.append(
            Heading(int(re.match(r"h(\d)", tag).group(1)), self.line))
        elif self.line_is_all_bold:
          id = self.line.title().replace(" ", "").replace(":", "").replace(".", "").replace(",", "")
          id = ID_REMAPPINGS.get(id) or id
          self.paragraphs.append(
            Heading(4, self.line))
        elif self.line.startswith("LB") and self.in_algorithm:
          self.paragraphs.append(
            Rule(self.line))
        elif self.centred:
          self.paragraphs.append(
            Formula(self.line))
        else:
          self.paragraphs.append(Paragraph(self.line))
    self.line = ""
    self.line_id = None
    self.line_tag = None
    self.line_is_all_bold = True
    self.centred = False



paragraphs = {}

for revision, filename in sorted(revisions.items()):
  print(filename)
  with open(filename, encoding=('cp1252' if revision < 10 else'utf-8')) as f:
    parser = TR14Parser(Version(3,0,0) if revision == 6 else
                        Version(16, 0, 0) if revision == 52 else
                        None)
    parser.feed(f.read())
    paragraphs[parser.version] = parser.paragraphs
    print(f"Unicode Version {parser.version}, {len(parser.paragraphs)} paragraphs")

args = dict(arg[2:].split("=", 1) for arg in sys.argv[1:] if arg.startswith("--"))
if "out" in args:
  f = open(args["out"], "w", encoding="utf-8")
else:
  f = sys.stdout
pprint.PrettyPrinter(sort_dicts=False, stream=f).pprint(paragraphs)
