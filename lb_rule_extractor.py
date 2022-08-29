from collections import Counter
import glob
from html.parser import HTMLParser
import pprint
import re
import sys

revisions = {int(re.search(r"-(\d+).html", filename).group(1)): filename
             for filename in glob.glob("tr14-*.html")}

def parse_version(s):
  match = re.match(r"(?:Unicode )?(\d+)\.(\d)\.(\d)", s)
  if match:
    return tuple(int(v) for v in match.groups())

def pretty_version(version):
  return ".".join(str(v) for v in version)

ID_REMAPPINGS = {
  "Line Breaking Algorithm": "Algorithm",
  "ResolveLineBreakClasses": "ResolveLineBreakingClasses",
  "ConjoiningJamo": "KoreanSyllableBlocks",
}

class TR14Parser(HTMLParser):
  def __init__(self, version=None):
    super().__init__()
    self.line_tag = None
    self.line_id = None
    self.line = ""
    self.line_is_all_bold = True
    self.bold = False
    self.clauses = []
    self.in_algorithm = False
    self.version = version
    self.heading_enumerators = Counter()

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    if tag == "b":
      self.bold = True
    if tag in ("p", "table") or re.match(r"h\d", tag):
      self.end_line()
      self.line_tag = tag
      if self.clauses and (("align", "center") in attrs.items() or
                           ("style", "text-align:center") in attrs.items()):
        if len(self.clauses) % 2 != 0:
          self.clauses[-1][1][1]
    elif tag == "a" and self.line_tag and self.line_tag.startswith("h") and "id" in attrs or "name" in attrs:
      self.line_id = attrs.get("id") or attrs.get("name")
      self.line_id = ID_REMAPPINGS.get(self.line_id) or self.line_id

  def handle_endtag(self, tag):
    if tag == "b":
      self.bold = False
    if tag == "h2":
      self.in_algorithm = "algorithm" in self.line.casefold()
    if tag in ("p", "table") or re.match(r"h\d", tag):
      self.end_line()

  def handle_data(self, data):
    if not self.version:
      self.version = parse_version(data)
    if data.strip() and not self.bold:
      self.line_is_all_bold = False
    self.line += data

  def end_line(self):
    self.line = re.sub(r'\s+', ' ', self.line.strip())
    if not self.line:
      return
    
    if self.in_algorithm:
      if not self.line_tag:
        raise ValueError("Stray text: %s" % self.line)
      if self.line_tag.startswith("h"):
        tag = self.line_tag
        id = self.line_id
        if self.line_tag == "h4" and not id and self.version <= (4, 0, 1):
          tag = "h3"
          id = "BreakingRules"
        if id == "BreakingRules" and self.version <= (4, 1, 1):
          # That heading disappeared into the middle of the introductory text,
          # and the id was reused for the non-tailorable part.
          # let’s pretend it wasn’t a heading.
          self.clauses[-1][1][1].append(self.line)
        else:          
          self.heading_enumerators[tag] += 1
          self.clauses.append((tag.upper() + (id or str(self.heading_enumerators[tag])), (self.line, [])))
      elif self.line_is_all_bold:
        id = self.line.title().replace(" ", "").replace(":", "").replace(".", "").replace(",", "")
        id = ID_REMAPPINGS.get(id) or id
        self.clauses.append(("H4" + id, (self.line, [])))
      elif self.line.startswith("LB"):
        rule_number = re.match(r"LB\s*(\d+[a-z]?)", self.line).group(1)
        rule_description = self.line# re.search(r"LB\s*\d+[a-z]?\s*(.*)", self.line).group(1)
        if True or not (rule_description.startswith("Withdrawn.") or
                rule_description.startswith("[replaced") or
                rule_description.startswith("[deprecated")):
          self.clauses.append(("LB" + rule_number, (rule_description, [])))
      else:
        self.clauses[-1][1][1].append(self.line)
    self.line = ""
    self.line_id = None
    self.line_tag = None
    self.line_is_all_bold = True



clauses = {}

for revision, filename in sorted(revisions.items()):
  print(filename)
  with open(filename, encoding=('cp1252' if revision < 10 else'utf-8')) as f:
    parser = TR14Parser(version=(3,0,0) if revision == 6 else None)
    parser.feed(f.read())
    clauses[parser.version] = dict(parser.clauses)
    print(f"Unicode Version {pretty_version(parser.version)}, {len(parser.clauses)} clauses:");
    print(", ".join(clauses[parser.version].keys()) + ".")

args = dict(arg[2:].split("=", 1) for arg in sys.argv[1:] if arg.startswith("--"))
if "out" in args:
  f = open(args["out"], "w", encoding="utf-8")
else:
  f = sys.stdout
pprint.PrettyPrinter(sort_dicts=False, stream=f).pprint(clauses)
