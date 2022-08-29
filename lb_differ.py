import historical_diff
import re

def pretty_version(version):
  return ".".join(str(v) for v in version)

with open("rules.py", encoding="utf-8") as f:
  VERSIONS = eval(f.read())

def make_sequence_history(v, s):
  h = historical_diff.SequenceHistory()
  h.add_version(v, s)
  return h

history = historical_diff.SequenceHistory(element_history=make_sequence_history)

for version_number, clauses in VERSIONS.items():
  paragraphs = []
  for title, subclauses in clauses.values():
    paragraphs.append(re.split(r"\b|(?<=\W)(?=\W)", title))
    paragraphs.extend(re.split(r"\b|(?<=\W)(?=\W)", s) for s in subclauses)
  version_class = "-".join(str(v) for v in version_number)

  new_rule_descriptions = {}
  for paragraph in paragraphs:
    match = re.match(r"(LB ?\d+[a-z]?)", "".join(paragraph))
    if match:
      new_rule_descriptions[match.group(1)] = paragraph
  for paragraph in history.elements:
    if paragraph.present():
      match = re.match(r"(LB ?\d+[a-z]?)", paragraph.value())
      if match and match.group(1) in new_rule_descriptions:
        paragraph.add_version(version_class, new_rule_descriptions[match.group(1)])
  history.add_version(version_class, paragraphs)

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

with open("dumb_diff.html", "w", encoding="utf-8") as f:
  print("<html>", file=f)
  print("<head>", file=f)
  print('<meta charset="utf-8">', file=f)
  print("<title>Annotated Line Breaking Algorithm</title>", file=f)
  print("<style>", file=f)
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
  print("<thead><tr><th>Base</th><th>New</th></tr></thead>", file=f)
  print("<tbody>", file=f)
  for i, version in enumerate(VERSIONS):
    hyphenated = '-'.join(str(v) for v in version)
    print("<tr><td>", file=f)
    print(f'<input type="radio" id="oldest-{hyphenated}" name="oldest" value="{hyphenated}"{"checked" if version == (5,0,0) else ""}>', file=f)
    #print(f'<label for="oldest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
    print("</td><td>", file=f)
    print(f'<input type="radio" id="newest-{hyphenated}" name="newest" value="{hyphenated}"{"checked" if i == len(VERSIONS) - 1 else ""}>', file=f)
    print(f'<label for="newest-{hyphenated}" class="changed-in-{hyphenated}">Unicode Version {pretty_version(version)}</label>', file=f)
    print("</td></tr>", file=f)
  print("</tbody>", file=f)
  print("</table>", file=f)
  for paragraph in history.elements:
    print("<p>", file=f)
    print(paragraph.html(), file=f)
    print("</p>", file=f)
  print("</body>", file=f)
  print("</html>", file=f)
