import difflib
import html
import re

class History:
  def remove(self, version):
    pass

  def value(self):
    return ""

  def present(self):
    return False

  def absent(self):
    return not self.present()

class AtomHistory(History):
  def __init__(self, version, c):
    self.text = c
    self.added = version
    self.removed = None

  def value(self):
    return self.text

  def remove(self, version):
    self.removed = version

  def present(self):
    return self.added and not self.removed

  def absent(self):
    return not self.present()

class SequenceHistory(History):
  def __init__(self, junk=lambda x: x.isspace(), element_history=AtomHistory):
    self.element_history = element_history
    self.elements : list[History] = []
    self.junk = junk

  def current_text(self):
    return "".join(c.value() for c in self.elements if c.present())

  def present(self):
    return any(c.present() for c in self.elements)

  def absent(self):
    return not self.present()

  def remove(self, version):
    self.add_version(version, [])

  def value(self):
    return "".join(c.value() for c in self.elements if c.present())

  def add_version(self, version, new_text):
    indexing = []
    i = 0
    for c in self.elements:
      if c.present():
        indexing.append((i, c))
        i += 1
      else:
        indexing.append((None, c))

    diff = difflib.SequenceMatcher(
      self.junk,
      [c.value() for c in self.elements if c.present()],
      [self.element_history(version, element).value() for element in new_text]).get_opcodes()
    text_changed = False
    for instruction in diff:
      (operation, old_begin, old_end, new_begin, new_end) = instruction
      if operation == "equal":
        continue
      elif operation == "replace":
        if (isinstance(self.elements[0], SequenceHistory) and
            old_end - old_begin == new_end - new_begin):
          elementary_instructions = [instruction]
        else:
          elementary_instructions = (
              ("delete", *instruction[1:]),
              ("insert", *instruction[1:]))
      else:
        elementary_instructions = [instruction]
      for operation, old_begin, old_end, new_begin, new_end in elementary_instructions:
        if operation == "delete":
          text_changed = True
          for old_index, c in indexing:
            if old_index is None:
              continue
            elif old_index >= old_end:
              break
            elif old_index >= old_begin:
              c.remove(version)
        elif operation == "insert":
          text_changed = True
          inserted = [(None, self.element_history(version, c))
                      for c in new_text[new_begin:new_end]]
          if new_begin == 0:
            indexing = inserted + indexing
          else:
            for i, (old_index, c) in enumerate(indexing):
              if old_index is None:
                continue
              elif old_index + 1 == old_begin:
                before = indexing[:i+1]
                after = indexing[i+1:]
                indexing = before + inserted + after
                break
            else:
              raise Exception("Failed to insert")
        elif operation == "replace":
          i = new_begin
          for old_index, c in indexing:
            if old_index is None:
              continue
            elif old_index >= old_end:
              break
            elif old_index >= old_begin:
              c.add_version(version, new_text[i])
              i += 1
          
    self.elements = [c for _, c in indexing]
    return text_changed

  def html(self):
    added = None
    removed = None
    versions = set()
    text = ""
    for c in self.elements:
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
      text += html.escape(c.value())
    if added:
      text += "</ins>"
    if removed:
      text += "</del>"
      removed = None
    return text

if False:
  import re

  h = SequenceHistory()
  h.add_version(1, "kitties are good")
  h.add_version(2, "cats are good")
  h.add_version(3, "Cats are good.")
  h.add_version(4, "Cats are good because they are soft.")
  print("".join(c.value for c in h.elements))
  print("".join(str(c.added) for c in h.elements))
  print("".join(str(c.removed or " ") for c in h.elements))
  print(h.html())

  h = SequenceHistory()
  h.add_version(1, re.split(r"\b", "kitties are good"))
  h.add_version(2, re.split(r"\b", "cats are good"))
  h.add_version(3, re.split(r"\b", "Cats are good."))
  h.add_version(4, re.split(r"\b", "Cats are good because they are soft."))
  print("".join(c.value for c in h.elements))
  print("".join(str(c.added) * len(c.value) for c in h.elements))
  print("".join(str(c.removed or " ") * len(c.value) for c in h.elements))
  print(h.html())
