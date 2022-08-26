import difflib
import html
import re

class CharacterHistory:
  def __init__(self, version, c):
    self.value = c
    self.added = version
    self.removed = None

  def present(self):
    return self.added and not self.removed

  def absent(self):
    return not self.present()

class History:
  def __init__(self, junk=lambda x: x.isspace()):
    self.characters : list[CharacterHistory] = []
    self.junk = junk

  def current_text(self):
    return "".join(c.value for c in self.characters if c.present())

  def add_version(self, version, new_text):
    indexing = []
    i = 0
    for c in self.characters:
      if c.present():
        indexing.append((i, c))
        i += 1
      else:
        indexing.append((None, c))

    diff = difflib.SequenceMatcher(
      self.junk,
      [c.value for c in self.characters if c.present()],
      new_text).get_opcodes()
    text_changed = False
    for operation in diff:
      if operation[0] == "equal":
        continue
      elif operation[0] == "replace":
        elementary_operations = (
            ("delete", *operation[1:]),
            ("insert", *operation[1:]))
      else:
        elementary_operations = [operation]
      for operation in elementary_operations:
        if operation[0] == "delete":
          text_changed = True
          for old_index, c in indexing:
            if old_index is None:
              continue
            elif old_index >= operation[2]:
              break
            elif old_index >= operation[1]:
              c.removed = version
        elif operation[0] == "insert":
          text_changed = True
          inserted = [(None, CharacterHistory(version, c))
                      for c in new_text[operation[3]:operation[4]]]
          if operation[3] == 0:
            indexing = inserted + indexing
          else:
            for i, (old_index, c) in enumerate(indexing):
              if old_index is None:
                continue
              elif old_index + 1 == operation[1]:
                before = indexing[:i+1]
                after = indexing[i+1:]
                indexing = before + inserted + after
                break
            else:
              raise Exception("Failed to insert")
    self.characters = [c for _, c in indexing]
    return text_changed

  def html(self):
    added = None
    removed = None
    versions = set()
    text = ""
    for c in self.characters:
      if not c.value:
        continue
      versions.add(c.added)
      if c.removed:
        versions.add(c.removed)
      if c.removed != removed:
        if added:
          text += "</ins>"
          added = None
        if removed:
          text += "</del>"
        removed = c.removed
        if removed:
          text += f'<del class="changed-in-{removed}">'
      if c.added != added:
        if added:
          text += "</ins>"
        added = c.added
        if added:
          text += f'<ins class="changed-in-{added}">'
      text += html.escape(c.value)
    if added:
      text += "</ins>"
    if removed:
      text += "</del>"
      removed = None
    return text

if False:
  import re

  h = History()
  h.add_version(1, "kitties are good")
  h.add_version(2, "cats are good")
  h.add_version(3, "Cats are good.")
  h.add_version(4, "Cats are good because they are soft.")
  print("".join(c.value for c in h.characters))
  print("".join(str(c.added) for c in h.characters))
  print("".join(str(c.removed or " ") for c in h.characters))
  print(h.html())

  h = History()
  h.add_version(1, re.split(r"\b", "kitties are good"))
  h.add_version(2, re.split(r"\b", "cats are good"))
  h.add_version(3, re.split(r"\b", "Cats are good."))
  h.add_version(4, re.split(r"\b", "Cats are good because they are soft."))
  print("".join(c.value for c in h.characters))
  print("".join(str(c.added) * len(c.value) for c in h.characters))
  print("".join(str(c.removed or " ") * len(c.value) for c in h.characters))
  print(h.html())
