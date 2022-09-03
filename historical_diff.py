import difflib
from functools import total_ordering
import html
import itertools
import re
from typing import Optional, Sequence, Tuple, Union

@total_ordering
class Version:
  def __init__(self, *components: int):
    self.components = components

  def __hash__(self):
    return hash(self.components)

  def __eq__(self, other):
    return isinstance(other, Version) and self.components == other.components

  def __lt__(self, other):
    return self.components < other.components

  def __repr__(self):
    return f"Version({', '.join(str(v) for v in self.components)})"

  def __str__(self):
    return ".".join(str(v) for v in self.components)

  def html_class(self):
    return "-".join(str(v) for v in self.components)

@total_ordering
class ParagraphNumber:
  def __init__(self, *components: Union[int, str]):
    self.main: list[int] = []
    self.annotation: list[Union[str, int]] = []
    for component in components:
      if self.annotation:
        if not isinstance(component, int):
          raise TypeError("Unexpected type %s in annotation part of paragraph number %r" % (type(component), components))
        self.annotation.append(component)
      elif isinstance(component, str):
        if len(component) > 1 or component < 'a' or component > 'z':
          raise ValueError("Unexpected %s in paragraph number %r" % (component, components))
        self.annotation.append(component)
      else:
        if not isinstance(component, int):
          raise TypeError("Unexpected type %s in paragraph number %r" % (type(component), components))
        self.main.append(component)
    self.main = tuple(self.main)
    self.annotation = tuple(self.annotation)

  def insertion(self, insertion_number):
    return ParagraphNumber(*self.main, *self.annotation, insertion_number)

  def __hash__(self):
    return hash((self.main, self.annotation))

  def __eq__(self, other):
    return (isinstance(other, ParagraphNumber) and
            self.main == other.main and
            self.annotation == other.annotation)

  def __lt__(self, other):
    return (self.main, self.annotation) < (other.main, other.annotation)

  def __repr__(self):
    return f"ParagraphNumber({', '.join(repr(n) for part in (self.main, self.annotation) for n in part)})"

  def __str__(self):
    return ".".join(str(n) for part in (self.main, self.annotation) for n in part)

def get_inserted_paragraph_number(
    previous_number: ParagraphNumber,
    next_number: Optional[ParagraphNumber]) -> Tuple[ParagraphNumber, int]:
  if (previous_number.annotation) or (next_number and next_number.annotation):
    raise IndexError("Inserting between annotations %s and %s" % (previous_number,  next_number))
  if not next_number or len(previous_number.main) == len(next_number.main) + 1:
    prefix = previous_number.main[:-1]
    offset = previous_number.main[-1] + 1
  elif len(previous_number.main) == len(next_number.main):
    prefix = previous_number.main
    offset = 1
  elif next_number.main[-1] == 1:
    prefix = (*next_number.main[:-1], 0)
    offset = 1
  else:
    raise IndexError(previous_number, next_number)
  return (ParagraphNumber(*prefix), offset)

class History:
  def remove(self, version):
    pass

  def value(self):
    return ""

  def value_at(self, version):
    return ""

  def present(self):
    return False

  def absent(self):
    return not self.present()

  def last_changed(self):
    return None

class AtomHistory(History):
  def __init__(self, version, c):
    self.text = c
    self.added = version
    self.removed = None

  def value(self):
    return self.text

  def value_at(self, version):
    return self.text if version >= self.added and (not self.removed or version < self.removed) else ""

  def remove(self, version):
    if self.added == version:
      print("ERROR:", self.text, "added and removed in", version)
    self.removed = version

  def present(self):
    return self.added and not self.removed

  def last_changed(self):
    return self.removed or self.added

