import csv
from difflib import SequenceMatcher
from typing import Sequence, Tuple
import re

from annotations import ISSUES
from document import Paragraph, Heading, Rule, Formula, Table
from historical_diff import Version
import historical_diff

def parse_version(s):
  match = re.match(r"(?:Unicode )?(\d+)\.(\d)\.(\d)", s)
  if match:
    return Version(*(int(v) for v in match.groups()))

with open('renumberings.tsv') as f:
  rows = csv.reader(f, delimiter="\t")
  columns = [tuple(re.sub(r"LB|deprecated|removed", "", entry).strip() or None for entry in column) for column in zip(*rows)]
  TABLE_5_BY_COLUMNS = {parse_version(column[0]) : tuple(column[1:]) for column in columns}
  RENUMBERINGS = {parse_version(left[0]) : tuple(zip(left[1:], right[1:])) for left, right in zip(columns[:-1], columns[1:])}

splits = set()
creations = set()
deletions = set()

REORDERINGS = {
  Version(4, 0, 0): [("13", "11b"), ("15b", "18b")],
  Version(5, 0, 0): [("11b", "11"), ("13", "12")]
}

for version, renumbering in reversed(list(RENUMBERINGS.items())):
  mapping = dict(renumbering)
  reverse = {}
  for new, old in renumbering:
    if old:
      if new:
        reverse.setdefault(old, set()).add(new)
      else:
        deletions.add((version, old))
        print (f"RULE DELETION: {old} in {version}")
    elif new:
      creations.add((version, new))
      print (f"RULE CREATION: {new} in {version}")

  for old, new in reverse.items():
    if len(new) > 1:
      for n in new:
        splits.add((version, n))
      print (f"RULE SPLIT: {old} into ({', '.join(sorted(new))}) in {version}")

  common = [(old, tuple(new)[0]) for old, new, in reverse.items() if len(new) == 1]
  old_order = sorted(common, key=lambda x: re.sub(r"^(\d)(?!\d)", r"0\1", x[0]))
  new_order = sorted(common, key=lambda x: re.sub(r"^(\d)(?!\d)", r"0\1", x[1]))
  if new_order != old_order:
    print("REORDERING in", version)
    for i in range(len(old_order)):
      if new_order[i] != old_order[i]:
        break
    for j in range(len(old_order)):
      if new_order[-j] != old_order[-j]:
        break
    print("...", " ".join(old + "↦" + new for old, new in old_order[i:-j+1]), "...")
    print("...", " ".join(old + "↦" + new for old, new in new_order[i:-j+1]), "...")
    if version in REORDERINGS:
      for old, new in REORDERINGS[version]:
        old_order.remove((old, new))
        new_order.remove((old, new))
      if old_order != new_order:
        print("INCORRECTLY DESCRIBED")
    else:
      print("UNEXPECTED")

METAMORPHOSES = {
  "4-1-0": [(Paragraph, (84,), Formula)],
}

with open("paragraphs.py", encoding="utf-8") as f:
  VERSIONS : dict[Version, Sequence[Paragraph]] = eval(f.read())

def get_words(p: Paragraph, h: historical_diff.SequenceHistory, version, *context):
  if not p:
    return p
  if type(h.tag) != type(p):
    if version not in METAMORPHOSES or (type(h.tag), *context, type(p)) not in METAMORPHOSES[version]:
      print("ERROR:", type(h.tag).__name__, *context, "becomes", type(p).__name__, "in", version)
      print("ERROR:", h.value())
      print("ERROR:", p.contents)
    h.tag = p
  return p.words()

def make_sequence_history(v, p: Paragraph):
  h = historical_diff.SequenceHistory(
        junk=lambda w: w.isspace() or w in ".,;:" or w in ("of", "and", "between", "the", "is", "that", "ing"),
        check_and_get_elements=get_words)
  h.tag = p
  h.issues = []
  h.add_version(v, p)
  return h

history = historical_diff.SequenceHistory(element_history=make_sequence_history, number_nicely=True)

PRESERVED_PARAGRAPHS = {
  Version(3, 1, 0): {(10,): "", (84,): ""},
  Version(4, 0, 0): {(3,): "", (27,): ""},
  Version(4, 1, 0): {(33, 3): "LB 6", (39,): "LB 7a", (84,): ""},
  Version(5, 0, 0): {(3,): "", (6,): "", (9, 1): "", (10,): "", (11,): "", (33, 2, 1): "", (39, 1): "", (40, 7): ""},
  Version(5, 1, 0): {(40, 13): "", (40, 18): "The following", (101, 3): "LB30"},
  Version(5, 2, 0): {(101, 3): "LB30"},
  Version(6, 0, 0): {(33,): ""},
  Version(6, 1, 0): {(13, 2): ""},
  Version(9, 0, 0): {(82, 4): "(PR | PO)", (101, 11) : "sot (RI RI)*"},
  Version(11, 0, 0): {(33, 1, 4): "A ZWJ"},
  Version(13, 0, 0): {(73,): "× IN"},
}

