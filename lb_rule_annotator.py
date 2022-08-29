import copy
import csv
from difflib import SequenceMatcher
import re
import sys
from typing import Dict, Sequence, Tuple

import historical_diff
from annotations import ISSUES, Issue

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
  CLAUSES = eval(f.read())

for version, rules in TABLE_5_BY_COLUMNS.items():
  expected_rules = tuple(rule for rule in rules if rule)
  actual_rules = tuple(key[2:] for  key in CLAUSES[version].keys() if key.startswith("LB"))
  if set(actual_rules) != set(expected_rules):
    print(pretty_version(version))
    for e in expected_rules:
      if e not in actual_rules:
        print(e, "in table but not in UAX")
    for e in actual_rules:
      if e not in expected_rules:
        print(e, "in UAX but not in table")
    print("Inconsistency between table 5 and Version", pretty_version(version))

SHOW_CHANGES = False
SHOW_EDITORIAL_CHANGES = False

def editorial_skeleton(s):
  s = s.casefold()
  s = re.sub(r"[,.: -]+", " ", s)
  s = re.sub(r"[“”]", '"', s)
  s = re.sub(r"[’]", "'", s)
  s = s.replace("don't", "do not")
  s = s.replace("character", "code point")
  s = s.replace("line break category", "line breaking class")
  return s.strip()

class RuleHistory:
  def __init__(self):
    self.issues : Dict[Tuple[int, int, int], Sequence[Issue]] = {}
    self.number = historical_diff.History()
    self.description = historical_diff.History(lambda x: x in ("ing", "of", "as", "and", "or") or re.match(r"[^\w()]+$", x))
    self.formulæ = []
    self.current_formulæ = 0

last_rules : Dict[str, RuleHistory] = {}

deleted_rules = []

trivial_versions = set()

for version, rules in CLAUSES.items():
  new_rules = {}
  rules_updated = set()
  text_changed_in_version = False
  for rule_number, (description, formulæ) in rules.items():
    rule_text_changed_in_version = False
    relevant_issue = False
    if not description:
      raise ValueError(rule_number)
    if version in RENUMBERINGS and rule_number.startswith("LB"):
      old_rule_number = dict(RENUMBERINGS[version]).get(rule_number[2:])
      if old_rule_number:
        old_rule_number = "LB"+old_rule_number
      history = copy.deepcopy(last_rules.get(old_rule_number, None))
      if old_rule_number:
        rules_updated.add(old_rule_number)
    else:
      history = copy.deepcopy(last_rules.get(rule_number, None))
      if history:
        rules_updated.add(rule_number)
    if not history:
      history = RuleHistory()
    for issue in ISSUES:
      if issue.version == version and (rule_number in issue.affected_rules or rule_number in issue.target_rules):
        history.issues.setdefault(version, []).append(issue)
        relevant_issue = True
    version_class = "-".join(str(v) for v in version)
    rule_text_changed_in_version |= history.number.add_version(version_class, re.split(r"(?<=\d)(?!\d)", rule_number))
    rule_text_changed_in_version |= history.description.add_version(version_class, re.split(r"(?:\b|(?=ing)|(?<=\W)(?=\W))", description))
    old_formulæ = [(i, f.current_text()) for i, f in enumerate(history.formulæ) if f.current_text()]
    operations = SequenceMatcher(None, [f for _, f in old_formulæ], formulæ).get_opcodes()
    offset = 0
    for operation, old_begin, old_end, new_begin, new_end in operations:
      if operation == "equal":
        continue
      elif operation == "delete":
        rule_text_changed_in_version = True
        for i, _ in old_formulæ[old_begin:old_end]:
          history.formulæ[i + offset].add_version(version_class, "")
      elif operation == "insert":
        for i in range(new_begin, new_end):
          f = historical_diff.History(lambda x: x.isspace() or x in "()")
          rule_text_changed_in_version |= f.add_version(version_class, re.split(r"(?:\b|(?<=\W)(?=\W))", formulæ[i]))
          if old_begin == len(old_formulæ):
            j = len(old_formulæ)
          else:
            j = old_formulæ[old_begin][0]
          history.formulæ.insert(j + offset, f)
          offset += 1
      elif operation == "replace":
        if old_end - old_begin == new_end - new_begin:
          for i, j in zip(range(old_begin, old_end), range(new_begin, new_end)):
            rule_text_changed_in_version |= history.formulæ[old_formulæ[i][0] + offset].add_version(version_class, re.split(r"(?:\b|(?<=\W)(?=\W))", formulæ[j]))
        else:
          for i, _ in old_formulæ[old_begin:old_end]:
            rule_text_changed_in_version |= history.formulæ[i + offset].add_version(version_class, "")
          for i in range(new_begin, new_end):
            f = historical_diff.History(lambda x: x.isspace() or x in "()")
            rule_text_changed_in_version |= f.add_version(version_class, re.split(r"(?:\b|(?<=\W)(?=\W))", formulæ[i]))
            if old_begin == len(old_formulæ):
              j = len(old_formulæ)
            else:
              j = old_formulæ[old_begin][0]
            history.formulæ.insert(j + offset, f)
            offset += 1
    if rule_text_changed_in_version and not relevant_issue:
      print("Unexplained change to", rule_number, "in", pretty_version(version))
    if relevant_issue and not rule_text_changed_in_version:
      print("Issue affects", rule_number, "in", pretty_version(version), " but it is unchanged")
    text_changed_in_version |= rule_text_changed_in_version

    new_rules[rule_number] = history
  for rule_number, history in last_rules.items():
    if rule_number not in rules_updated:
      history = copy.deepcopy(history)
      for issue in ISSUES:
        if issue.version == version and ("x" + rule_number in issue.affected_rules or "x" + rule_number in issue.target_rules):
          history.issues.setdefault(version, []).append(issue)
      text_changed_in_version |= history.number.add_version(version_class, "")
      text_changed_in_version |= history.description.add_version(version_class, "")
      for formula in history.formulæ:
        text_changed_in_version |= formula.add_version(version_class, "")
      deleted_rules.append((rule_number, history))
  if not text_changed_in_version:
    trivial_versions.add(version)
    print("No change in", pretty_version(version))
  last_rules = new_rules

