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

class TR14Parser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.paragraph = ""
    self.in_rule = False
    self.rules = []
    self.in_algorithm = False
    self.version = None

  def handle_starttag(self, tag, attrs):
    if tag == "p" or re.match(r"h\d", tag):
      self.end_paragraph()
      if tag != "p" or not (("align", "center") in attrs or
                            ("style", "text-align:center") in attrs):
        self.in_rule = False

  def handle_endtag(self, tag):
    if tag == "h2":
      self.in_algorithm = "algorithm" in self.paragraph.casefold()
      self.in_rule &= self.in_algorithm
    if tag == "p" or re.match(r"h\d", tag):
      self.end_paragraph()

  def handle_data(self, data):
    if not self.version:
      self.version = parse_version(data)
    self.paragraph += data

  def end_paragraph(self):
    self.paragraph = re.sub(r'\s+', ' ', self.paragraph.strip())
    if not self.paragraph:
      return

    if self.in_algorithm and self.paragraph.startswith("LB"):
      rule_number = re.match(r"LB\s*(\d+[a-z]?)", self.paragraph).group(1)
      rule_description = re.search(r"LB\s*\d+[a-z]?\s*(.*)", self.paragraph).group(1)
      if not (rule_description.startswith("Withdrawn.") or
              rule_description.startswith("[replaced") or
              rule_description.startswith("[deprecated")):
        self.rules.append((rule_number, (rule_description, [])))
        self.in_rule = True
    elif self.in_rule:
      self.rules[-1][1][1].append(self.paragraph)
    self.paragraph = ""

rules = {}

for revision, filename in sorted(revisions.items()):
  print(filename)
  with open(filename, encoding=('cp1252' if revision < 10 else'utf-8')) as f:
    parser = TR14Parser()
    parser.feed(f.read())
    if revision == 6:
      parser.version = (3,0,0)
    rules[parser.version] = dict(parser.rules)
    print(f"Unicode Version {pretty_version(parser.version)}, {len(parser.rules)} rules:");
    print(", ".join(rules[parser.version].keys()) + ".")

args = dict(arg[2:].split("=", 1) for arg in sys.argv[1:] if arg.startswith("--"))
if "out" in args:
  f = open(args["out"], "w", encoding="utf-8")
else:
  f = sys.stdout
pprint.PrettyPrinter(sort_dicts=False, stream=f).pprint(rules)