nontrivial_versions = []

previous_version = None
for version, paragraphs in VERSIONS.items():
  print(version)

  new_rule_descriptions = {}
  for paragraph in paragraphs:
    match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.contents)
    if match:
      if version in RENUMBERINGS:
        old_number = None
        for new, old in RENUMBERINGS[version]:
          if new == match.group(1) and (
              (version, new) not in splits and
              (version, new) not in creations and
              (old, new) not in REORDERINGS.get(version, [])):
            old_number = old
      else:
        old_number = match.group(1)
      if old_number:
        new_rule_descriptions[old_number] = paragraph
  old_paragraphs = dict(history.elements)
  for paragraph_number, hint in PRESERVED_PARAGRAPHS.get(version, {}).items():
    print("Preserving", paragraph_number, "in", version)
    old_paragraph = old_paragraphs[paragraph_number].value()
    hinted_paragraphs = (p for p in paragraphs if p.contents.startswith(hint)) if hint else paragraphs
    new_paragraph = max(hinted_paragraphs, key = lambda p: SequenceMatcher(None, p.contents, old_paragraph).ratio())
    if not hinted_paragraphs:
      print("ERROR: no paragraph matching hint", hint)
    old_paragraphs[paragraph_number].add_version(version, new_paragraph, paragraph_number)
  for paragraph_number, paragraph in history.elements:
    if paragraph.present():
      match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value())
      if match and match.group(1) in new_rule_descriptions:
        paragraph.add_version(version, new_rule_descriptions[match.group(1)], paragraph_number)
  history.add_version(version, paragraphs)

  any_change = False
  rule_number = None
  current_issues = []
  for paragraph_number, paragraph in history.elements:
    match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value())
    if match:
      rule_number = "LB" + match.group(1)
      previous_rule_number = None
      if previous_version:
        match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value_at(previous_version))
        if match:
          previous_rule_number = "LB" + match.group(1)
      current_issues = [issue for issue in ISSUES
                        if issue.version == version and
                           (rule_number in issue.target_rules or
                            rule_number in issue.affected_rules)]
      current_issues += [issue for issue in ISSUES
                         if issue.version == version and
                            previous_rule_number in issue.deleted_rules]

    if paragraph.last_changed() == version:
      any_change = True
      paragraph.issues += current_issues
  if any_change:
    nontrivial_versions.append(version)

  previous_version = version


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

