from typing import Tuple, Union
from typing import Sequence
from typing import Optional

from document import Paragraph
from historical_diff import Version, ParagraphNumber

class Annotation(Paragraph):
  def __init__(self, number: Tuple[Union[int, str]], text: str):
    self.contents = text
    self.number = ParagraphNumber(*number)
    if not self.number.annotation:
      raise IndexError("%s is not an annotation number" % self.number)

  def kind(self) -> str:
    raise TypeError("Annotation without a type", self.number, self.text)

  def html(self, inner):
    return f"<p class=annotation><b>{self.kind()}: </b>{inner}</p>"

class Reason(Annotation):
  def kind(self):
    return "Reason"
class Ramification(Annotation):
  def kind(self):
    return "Ramification"
class Proof(Annotation):
  def kind(self):
    return "Proof"
class IpmlementationNote(Annotation):
  def kind(self):
    return "Implementation Note"
class Discussion(Annotation):
  def kind(self):
    return "Discussion"
class ToBeHonest(Annotation):
  def kind(self):
    return "To be honest"

class Issue:
  def __init__(
      self,
      version: Version,
      target_rules: Sequence[str],
      l2_refs: Sequence[str],
      annotations: Sequence[Annotation] = [],
      l2_docs: Sequence[str] = [],
      affected_rules: Sequence[str] = [],
      deleted_rules: Sequence[str] = []) -> None:
    self.version = version
    self.target_rules = target_rules
    self.l2_refs = l2_refs
    self.l2_docs = l2_docs
    self.affected_rules = affected_rules
    self.deleted_rules = deleted_rules
    self.annotations = annotations



