import csv
from difflib import SequenceMatcher
import historical_diff
import re

def parse_version(s):
  match = re.match(r"(?:Unicode )?(\d+)\.(\d)\.(\d)", s)
  if match:
    return tuple(int(v) for v in match.groups())

def pretty_version(version):
  return ".".join(str(v) for v in version)

with open('renumberings.tsv') as f:
  rows = csv.reader(f, delimiter="\t")
  columns = [tuple(re.sub(r"LB|deprecated|removed", "", entry).strip() or None for entry in column) for column in zip(*rows)]
  TABLE_5_BY_COLUMNS = {parse_version(column[0]) : tuple(column[1:]) for column in columns}
  RENUMBERINGS = {parse_version(left[0]) : tuple(zip(left[1:], right[1:])) for left, right in zip(columns[:-1], columns[1:])}

splits = set()
creations = set()
deletions = set()

reorderings = set()

for version, renumbering in reversed(list(RENUMBERINGS.items())):
  mapping = dict(renumbering)
  reverse = {}
  for new, old in renumbering:
    if old:
      if new:
        reverse.setdefault(old, set()).add(new)
      else:
        deletions.add((version, old))
        print (f"RULE DELETION: {old} in {pretty_version(version)}")
    elif new:
      creations.add((version, new))
      print (f"RULE CREATION: {new} in {pretty_version(version)}")

  for old, new in reverse.items():
    if len(new) > 1:
      for n in new:
        splits.add((version, n))
      print (f"RULE SPLIT: {old} into ({', '.join(sorted(new))}) in {pretty_version(version)}")

  common = [(old, tuple(new)[0]) for old, new, in reverse.items() if len(new) == 1]
  old_order = sorted(common, key=lambda x: re.sub(r"^(\d)(?!\d)", r"0\1", x[0]))
  new_order = sorted(common, key=lambda x: re.sub(r"^(\d)(?!\d)", r"0\1", x[1]))
  if new_order != old_order:
    reorderings.add(version)
    print("REORDERING in", pretty_version(version))
    for i in range(len(old_order)):
      if new_order[i] != old_order[i]:
        break
    for j in range(len(old_order)):
      if new_order[-j] != old_order[-j]:
        break
    print("...", " ".join(old + "↦" + new for old, new in old_order[i:-j+1]), "...")
    print("...", " ".join(old + "↦" + new for old, new in new_order[i:-j+1]), "...")


with open("rules.py", encoding="utf-8") as f:
  VERSIONS = eval(f.read())

def make_sequence_history(v, s):
  h = historical_diff.SequenceHistory()
  h.add_version(v, s)
  return h

history = historical_diff.SequenceHistory(element_history=make_sequence_history)

PRESERVED_PARAGRAPHS = {
  (4, 0, 0): [(3,), (27,)],
}

for version, clauses in VERSIONS.items():
  paragraphs = []
  for title, subclauses in clauses.values():
    paragraphs.append(re.split(r"\b|(?<=\W)(?=\W)", title))
    paragraphs.extend(re.split(r"\b|(?<=\W)(?=\W)", s) for s in subclauses)
  version_class = "-".join(str(v) for v in version)

  new_rule_descriptions = {}
  for paragraph in paragraphs:
    match = re.match(r"LB\s*(\d+[a-z]?)", "".join(paragraph))
    if match:
      if version in RENUMBERINGS:
        old_number = None
        for new, old in RENUMBERINGS[version]:
          if new == match.group(1) and (version, new) not in splits and (version, new) not in creations:
            old_number = old
      else:
        old_number = match.group(1)
      if old_number:
        new_rule_descriptions[old_number] = paragraph
  old_paragraphs = dict(history.elements)
  for paragraph_number in PRESERVED_PARAGRAPHS.get(version, []):
    print("Preserving", paragraph_number, "in", version)
    old_paragraph = old_paragraphs[paragraph_number].value()
    new_paragraph = max(paragraphs, key = lambda p: SequenceMatcher(None, "".join(p), old_paragraph).ratio())
    old_paragraphs[paragraph_number].add_version(version_class, new_paragraph)
  for paragraph_number, paragraph in history.elements:
    if paragraph.present():
      match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value())
      if match and match.group(1) in new_rule_descriptions:
        paragraph.add_version(version_class, new_rule_descriptions[match.group(1)])
  history.add_version(version_class, paragraphs)

