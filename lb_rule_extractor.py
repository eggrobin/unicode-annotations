from collections import Counter
from historical_diff import Version
from document import Paragraph, Heading, Rule, Formula, TableRow
import glob
import html
from html.parser import HTMLParser
import pprint
import re
import sys

revisions = {int(re.search(r"-(\d+).html", filename).group(1)): filename
             for filename in glob.glob("tr14-*.html")}

def parse_version(s):
  match = re.match(r"(?:Unicode )?(\d+)\.(\d)\.(\d)", s)
  if match:
    return Version(*(int(v) for v in match.groups()))

ID_REMAPPINGS = {
  "Line Breaking Algorithm": "Algorithm",
  "ResolveLineBreakClasses": "ResolveLineBreakingClasses",
  "ConjoiningJamo": "KoreanSyllableBlocks",
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
    self.in_algorithm = False
    self.version = version

  def handle_starttag(self, tag, attrs):
    if tag == "tr":
      self.end_line()
      self.line_tag = tag
    if tag == "br":
      self.handle_data("\u2028")
      return
    attrs = dict(attrs)
    if tag == "b":
      self.bold = True
    if tag in ("td", "th") and self.line.strip():
      self.line = self.line.rstrip() + '\uE000'
    if tag == "p" or re.match(r"h\d", tag):
      self.end_line()
      self.line_tag = tag
      if (("align", "center") in attrs.items() or
          ("style", "text-align:center") in attrs.items()):
        self.centred = True
    elif tag == "a" and self.line_tag and self.line_tag.startswith("h") and "id" in attrs or "name" in attrs:
      self.line_id = attrs.get("id") or attrs.get("name")
      self.line_id = ID_REMAPPINGS.get(self.line_id) or self.line_id

  def handle_endtag(self, tag):
    if tag == "b":
      self.bold = False
    if tag == "h2":
      self.in_algorithm = "algorithm" in self.line.casefold()
    if tag == "p" or re.match(r"h\d", tag):
      self.end_line()

  def handle_data(self, data):
    if not self.version:
      self.version = parse_version(data)
    if data.strip() and not self.bold:
      self.line_is_all_bold = False
    if self.line.endswith("\uE000"):
      self.line += data.lstrip()
    else:
      self.line += data

  def end_line(self):
    self.line = re.sub(r'\s+', ' ', self.line.strip())
    if not self.line:
      return
    
    if self.in_algorithm:
      if not self.line_tag:
        raise ValueError("Stray text: %s" % self.line)
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
      elif self.line.startswith("LB"):
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
    parser = TR14Parser(Version(3,0,0) if revision == 6 else None)
    parser.feed(f.read())
    paragraphs[parser.version] = parser.paragraphs
    print(f"Unicode Version {parser.version}, {len(parser.paragraphs)} paragraphs")

args = dict(arg[2:].split("=", 1) for arg in sys.argv[1:] if arg.startswith("--"))
if "out" in args:
  f = open(args["out"], "w", encoding="utf-8")
else:
  f = sys.stdout
pprint.PrettyPrinter(sort_dicts=False, stream=f).pprint(paragraphs)