rule_history = list(last_rules.items())

DELETED_RULE_LOCATIONS = {
    "LB30": "LB30a",
    "LB18b": "LB26",
    "LB7a": "LB9",
    "H4FinallyJoinAlphabeticLettersAndBreakEverythingElse": "LB28",
    "LB6": "H2Algorithm",
}

for rule_number, history in deleted_rules:
  rule_history.insert(
      next(i for i, (n, _) in enumerate(rule_history) if n == DELETED_RULE_LOCATIONS[rule_number]),
      (rule_number, history))

WONG_COLOURS = [
    #"white",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    #"#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7"]

TOL_LIGHT_COLOURS = [
    "#77AADD",
    "#99DDFF",
    #"#44BB99",
    "#BBCC33",
    "#AAAA00",
    "#EEDD88",
    "#EE8866",
    "#FFAABB",
    "#DDDDDD",
]


args = dict(arg[2:].split("=", 1) for arg in sys.argv[1:] if arg.startswith("--"))
if "out" in args:
  f = open(args["out"], "w", encoding="utf-8")
else:
  f = sys.stdout

nontrivial_versions = tuple(
    version for version in CLAUSES.keys() if not version in trivial_versions)

print("<html>", file=f)
print("<head>", file=f)
print('<meta charset="utf-8">', file=f)
print("<title>Annotated Line Breaking Algorithm</title>", file=f)
print("<style>", file=f)
print("a { color: inherit; }", file=f)
print(".sources { text-decoration: none; }", file=f)
for i, version in enumerate(nontrivial_versions):
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
print('<body>', file=f)
print(f"<h1><span class=changed-in-{'-'.join(str(v) for v in nontrivial_versions[-1])}>Annotated</span> Line Breaking Algorithm</h1>", file=f)
print('<table style="background:white;position:fixed;right:0;bottom:50%">', file=f)
print("<thead><tr><th>Base</th><th>New</th></tr></thead>", file=f)
print("<tbody>", file=f)
for i, version in enumerate(nontrivial_versions):
  hyphenated = '-'.join(str(v) for v in version)
  print("<tr><td>", file=f)
  print(f'<input type="radio" id="oldest-{hyphenated}" name="oldest" value="{hyphenated}"{"checked" if version == (5,0,0) else ""}>', file=f)
  #print(f'<label for="oldest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
  print("</td><td>", file=f)
  print(f'<input type="radio" id="newest-{hyphenated}" name="newest" value="{hyphenated}"{"checked" if i == len(nontrivial_versions) - 1 else ""}>', file=f)
  print(f'<label for="newest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
  print("</td></tr>", file=f)
print("</tbody>", file=f)
print("</table>", file=f)
for rule, history in rule_history:
  print("<p>", file=f)
  for version, issues in history.issues.items():
    hyphenated = '-'.join(str(v) for v in version)
    print(f'<ins class="changed-in-{hyphenated} sources">', file=f)
    for issue in issues:
      print("{", file=f)
      print(pretty_version(version) + ":", file=f)
      print(", ".join(f'<a href="https://www.unicode.org/cgi-bin/GetL2Ref.pl?{l2ref}">{l2ref}</a>' for l2ref in issue.l2_refs),
            file=f)
      if issue.l2_refs and issue.l2_docs:
        print("; ", file=f)
      print(", ".join(f'<a href="https://www.unicode.org/cgi-bin/GetMatchingDocs.pl?{l2doc}">{l2doc}</a>' for l2doc in issue.l2_docs),
            file=f)
      print("} ", file=f)
    print('</ins>', file=f)
  if history.issues:
    print("<br>", file=f)
  print(history.number.html(), file=f)
  print(history.description.html(), file=f)
  print("</p>", file=f)
  for formula in history.formulæ:
    print(f'<p style="text-align:center">', file=f)
    print(formula.html(), file=f)
    print("</p>", file=f)
print("</body>", file=f)
print("</html>", file=f)