ISSUES = (
    Issue(
        Version(3, 0, 0),
        [], 
        [],  # TODO(egg): if this annotation thing ever makes it to the UTC, put an AI here.
        [
            Discussion(
                (1, 'a'),
                "This Annotated Line Breaking Algorithm contains the entire"
                " text of Section 6 of Unicode Standard Annex #14, Unicode Line"
                " Breaking Algorithm, plus certain annotations. The annotations"
                " give a more in-depth analysis of the algorithm. They describe"
                " the reason for each nonobvious rule, and point out"
                " interesting ramifications of the rules and interactions among"
                " the rules (interesting to Unicode maintainers, that is). (The"
                " text you are reading now is an annotation.)"),
            Ramification(
                (31, 'a'),
                "Lines do not start with spaces, except after a hard line break"
                " or at the start of text."),
            Ramification(
                (31, 'b'),
                "A sequence of spaces is unbreakable; prohibited breaks are"
                " expressed in subsequent rules by disallowing the break after"
                " the last space."),
        ]),

    Issue(Version(14, 0, 0),
          ["LB30b"],
          ["168-C8"]),
    Issue(Version(14, 0, 0),
          ["LB27"],
          ["163-A70"]),
    Issue(Version(13, 0, 0),
          ["LB30"],
          ["160-A75", "161-A47", "162-A42"]),
    Issue(Version(13, 0, 0),
          ["LB22"],
          ["142-A23", "160-A56"]),
    Issue(Version(11, 0, 0),
          ["LB8a"],
          ["149-A53"],
          l2_docs=["L2/17-074"]),
    # Creates 8a.  The original proposal targets LB23 and LB24, but the relevant
    # parts become LB23a per the next issue.
    Issue(Version(9, 0, 0),
          ["LB8a", "LB9", "LB10", "LB22", "LB23a", "LB30a", "LB30b"],
          ["146-A46", "147-C26"]),
    # Creates LB23a.
    Issue(
        Version(9, 0, 0),
        ["LB23", "LB23a", "LB24"],
        ["143-A4", "146-C19"],
        [
            Reason(
                (82, 5, 'a'),
                "This rule forbids breaking within currency symbols such as "
                " CA$ or JP¥, as well as stylized artist names such as “Travi$"
                " Scott”, “Ke$ha”, “Curren$y”, and “A$AP Rocky”"),
        ]),
    # Creates LB21b.
    Issue(
        Version(8, 0, 0),
        ["LB21b"],
        ["137-C9"],
        [
            Reason(
                (71, 4, 'a'),
                "From CLDR.  “Hebrew makes extensive use of the / character to"
                " create gender-neutral verb forms, with the feminine suffix"
                " coming after the slash. […] It is quite rare in Hebrew to use a"
                " slash other than in this context.” See CLDR-6616."),
        ]),
    Issue(Version(8, 0, 0),
          ["LB22"],
          ["142-C3"]),
    # Added LB30a.
    Issue(Version(6, 2, 0),
          ["LB30a"],
          ["131-C16", "132-C33"]),
    # Added LB21a.
    Issue(
        Version(6, 1, 0),
        ["LB21a"],
        ["125-A99"],  # Discussed in https://www.unicode.org/L2/L2011/11116-pre.htm#:~:text=Segmentation%20and%20Linebreak, approved in 129-A147.
        [
            Reason(
                (71, 2, 'a'),
                "“With <hebrew hyphen non-hebrew>, there is no break on either side of the hyphen.”"),
            Discussion(
                (71, 2, 'b'),
                "The Hebrew ICU “and” list format with a non-Hebrew last element"
                " provides an example of such a sequence: ⁧John ו-Michael⁩; with"
                " a Hebrew last word, the letter ו is prefixed to the word:"
                " יוחנן ומיכאל."
                " See ICU-21016."),
        ],
        l2_docs=["L2/11-141R"],
        affected_rules=["LB22", "LB23", "LB24", "LB28", "LB29", "LB30"]),
    Issue(Version(6, 1, 0),
          ["LB1"],
          ["129-C2"]),  # Rationale is in the review note https://www.unicode.org/reports/tr14/tr14-27d2.html#NS.
    Issue(Version(6, 0, 0),
          ["LB8"],
          ["121-C5"]),
    # Re-added LB30.
    Issue(Version(5, 2, 0),
          ["LB30"],
          ["114-A86, 120-M1"],
          affected_rules=["LB13", "LB16", "LB25"]),
    # Removed LB30.
    Issue(Version(5, 1, 0),
          [],
          ["114-C30"],
          deleted_rules=["LB30"]),
    # Split 12a from 12.
    Issue(Version(5, 1, 0),
          ["LB12a"],
          ["110-C17"],
          affected_rules=["LB12"]),
    # Added LB30 (2); changes LB18 (3), but that one gets split into LB24 and LB25.
    # Changes to discusssions of tailoring are from (5).
    Issue(Version(5, 0, 0),
          ["LB30", "LB24", "LB25"],
          ["105-C37"],
          [
              ToBeHonest(
                  (11, 3, 'a'),
                  "Implementations are not required to support the vertical"
                  " tabulation in class BK, nor to support the singleton class"
                  " NL.")
          ]),
    # Splits 18 into 24 and 25.
    Issue(Version(5, 0, 0),
          ["LB24", "LB25"],
          ["105-C6"]),
    # Splits 6 into 18b and 18c (4), removes 18b (5).
    Issue(Version(4, 1, 0),
          ["LB18b", "LB18c"],
          ["100-C40"],
          deleted_rules=["LB6", "LB18b"]),
    # Removes 7a.
    Issue(Version(4, 1, 0),
          [],
          ["100-M2"],
          deleted_rules=["LB7a"]),
    Issue(Version(4, 1, 0),
          ["LB7b"],
          ["102-C23"]),
    # Splits 13 from 11b.
    Issue(Version(4, 1, 0),
          ["LB11b", "LB13"],
          ["94-M3"]),
    # Creates 19b.
    Issue(Version(4, 0, 1),
          ["LB19b"],
          ["97-C25"]),
    # Splits 3b from 3a.
    Issue(Version(4, 0, 0),
          ["LB3a", "LB3b"],
          ["94-M2"],
          affected_rules=["LB3c"]),
    # Moves 15b to 18b (A).  Separate from the one below because the motion is 
    # only about 18b.
    Issue(Version(4, 0, 0),
          ["LB18b"],
          ["92-A64", "93-A96", "94-M4"]),
    # Adds 14a (F), adds 7c (J), moves 13 to 11b (K).
    Issue(Version(4, 0, 0),
          ["LB14a", "LB7c", "LB11b"],
          ["92-A64", "93-A96"]),
    # Splits 7b from 6.
    Issue(Version(4, 0, 0),
          ["LB6", "LB7b"],
          ["94-C6"]),
    Issue(Version(3, 2, 0),
          ["LB13"],
          ["81-M6", "85-M7"],
          l2_docs=["L2/00-258"])
)