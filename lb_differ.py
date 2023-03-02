import csv
from difflib import SequenceMatcher
from typing import Sequence, Tuple
import re

from annotations import ISSUES
from document import Paragraph, Heading, Rule, Formula, TableRow
from historical_diff import Version, ParagraphNumber, SequenceHistory, AtomHistory
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
  Version(4, 1, 0): [(Paragraph, ParagraphNumber(84), Formula)],
}

with open("paragraphs.py", encoding="utf-8") as f:
  VERSIONS : dict[Version, Sequence[Paragraph]] = eval(f.read())

def get_ancestor(version: Version, p: ParagraphNumber):
  if version in ANCESTRIES and p in ANCESTRIES[version]:
    ancestor = ANCESTRIES[version][p]
    ancestor_history = dict(history.elements)[ancestor]
    return (version, ancestor, ancestor_history)
  else:
    return None

def is_default_junk(w):
  return w.isspace() or w in ".,;:" or w in ("of", "and", "between", "the", "is", "that", "ing")

def get_junk_override(version: Version, p: ParagraphNumber):
  if version in JUNK and p in JUNK[version]:
    junk = JUNK[version][p]
    return lambda w: is_default_junk(w) or w in junk
  else:
    return None

def get_words(p: Paragraph, h: SequenceHistory, version, *context):
  if not p:
    return p
  if type(h.tag) != type(p):
    if version not in METAMORPHOSES or (type(h.tag), *context, type(p)) not in METAMORPHOSES[version]:
      print("ERROR:", type(h.tag).__name__, *context, "becomes", type(p).__name__, "in", version)
      print("ERROR:", h.value())
      print("ERROR:", p.contents)
    h.tag = p
  return p.words()

def make_sequence_history(v, p: Paragraph, *context):
  h = SequenceHistory(
        junk=is_default_junk,
        check_and_get_elements=get_words,
        get_ancestor=get_ancestor,
        get_junk_override=get_junk_override)
  h.tag = p
  h.add_version(v, p, *context)
  return h

history = SequenceHistory(element_history=make_sequence_history, number_nicely=True)

DELETED_PARAGRAPHS = {
  Version(3, 1, 0): [ParagraphNumber(65), ParagraphNumber(67)],
  Version(4, 0, 0): [ParagraphNumber(22)],
  Version(4, 1, 0): [ParagraphNumber(53, 5), ParagraphNumber(53, 6)],
}

PRESERVED_PARAGRAPHS = {
  Version(3, 1, 0): {ParagraphNumber(10): "",
                     ParagraphNumber(38): "",
                     #ParagraphNumber(67): "× NS",
                     ParagraphNumber(84): ""},
  Version(4, 0, 0): {ParagraphNumber(3): "",
                     ParagraphNumber(27): ""},
  Version(4, 1, 0): {ParagraphNumber(33, 3): "LB 6",
                     ParagraphNumber(39): "LB 7a",
                     ParagraphNumber(40, 3): "",
                     ParagraphNumber(40, 4): "",
                     ParagraphNumber(53, 4): "",
                     ParagraphNumber(84): ""},
  Version(5, 0, 0): {ParagraphNumber(3): "",
                     ParagraphNumber(6): "",
                     ParagraphNumber(9, 1): "",
                     ParagraphNumber(10,): "",
                     ParagraphNumber(11): "",
                     ParagraphNumber(33, 2, 1): "",
                     ParagraphNumber(39, 1): "",
                     ParagraphNumber(40, 7): ""},
  Version(5, 1, 0): {ParagraphNumber(40, 13): "",
                     ParagraphNumber(40, 18): "The following",
                     ParagraphNumber(101, 3): "LB30"},
  Version(5, 2, 0): {ParagraphNumber(101, 3): "LB30"},
  Version(6, 0, 0): {ParagraphNumber(33): ""},
  Version(6, 1, 0): {ParagraphNumber(13, 2): ""},
  Version(9, 0, 0): {ParagraphNumber(82, 4): "(PR | PO)",
                     ParagraphNumber(101, 11) : "sot (RI RI)*"},
  Version(11, 0, 0): {ParagraphNumber(33, 1, 4): "A ZWJ"},
  Version(13, 0, 0): {ParagraphNumber(73): "× IN"},
}