TOL_LIGHT_COLOURS = [
    "#77AADD",
    "#99DDFF",
    "#44BB99",
    "#BBCC33",
    "#AAAA00",
    "#EEDD88",
    "#EE8866",
    "#FFAABB",
    "#DDDDDD",
]

with open("dumb_diff.html", "w", encoding="utf-8") as f:
  print("<html>", file=f)
  print("<head>", file=f)
  print('<meta charset="utf-8">', file=f)
  print("<title>Annotated Line Breaking Algorithm</title>", file=f)
  print("<style>", file=f)
  print("div.paranum { float:left; font-size: 64%; width: 2.8em; margin-left: -0.4em; margin-right: -3em; margin-top: 0.2em; }", file=f)
  print("p { margin-left: 3em }", file=f)
  print("a { color: inherit; }", file=f)
  print(".sources { text-decoration: none; }", file=f)
  for i, version in enumerate(VERSIONS):
    colour = TOL_LIGHT_COLOURS[i % len(TOL_LIGHT_COLOURS)]
    print(".changed-in-%s { background-color:%s; }" % (
              '-'.join(str(v) for v in version),
              colour),
          file=f)
    print("del.changed-in-%s { color:%s; text-decoration-thickness: .3ex; }" % (
              '-'.join(str(v) for v in version),
              colour),
          file=f)
    print("ins.changed-in-%s { background-color:%s; text-decoration: none; color: black; }" % (
              '-'.join(str(v) for v in version),
              colour),
          file=f)
  print("</style>", file=f)
  print("<script>", file=f)
  print("""
    function older_or_equal(v1, v2) {
      return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] <= v2[2])))
    }
    function older(v1, v2) {
      return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] < v2[2])))
    }
    function meow() {
      oldest = document.querySelector('input[name="oldest"]:checked').value.split("-").map(x => parseInt(x));
      newest = document.querySelector('input[name="newest"]:checked').value.split("-").map(x => parseInt(x));
      for (var label of document.getElementsByTagName("label")) {
        version = label.className.split("-").slice(-3).map(x => parseInt(x));
        if (older_or_equal(version, oldest)) {
          label.style = "color:black;background:white;";
        } else if (older(newest, version)) {
          label.style = "color:black;background:white;border:dashed";
        } else {
          label.style = "";
        }
      }
      for (var ins of document.getElementsByTagName("ins")) {
        version = ins.className.split("-").slice(-3).map(x => parseInt(x));
        if (older_or_equal(version, oldest)) {
          ins.style = "color:black;text-decoration:none;background-color:white;";
        } else if (older(newest, version)) {
          ins.style = "display:none";
        } else {
          ins.style = "";
        }
      }
      for (var del of document.getElementsByTagName("del")) {
        version = del.className.split("-").slice(-3).map(x => parseInt(x));
        if (older_or_equal(version, oldest)) {
          del.style = "display:none";
        } else if (older(newest, version)) {
          del.style = "text-decoration:none";
        } else {
          del.style = "";
        }
      }
    }
    window.onload = function () {
      for (var input of document.getElementsByTagName("input")) {
        input.onclick = meow;
      }
      meow();
    }
  """, file=f)
  print("</script>", file=f)
  print("</head>", file=f)
  print('<body style="margin-right:15em">', file=f)
  print('<table style="background:white;position:fixed;right:0;top:0">', file=f)
  print("<thead><tr><th>Base</th><th>Head</th></tr></thead>", file=f)
  print("<tbody>", file=f)
  for i, version in enumerate(VERSIONS):
    hyphenated = '-'.join(str(v) for v in version)
    print("<tr><td>", file=f)
    print(f'<input type="radio" id="oldest-{hyphenated}" name="oldest" value="{hyphenated}"{"checked" if version == (5,0,0) else ""}>', file=f)
    #print(f'<label for="oldest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
    print("</td><td>", file=f)
    print(f'<input type="radio" id="newest-{hyphenated}" name="newest" value="{hyphenated}"{"checked" if i == len(VERSIONS) - 1 else ""}>', file=f)
    print("</td><td>", file=f)
    print(f'<label for="newest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
    print("</td></tr>", file=f)
  print("</tbody>", file=f)
  print("</table>", file=f)
  for paragraph_number, paragraph in history.elements:
    print("<div class=paranum>", file=f)
    print(".".join(str(n) for n in paragraph_number), file=f)
    print("</div>", file=f)
    print("</p>", file=f)
    print("<p>", file=f)
    print(paragraph.html(), file=f)
    print("&nbsp;", file=f)
    print("</p>", file=f)
  print("</body>", file=f)
  print("</html>", file=f)