class SequenceHistory(History):
  def __init__(
      self,
      junk=lambda x: x.isspace(),
      element_history=AtomHistory,
      check_and_get_elements=lambda x, h, version, *context: x,
      number_nicely=False):
    self.element_history = element_history
    self.elements : list[Tuple[ParagraphNumber, History]] = []
    self.check_and_get_elements = check_and_get_elements
    self.junk = junk
    self.number_nicely = number_nicely

  def current_text(self):
    return "".join(c.value() for _, c in self.elements if c.present())

  def present(self):
    return any(c.present() for _, c in self.elements)

  def remove(self, version, *context):
    self.add_version(version, [], *context)

  def value(self):
    return "".join(c.value() for _, c in self.elements if c.present())

  def value_at(self, version):
    return "".join(c.value_at(version) for _, c in self.elements)

  def last_changed(self):
    return max(c.last_changed() for _, c in self.elements)

  def add_version(self, version, new_text, *context):
    new_text = self.check_and_get_elements(new_text, self, version, *context)
    indexing : Sequence[Tuple[Optional[int], Tuple[ParagraphNumber, History]]] = []
    i = 0
    for n, c in self.elements:
      if c.present():
        indexing.append((i, (n, c)))
        i += 1
      else:
        indexing.append((None, (n, c)))

    diff = difflib.SequenceMatcher(
      self.junk,
      [c.value() for _, c in self.elements if c.present()],
      [self.element_history(version, element).value() for element in new_text]).get_opcodes()
    text_changed = False
    for instruction in diff:
      (operation, old_begin, old_end, new_begin, new_end) = instruction
      if operation == "equal":
        continue
      elif operation == "replace":
        if (isinstance(self.elements[0][1], SequenceHistory) and
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
          for old_index, (n, c) in indexing:
            if old_index is None:
              continue
            elif old_index >= old_end:
              break
            elif old_index >= old_begin:
              c.remove(version)
        elif operation == "insert":
          text_changed = True
          inserted_histories = [self.element_history(version, c)
                                for c in new_text[new_begin:new_end]]
          if new_begin == 0:
            if indexing:
              first_number = indexing[0][1][0]
              if first_number.main[-1] != 1:
                raise IndexError(first_number)
              inserted = [(None, (first_number.insertion(0).insertion(1 + i) , c))
                          for i, c in enumerate(inserted_histories)]
            else:
              inserted = [(None, (ParagraphNumber(1 + i) , c))
                          for i, c in enumerate(inserted_histories)]
            indexing = inserted + indexing
          else:
            for i, (old_index, (n, c)) in enumerate(indexing):
              if old_index is None:
                continue
              elif old_index + 1 == old_begin:
                # We are inserting after paragraph n.
                previous_number = indexing[i][1][0]
                next_number = indexing[i+1][1][0] if i + 1 < len(indexing) else None
                prefix, offset = get_inserted_paragraph_number(previous_number, next_number)
                if self.number_nicely:
                  # Instead of inserting immediately after paragraph n, see if we 
                  # can insert at a higher level by skipping some deleted paragraphs.
                  for j in itertools.count(i+1):
                    if j == len(indexing) or indexing[j][1][1].present():
                      break
                    previous_number = indexing[j][1][0]
                    next_number = indexing[j+1][1][0] if j+1 < len(indexing) else None
                    p, o = get_inserted_paragraph_number(previous_number, next_number)
                    if len(prefix.main) >= len(p.main):
                      prefix, offset = p, o
                      i = j

                inserted = [(None, (prefix.insertion(offset + i) , c))
                            for i, c in enumerate(inserted_histories)]
                before = indexing[:i+1]
                after = indexing[i+1:]
                indexing = before + inserted + after
                break
            else:
              raise Exception("Failed to insert")
        elif operation == "replace":
          i = new_begin
          for old_index, (n, c) in indexing:
            if old_index is None:
              continue
            elif old_index >= old_end:
              break
            elif old_index >= old_begin:
              c.add_version(version, new_text[i], *context, n)
              i += 1
          
    self.elements = [c for _, c in indexing]
    return text_changed

  def html(self):
    added = None
    removed = None
    versions = set()
    text = ""
    for _, c in self.elements:
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
          text += f'<del class="changed-in-{removed.html_class()}">'
      if c.added != added:
        if added:
          text += "</ins>"
        added = c.added
        if added:
          text += f'<ins class="changed-in-{added.html_class()}">'
      text += html.escape(c.value()).replace('\u2028', '<br>')
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