ANCESTRIES = {
  Version(3, 1, 0): {ParagraphNumber(9, 1): ParagraphNumber(11),
                     ParagraphNumber(21, 3): ParagraphNumber(23),
                     ParagraphNumber(21, 2): ParagraphNumber(24),
                     ParagraphNumber(21, 1): ParagraphNumber(25),
                     ParagraphNumber(45, 1): ParagraphNumber(47),
                     ParagraphNumber(67, 1): ParagraphNumber(65),
                     ParagraphNumber(65, 1): ParagraphNumber(67),
                     ParagraphNumber(72, 1): ParagraphNumber(75),
                     ParagraphNumber(72, 2): ParagraphNumber(76),
                     ParagraphNumber(80, 1): ParagraphNumber(83),
                     ParagraphNumber(87, 1): ParagraphNumber(97),
                     ParagraphNumber(87, 2): ParagraphNumber(92),
                     ParagraphNumber(87, 3): ParagraphNumber(95),
                     ParagraphNumber(87, 4): ParagraphNumber(94),
                     ParagraphNumber(87, 5): ParagraphNumber(96),
                     ParagraphNumber(87, 6): ParagraphNumber(89),
                     ParagraphNumber(87, 7): ParagraphNumber(91),},
  Version(4, 0, 0): {ParagraphNumber(21, 1, 2): ParagraphNumber(22),
                     ParagraphNumber(40, 1): ParagraphNumber(38, 1),
                     ParagraphNumber(40, 3): ParagraphNumber(37),
                     ParagraphNumber(40, 4): ParagraphNumber(35),
                     ParagraphNumber(53, 4): ParagraphNumber(58),
                     ParagraphNumber(53, 5): ParagraphNumber(59),
                     ParagraphNumber(53, 6): ParagraphNumber(60),
                     ParagraphNumber(98, 1): ParagraphNumber(69),
                     ParagraphNumber(98, 2): ParagraphNumber(70),
                     ParagraphNumber(98, 3): ParagraphNumber(71),},
  Version(4, 1, 0): {ParagraphNumber(56, 3): ParagraphNumber(53, 4),
                     ParagraphNumber(56, 4): ParagraphNumber(53, 5),
                     ParagraphNumber(56, 5): ParagraphNumber(53, 6),
                     ParagraphNumber(98, 5): ParagraphNumber(33, 2),
                     ParagraphNumber(98, 10): ParagraphNumber(33, 2),
                     ParagraphNumber(98, 6): ParagraphNumber(33, 3),
                     ParagraphNumber(98, 11): ParagraphNumber(33, 3),
                     ParagraphNumber(98, 15): ParagraphNumber(33, 2),},
  Version(5, 0, 0): {ParagraphNumber(20, 1): ParagraphNumber(27, 1),
                     ParagraphNumber(40, 8): ParagraphNumber(53, 3),
                     ParagraphNumber(40, 9): ParagraphNumber(53, 4),
                     ParagraphNumber(40, 10): ParagraphNumber(53, 7),
                     ParagraphNumber(40, 11): ParagraphNumber(53, 8),
                     ParagraphNumber(40, 12): ParagraphNumber(56, 2),
                     ParagraphNumber(40, 13): ParagraphNumber(56, 3),
                     ParagraphNumber(40, 14): ParagraphNumber(56, 4),
                     ParagraphNumber(40, 15): ParagraphNumber(56, 5),
                     ParagraphNumber(82, 3): ParagraphNumber(87, 6),
                     ParagraphNumber(87, 1, 2): ParagraphNumber(87, 5),
                     ParagraphNumber(87, 1, 6): ParagraphNumber(90),
                     ParagraphNumber(87, 1, 7): ParagraphNumber(88),},
  Version(5, 1, 0): {ParagraphNumber(40, 20): ParagraphNumber(40, 13),
                     ParagraphNumber(40, 21): ParagraphNumber(40, 14),
                     ParagraphNumber(40, 22): ParagraphNumber(40, 16),},
  Version(9, 0, 0): {ParagraphNumber(82, 0, 1): ParagraphNumber(82, 1),
                     ParagraphNumber(82, 0, 2): ParagraphNumber(82, 2),
                     ParagraphNumber(82, 0, 3): ParagraphNumber(80, 1),},
}