with open("alba.html", "w", encoding="utf-8") as f:
  print("<!DOCTYPE html>", file=f)
  print("<html>", file=f)
  print("<head>", file=f)
  print('<meta charset="utf-8">', file=f)
  print("<title>Annotated Line Breaking Algorithm</title>", file=f)
  print("<style>", file=f)
  print("div.paranum { float:left; font-size: 64%; width: 2.8em; margin-left: -0.4em; margin-right: -3em; margin-top: 0.2em; }", file=f)
  print("div.sources { float:right; font-size: 80%; max-width:50%; text-align:right; }", file=f)
  print("p { margin-left: 3em; }", file=f)
  #print("p.sources { margin-block-end: 0 }", file=f)
  print("h1 { margin-left: 3em }", file=f)
  print("h2 { margin-left: 3em }", file=f)
  print("h3 { margin-left: 3em }", file=f)
  print("h4 { margin-left: 3em }", file=f)
  print("table { margin-left: 3em }", file=f)
  print(".rule { font-style: italic }", file=f)
  print(".formula { margin-left: 5em }", file=f)
  print("a { color: inherit; }", file=f)
  print("ins.sources { text-decoration: none; white-space:nowrap; }", file=f)
  for i, version in enumerate(nontrivial_versions):
    colour = TOL_LIGHT_COLOURS[i % len(TOL_LIGHT_COLOURS)]
    print(".changed-in-%s { background-color:%s; }" % (
              version.html_class(),
              colour),
          file=f)
    print("del.changed-in-%s { color:%s; text-decoration-thickness: .3ex; }" % (
              version.html_class(),
              colour),
          file=f)
    print("ins.changed-in-%s { background-color:%s; text-decoration: none; color: black; }" % (
              version.html_class(),
              colour),
          file=f)
    print("table.changed-in-%s { background:%s; color: black; }" % (
              version.html_class(),
              colour),
          file=f)
  print("</style>", file=f)
  print("<script>", file=f)
  print("""
    function older_or_equal(v1, v2) {
      return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] <= v2[2])));
    }
    function older(v1, v2) {
      return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] < v2[2])));
    }
    function show_version_diff(version) {
      chosen_oldest = null;
      for (var input of document.querySelectorAll('input[name="oldest"]')) {
        if (input.name != "oldest") {
          continue;
        }
        input_version = input.value.split("-").map(x => parseInt(x));
        chosen_oldest_version = chosen_oldest?.value.split("-").map(x => parseInt(x));
        if (older(input_version, version.split("-").map(x => parseInt(x))) && 
            (chosen_oldest_version == null || older(chosen_oldest_version, input_version))) {
          chosen_oldest = input;
        }
      }
      if (!chosen_oldest) {
        chosen_oldest = document.querySelector('input[name="oldest"][value="' + version + '"]')
      }
      chosen_oldest.checked = true;
      document.querySelector('input[name="newest"][value="' + version + '"]').checked = true;
      meow();
    }
    function meow() {
      oldest = document.querySelector('input[name="oldest"]:checked').value.split("-").map(x => parseInt(x));
      newest = document.querySelector('input[name="newest"]:checked').value.split("-").map(x => parseInt(x));
      for (var label of document.getElementsByTagName("button")) {
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
      for (var table of document.querySelectorAll("table[class^=changed-in-]")) {
        version = table.className.split("-").slice(-3).map(x => parseInt(x));
        if (older_or_equal(version, oldest)) {
          table.style = "color:black;text-decoration:none;background-color:white;";
        } else if (older(newest, version)) {
          table.style = "display:none";
        } else {
          table.style = "";
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
      for (var button of document.getElementsByTagName("button")) {
        const version = button.value;
        button.onclick = function() { show_version_diff(version); };
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
  for i, version in enumerate(nontrivial_versions):
    print("<tr><td>", file=f)
    print(f'<input type="radio" id="oldest-{version.html_class()}" name="oldest" value="{version.html_class()}"{"checked" if version == Version(5,0,0) else ""}>', file=f)
    #print(f'<label for="oldest-{version.html_class()}" class="changed-in-{version.html_class()}">Unicode Version {version}</label>', file=f)
    print("</td><td>", file=f)
    print(f'<input type="radio" id="newest-{version.html_class()}" name="newest" value="{version.html_class()}"{"checked" if i == len(nontrivial_versions) - 1 else ""}>', file=f)
    print("</td><td>", file=f)
    print(f'<button class="changed-in-{version.html_class()}" value="{version.html_class()}">Unicode Version {version}</button>', file=f)
    print("</td></tr>", file=f)
  print("</tbody>", file=f)
  print("</table>", file=f)
  for paragraph_number, paragraph in history.elements:
    paragraph: historical_diff.SequenceHistory
    print("<div class=paranum>", file=f)
    print(".".join(str(n) for n in paragraph_number), file=f)
    print("</div>", file=f)

    if paragraph.issues:
      print("<div class=sources>", file=f)
    for issue in paragraph.issues:
      print(f'<ins class="changed-in-{issue.version.html_class()} sources">', file=f)
      print("{" + str(issue.version) + ": " +
            ", ".join(f'<a href="https://www.unicode.org/cgi-bin/GetL2Ref.pl?{l2ref}">{l2ref}</a>'
                      for l2ref in issue.l2_refs) +
            ("" if not issue.l2_refs or not issue.l2_docs else
             "; " + ",".join(f'<a href="https://www.unicode.org/cgi-bin/GetMatchingDocs.pl?{l2doc}">{l2doc}</a>'
                             for l2doc in issue.l2_docs)) +
            "}",
            file=f)
      print('</ins>', file=f)
    if paragraph.issues:
      print("</div>", file=f)

    if type(paragraph.tag) == Table:
      for _, t in paragraph.elements:
        t: historical_diff.AtomHistory
        if t.removed:
          print(f"<del class=changed-in-{t.removed}>", file=f)
        table_contents = t.value().replace("\u2028", "<br>")
        print(f"<table class=changed-in-{t.added}>{table_contents}</table>", file=f)
        if t.removed:
          print(f"</del>", file=f)
      print(f"<p>&nbsp;</p>", file=f)
    else:
      print(paragraph.tag.html(paragraph.html() + "&nbsp;"), file=f)
  print("</body>", file=f)
  print("</html>", file=f)