JUNK = {
  Version(9, 0, 0): {ParagraphNumber(101,10): ["break"],},
  Version(13, 0, 0): {ParagraphNumber(73): ["IN"],},
  Version(3, 1, 0): {ParagraphNumber(11): ["The", "each", "rule"],
                     ParagraphNumber(35): ["CM"]},
  Version(4, 1, 0): {ParagraphNumber(98, 5): ["Syllable", "Blocks", "for"],
                     ParagraphNumber(98, 10): ["Hangul", "syllable", "block"],
                     ParagraphNumber(98, 15): ["Korean", "are", "for", "line", "break", "class", "ID"]},
  Version(5, 1, 0): {ParagraphNumber(40, 20): ["after"]},
}

nontrivial_versions = []

additional_paragraphs = {}

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
  for paragraph_number in DELETED_PARAGRAPHS.get(version, []):
    print("Deleting", paragraph_number, "in", version)
    old_paragraphs[paragraph_number].remove(version, paragraph_number)
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
  rule_issues = []
  for paragraph_number, paragraph in history.elements:
    paragraph_issues = [issue for issue in ISSUES
                        if issue.version == version and paragraph_number in issue.paragraphs]
    match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value())
    rule_number = None
    previous_rule_number = None
    if match:
      rule_number = "LB" + match.group(1)
    if previous_version:
      match = re.match(r"LB\s*(\d+[a-z]?)", paragraph.value_at(previous_version))
      if match:
        previous_rule_number = "LB" + match.group(1)
    if rule_number or previous_rule_number:
      rule_issues = [issue for issue in ISSUES
                        if issue.version == version and
                           (rule_number in issue.target_rules or
                            rule_number in issue.affected_rules)]
      rule_issues += [issue for issue in ISSUES
                         if issue.version == version and
                            previous_rule_number in issue.deleted_rules]

    if paragraph.last_changed() == version:
      any_change = True
      for issue in rule_issues:
        additional_paragraphs.setdefault(issue, []).append(paragraph_number)
      paragraph.references += paragraph_issues + rule_issues
  if any_change:
      nontrivial_versions.append(version)
  previous_version = version

for issue, paragraphs in additional_paragraphs.items():
  print(issue)
  print(str(paragraphs).replace("), ", "),\n "))

for issue in ISSUES:
  for annotation in issue.annotations:
    print("adding annotation %s" % annotation.number)
    for i, (paragraph_number, paragraph) in enumerate(history.elements):
      if annotation.number < paragraph_number:
        break
    annotation_history = make_sequence_history(issue.version, annotation, annotation.number)
    history.elements.insert(i,
                            (annotation.number,
                             annotation_history))
    annotation_history.references = [issue]


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
  with open("alba.css") as css:
    print(css.read(), file=f)
  print("</style>", file=f)
  print("<script>", file=f)
  with open("alba.js") as js:
    print(js.read(), file=f)
  print("</script>", file=f)
  print("</head>", file=f)
  print('<body lang="en-US">', file=f)
  print('<nav>', file=f)
  print('<table>', file=f)
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
  print('<div><input type="checkbox" name="show-deleted" id="show-deleted" checked>', file=f)
  print('<label for="show-deleted">Show deleted paragraphs</label></div>', file=f)
  print('</nav>', file=f)
  for paragraph_number, paragraph in history.elements:
    paragraph: SequenceHistory
    revision_number = ""
    versions_changed = paragraph.versions_changed()
    version_added = paragraph.version_added()
    last_changed = paragraph.last_changed()
    print(f'<div class="paragraph added-in-{version_added.html_class()}{(" removed-in-" + last_changed.html_class()) if paragraph.absent() else ""}">', file=f)
    for new, old in zip(versions_changed[1:], versions_changed[:-1]):
      if old == Version(3, 0, 0):
        continue
      revision_number += f'<del class="paranum changed-in-{new.html_class()}"><ins class="paranum changed-in-{old.html_class()}">/{old.short()}</ins></del>'
    if versions_changed[-1] != Version(3, 0, 0):
      revision_number += f'<ins class="paranum changed-in-{last_changed.html_class()}">/{last_changed.short()}</ins>'
    print(f"<div class=paranum><a id=p{paragraph_number} href=#p{paragraph_number}>{paragraph_number}{revision_number}</a></div>", file=f)

    if paragraph.references:
      print("<div class=sources>", file=f)
    for issue in paragraph.references:
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
    if paragraph.references:
      print("</div>", file=f)

    print(paragraph.tag.html(paragraph.html(), paragraph.version_added()), file=f)
    print("</div>", file=f)
  print("</body>", file=f)
  print("</html>", file=f)
