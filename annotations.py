import inspect
from typing import Tuple, Union
from typing import Sequence
from typing import Optional

from document import Paragraph
from historical_diff import Version, ParagraphNumber

SECTION_6 = 361

class Annotation(Paragraph):
  def __init__(self, number: Tuple[Union[int, str]], text: str):
    self.contents = text
    self.number = ParagraphNumber(*number)
    if not self.number.annotation:
      raise IndexError("%s is not an annotation number" % self.number)

  def kind(self) -> str:
    return None

  def html(self, inner, version:Optional[Version]=None):
    title = (
        f"<ins class=changed-in-{version.html_class()}><b>{self.kind()}: </b></ins>"
        if self.kind() else "")
    return f"<p class=annotation>{title}{inner}</p>"

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
      paragraphs: Sequence[ParagraphNumber] = [],
      l2_docs: Sequence[str] = [],
      affected_rules: Sequence[str] = [],
      deleted_rules: Sequence[str] = []) -> None:
    self.source_line = inspect.getframeinfo(inspect.stack()[1][0]).lineno
    self.version = version
    self.target_rules = target_rules
    self.l2_refs = l2_refs
    self.l2_docs = l2_docs
    self.paragraphs = paragraphs
    self.affected_rules = affected_rules
    self.deleted_rules = deleted_rules
    self.annotations = annotations

  def __repr__(self):
    return "(Issue in %s, l. %s)" % (self.version, self.source_line)



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
            Annotation(
                (1, 'b'),
                "The structure of this document is heavily inspired by that of"
                " the Annotated Ada Reference Manual.  For a description of the"
                " various kinds of annotations, see paragraphs 1(2.dd) through"
                " 1(2.ll) in that document."),
            Annotation(
                (1, 'c'),
                "A version number of the form /v[.v[.v]] follows the paragraph"
                " number for any paragraph that has been modified from the"
                " original Unicode Line Breaking Algorithm (Unicode"
                " Version 3.0.0)."
                " Paragraph numbers are of the form pp{.nn}, where pp is a"
                " sequential numbering of the paragraphs of Version 3.0.0,"
                " and the nn are insertion numbers. For instance, the first"
                " paragraph inserted after paragraph 3 is numbered 3.1, the"
                " second is numbered 8.2, etc. A paragraph inserted between"
                " paragraphs 8.1 and 8.2 is numbered 8.1.1, a paragraph"
                " inserted between paragraphs 8 and 8.1 is numbered 8.0.1."
                " Inserted text is indicated by highlighting, and deleted text"
                " is indicated by strikethroughs. Colour is used to indicate"
                " the version of the change."
                " Deleted paragraphs are indicated by the text “This paragraph"
                " was deleted.”, or by a description of the new location of"
                " any text retained. Compare the Annotated Ada 2012 Reference"
                " Manual, Introduction (77.5)."),
            Annotation(
                (1, 'd'),
                "Annotations are numbered similarly, except that the first"
                " insertion number is alphabetic rather than numeric."),
            Discussion(
                (1, 'e'),
                "This document is available as an interactive web page; the bar"
                " on the right-hand side of the document allows for the"
                " selection of the base version from which changes are shown"
                " and the “head” version which determines the most recent"
                " changes shown.  Paragraph deleted by the base version or"
                " by earlier versions may be suppressed.  Clicking on a version"
                " number sets the head to that version and the base to the"
                " preceding version, thus showing the changes from that"
                " version.  These settings are reflected as URL parameters."),
            Ramification(
                (31, 'a'),
                "Lines do not start with spaces, except after a hard line break"
                " or at the start of text."),
            Ramification(
                (31, 'b'),
                "A sequence of spaces is unbreakable; a prohibited break after"
                " X is expressed in subsequent rules by disallowing the break"
                " after any spaces following X (X SP* ×), and a prohibited break"
                " by disallowing the break before X (× X)."),
            Reason(
                (47, 'a'),
                "× EX and × IS accomodate French typographical conventions in"
                " cases where a normal space (rather than NBSP or NNBSP, class"
                " GL) is used before the exclamation or question marks, or the"
                " colon and semicolon. × CL likewise caters to French"
                " « quotation marks » if QU has been resolved for French."
                " See [Suign98]."),
        ]),

    Issue(
        Version(14, 0, 0),
        [],
        ["167-A94", "168-C7", "168-C8"],
        [
            Reason(
                (101, 15, 'a'),
                "The property-based rule provides some degree of"
                " future-proofing, by preventing implementations running"
                " earlier of Unicode from breaking emoji sequences encoded"
                " in later versions.  Any future emoji will be encoded in the"
                " space preallocated as \p{Extended_Pictographic} in Unicode"
                " Version 13.0.0, see 168-C7."),
            Ramification(
                (101, 15, 'b'),
                "As emoji get encoded, new line break opportunities may appear"
                " between those that did not turn out to be an emoji base and"
                " subsequent (dangling) emoji modifiers."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 101, 13),
            ParagraphNumber(SECTION_6 + 101, 15),
        ]
        ),
    Issue(Version(14, 0, 0),
          [],
          ["163-A70"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 98, 12),
          ]),
    Issue(Version(13, 0, 0),
          [],
          ["160-A75", "161-A47", "162-A42"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 7),
              ParagraphNumber(SECTION_6 + 101, 8),
              ParagraphNumber(SECTION_6 + 101, 9, 1),
              ParagraphNumber(SECTION_6 + 101, 9, 2),
              ParagraphNumber(SECTION_6 + 101, 9, 3),
          ]),
    Issue(Version(13, 0, 0),
          [],
          ["142-A23", "160-A56"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 72),
              ParagraphNumber(SECTION_6 + 72, 1),
              ParagraphNumber(SECTION_6 + 72, 1, 1),
              ParagraphNumber(SECTION_6 + 72, 2),
              ParagraphNumber(SECTION_6 + 73),
              ParagraphNumber(SECTION_6 + 74),
          ]),
    Issue(Version(11, 0, 0),
          [],
          ["149-A53"],
          [
            Ramification(
                (40, 11, 'a'),
                "ZWJ and WJ differ in line breaking only when preceded by SP"
                " (and in the absence of ZW). This resolves to SP ÷ ZWJ by LB18"
                " unless LB14 applies."),
            Proof(
                (40, 11, 'b'),
                "ZWJ × is LB8a. LB9 implies X × ZWJ, where the exceptions for X"
                " are SP or Y such that Y ! or Y ÷ by that point."),
            Discussion(
                (40, 11, 'c'),
                "In contrast to SP CM which is either deprecated or anomalous,"
                " SP ZWJ can occur in practice, and SP ÷ ZWJ is desired; a"
                " leading ZWJ can be used to force a leading medial or final"
                " form, such as this final alif: ‍ا (contrast the isolated ا)."),
            Discussion(
                (40, 7, 'a'),
                "Absent tailoring, this rule has no effect in the case of ZWJ."
                " The breaks on both sides of ZWJ have already been resolved,"
                " except in SP ZWJ, which gets resolved at the latest in LB18"
                " without class AL being involved.  The rule is written like"
                " this for consistency with combining marks following LB9."),
          ],
          l2_docs=["L2/17-074"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 1, 2),
              ParagraphNumber(SECTION_6 + 33, 1, 3),
              ParagraphNumber(SECTION_6 + 33, 1, 4),
              ParagraphNumber(SECTION_6 + 33, 1, 5),
          ]),
    # Creates 8a.  The original proposal targets LB23 and LB24, but the relevant
    # parts become LB23a per the next issue.
    Issue(Version(9, 0, 0),
          [],
          ["146-A46", "147-C26"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 1, 2),
              ParagraphNumber(SECTION_6 + 33, 1, 3),
              ParagraphNumber(SECTION_6 + 33, 1, 4),
              ParagraphNumber(SECTION_6 + 33, 1, 5),
              ParagraphNumber(SECTION_6 + 40, 2),
              ParagraphNumber(SECTION_6 + 40, 3),
              ParagraphNumber(SECTION_6 + 40, 5),
              ParagraphNumber(SECTION_6 + 40, 6),
              ParagraphNumber(SECTION_6 + 72, 2),
              ParagraphNumber(SECTION_6 + 82, 0, 1),
              ParagraphNumber(SECTION_6 + 82, 0, 2),
              ParagraphNumber(SECTION_6 + 82, 0, 3),
              ParagraphNumber(SECTION_6 + 101, 10),
              ParagraphNumber(SECTION_6 + 101, 11),
              ParagraphNumber(SECTION_6 + 101, 12),
              ParagraphNumber(SECTION_6 + 101, 13),
              ParagraphNumber(SECTION_6 + 101, 14),
          ]),
    # Drops the pair table.  See the PRI comments which say it can’t implement
    # the new rules, and the review note which says it wasn’t updated.
    Issue(
        Version(10, 0, 0),
        [],
        ["147-A79"],
        paragraphs=[ParagraphNumber(SECTION_6 + 3)],
        ),
    # Creates LB23a.
    Issue(
        Version(9, 0, 0),
        [],
        ["143-A4", "146-C19"],
        [
            Reason(
                (82, 5, 'a'),
                "This rule forbids breaking within currency symbols such as "
                " CA$ or JP¥, as well as stylized artist names such as “Travi$"
                " Scott”, “Ke$ha”, “Curren$y”, and “A$AP Rocky”."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 80),
            ParagraphNumber(SECTION_6 + 80, 1),
            ParagraphNumber(SECTION_6 + 82, 0, 1),
            ParagraphNumber(SECTION_6 + 82, 0, 2),
            ParagraphNumber(SECTION_6 + 82, 0, 3),
            ParagraphNumber(SECTION_6 + 82, 1),
            ParagraphNumber(SECTION_6 + 82, 2),
            ParagraphNumber(SECTION_6 + 82, 3),
            ParagraphNumber(SECTION_6 + 82, 4),
            ParagraphNumber(SECTION_6 + 82, 5),
        ]),
    # Creates LB21b.
    Issue(
        Version(8, 0, 0),
        [],
        ["137-C9"],
        [
            Reason(
                (71, 4, 'a'),
                "From CLDR.  “Hebrew makes extensive use of the / character to"
                " create gender-neutral verb forms, with the feminine suffix"
                " coming after the slash. […] It is quite rare in Hebrew to use a"
                " slash other than in this context.” See CLDR-6616."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 71, 3),
            ParagraphNumber(SECTION_6 + 71, 4),
        ]),
    Issue(Version(8, 0, 0),
          [],
          ["142-C3"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 72),
              ParagraphNumber(SECTION_6 + 72, 1, 1),
          ]),
    # Added LB30a.
    Issue(Version(6, 2, 0),
          [],
          ["131-C16", "132-C33"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 10),
              ParagraphNumber(SECTION_6 + 101, 11),
          ]),
    # Added LB21a.
    Issue(
        Version(6, 1, 0),
        [],
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
        paragraphs=[
            ParagraphNumber(SECTION_6 + 71, 1),
            ParagraphNumber(SECTION_6 + 71, 2),
            ParagraphNumber(SECTION_6 + 72, 1),
            ParagraphNumber(SECTION_6 + 81),
            ParagraphNumber(SECTION_6 + 82),
            ParagraphNumber(SECTION_6 + 82, 3),
            ParagraphNumber(SECTION_6 + 82, 4),
            ParagraphNumber(SECTION_6 + 101),
            ParagraphNumber(SECTION_6 + 101, 2),
            ParagraphNumber(SECTION_6 + 101, 7),
            ParagraphNumber(SECTION_6 + 101, 8),
        ]),
    Issue(Version(6, 1, 0),
          [],
          ["129-C2"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 13),
              ParagraphNumber(SECTION_6 + 13, 2),
              ParagraphNumber(SECTION_6 + 13, 3),
              ParagraphNumber(SECTION_6 + 13, 4),
              ParagraphNumber(SECTION_6 + 13, 5),
              ParagraphNumber(SECTION_6 + 13, 6),
              ParagraphNumber(SECTION_6 + 13, 7),
        ]),  # Rationale is in the review note https://www.unicode.org/reports/tr14/tr14-27d2.html#NS.
    Issue(
        Version(6, 0, 0),
        [],
        ["121-C5"],
        [
            Discussion(
                (33, 'a'),
                "The zero width space is a hint to the line breaking algorithm,"
                " hinting a break. Its inverse is the word joiner, see LB11."
                " When they contradict each other, the zero width space wins."
                " However, this rule needs to be more complicated than LB11: "
                " if it were simply ZW ÷ before LB7, it would allow for spaces"
                " at the beginning of a line.  Instead it acts through any"
                " sequence of spaces following it."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 32),
            ParagraphNumber(SECTION_6 + 33),
            ParagraphNumber(SECTION_6 + 33, 1, 1),
        ]),
    # Re-added LB30.
    Issue(Version(5, 2, 0),
          [],
          ["114-A86", "120-M1"],
          paragraphs=[
            ParagraphNumber(SECTION_6 + 84),
            ParagraphNumber(SECTION_6 + 44, 1),
            ParagraphNumber(SECTION_6 + 53),
            ParagraphNumber(SECTION_6 + 87, 1, 0, 1),
            ParagraphNumber(SECTION_6 + 87, 1, 1, 1),
            ParagraphNumber(SECTION_6 + 98, 5),
            ParagraphNumber(SECTION_6 + 101, 3),
            ParagraphNumber(SECTION_6 + 101, 7),
            ParagraphNumber(SECTION_6 + 101, 8),
            ParagraphNumber(SECTION_6 + 101, 9),
        ]),
    # Removed LB30.
    Issue(Version(5, 1, 0),
          [],
          ["114-C30"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 3),
              ParagraphNumber(SECTION_6 + 101, 4),
              ParagraphNumber(SECTION_6 + 101, 5),
              ParagraphNumber(SECTION_6 + 101, 6),
          ]),
    Issue(Version(5, 1, 0),
          [],
          [],
          [
              Discussion(
                  (51, 1, 'a'),
                  "When a quote is known to be opening or closing, OP and CL"
                  " should respectively be used.  Class QU (for ambiguous"
                  " quotation marks) is a Unicode innovation compared to the"
                  " ancestor standard JIS X 4051, necessitated by the variety"
                  " of quotation mark styles across languages; see The Unicode"
                  " Standard, Chapter 6."),
              Ramification(
                  (51, 1, 'b'),
                  "The rules pertaining to class QU in the algorithm may be"
                  " expressed as heuristics for its resolution into OP and CL,"
                  " as follows, where treating a quotation mark as both OP and"
                  " CL means disallowing breaks according to both"
                  " interpretations:"),
              Annotation(
                  (51, 1, 'c'),
                  "Treat QU as OP in QU SP+ OP. (LB15)"),
              Annotation(
                  (51, 1, 'd'),
                  "Treat QU as OP in QU [^SP]. (LB19)"),
              Annotation(
                  (51, 1, 'e'),
                  "Treat QU as CL in [^SP] QU. (LB19)"),
              Discussion(
                  (51, 1, 'f'),
                  "While the latter two heuristics are self-explanatory, the"
                  " first one (LB15) is weird.  It applies to cases such"
                  " as the opening quotation mark in « [Le livre] tuera"
                  " [l’édifice] », but not to the closing quotation mark."
                  " It can misfire, as in “All Gaul is divided into three"
                  " parts” ×(Caes. BGall. 1.1.1)."),
              Annotation(
                  (51, 1, 'g'),
                  " Generally, whereas the algorithm correctly deals with"
                  " spaces before French !?:;, it does not prevent break"
                  " opportunities inside of French quotation marks, unless"
                  " no-break space is used."),
              
          ],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 51, 1),
          ]),
    # Split 12a from 12.
    Issue(Version(5, 1, 0),
          [],
          ["110-C17"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 40, 13),
              ParagraphNumber(SECTION_6 + 40, 14),
              ParagraphNumber(SECTION_6 + 40, 16),
              ParagraphNumber(SECTION_6 + 40, 18),
              ParagraphNumber(SECTION_6 + 40, 19),
              ParagraphNumber(SECTION_6 + 40, 20),
              ParagraphNumber(SECTION_6 + 40, 21),
              ParagraphNumber(SECTION_6 + 40, 22),
              ParagraphNumber(SECTION_6 + 42),
          ]),
    # Added LB30 (2); changes LB18 (3), but that one gets split into LB24 and LB25.
    # Changes to discusssions of tailoring are from (5).
    Issue(Version(5, 0, 0),
          [],
          ["105-C37"],
          [
              ToBeHonest(
                  (11, 3, 'a'),
                  "Implementations are not required to support the vertical"
                  " tabulation in class BK, nor to support the singleton class"
                  " NL.")
          ],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 82, 1),
              ParagraphNumber(SECTION_6 + 82, 2),
              ParagraphNumber(SECTION_6 + 82, 3),
              ParagraphNumber(SECTION_6 + 82, 4),
              ParagraphNumber(SECTION_6 + 84),
              ParagraphNumber(SECTION_6 + 86),
              ParagraphNumber(SECTION_6 + 87),
              ParagraphNumber(SECTION_6 + 87, 1, 1),
              ParagraphNumber(SECTION_6 + 87, 1, 2),
              ParagraphNumber(SECTION_6 + 87, 1, 3),
              ParagraphNumber(SECTION_6 + 87, 1, 4),
              ParagraphNumber(SECTION_6 + 87, 1, 5),
              ParagraphNumber(SECTION_6 + 87, 1, 6),
              ParagraphNumber(SECTION_6 + 87, 1, 7),
              ParagraphNumber(SECTION_6 + 87, 5),
              ParagraphNumber(SECTION_6 + 87, 6),
              ParagraphNumber(SECTION_6 + 87, 7),
              ParagraphNumber(SECTION_6 + 87, 8),
              ParagraphNumber(SECTION_6 + 88),
              ParagraphNumber(SECTION_6 + 90),
              ParagraphNumber(SECTION_6 + 98),
              ParagraphNumber(SECTION_6 + 98, 5),
              ParagraphNumber(SECTION_6 + 101, 3),
              ParagraphNumber(SECTION_6 + 101, 4),
              ParagraphNumber(SECTION_6 + 101, 5),
              ParagraphNumber(SECTION_6 + 101, 6),
          ]),
    # Splits 18 into 24 and 25.
    Issue(Version(5, 0, 0),
          [],
          ["105-C6"],
          paragraphs=[
            ParagraphNumber(SECTION_6 + 82, 1),
            ParagraphNumber(SECTION_6 + 82, 2),
            ParagraphNumber(SECTION_6 + 82, 3),
            ParagraphNumber(SECTION_6 + 82, 4),
            ParagraphNumber(SECTION_6 + 84),
            ParagraphNumber(SECTION_6 + 86),
            ParagraphNumber(SECTION_6 + 87),
            ParagraphNumber(SECTION_6 + 87, 1, 1),
            ParagraphNumber(SECTION_6 + 87, 1, 2),
            ParagraphNumber(SECTION_6 + 87, 1, 3),
            ParagraphNumber(SECTION_6 + 87, 1, 4),
            ParagraphNumber(SECTION_6 + 87, 1, 5),
            ParagraphNumber(SECTION_6 + 87, 1, 6),
            ParagraphNumber(SECTION_6 + 87, 1, 7),
            ParagraphNumber(SECTION_6 + 87, 5),
            ParagraphNumber(SECTION_6 + 87, 6),
            ParagraphNumber(SECTION_6 + 87, 7),
            ParagraphNumber(SECTION_6 + 87, 8),
            ParagraphNumber(SECTION_6 + 88),
            ParagraphNumber(SECTION_6 + 90),
            ParagraphNumber(SECTION_6 + 98),
            ParagraphNumber(SECTION_6 + 98, 5),
        ]),
    # Splits 6 into 18b and 18c (4), removes 18b (5).
    Issue(Version(4, 1, 0),
          [],
          ["100-C40"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 3),
              ParagraphNumber(SECTION_6 + 33, 4),
              ParagraphNumber(SECTION_6 + 33, 5),
              ParagraphNumber(SECTION_6 + 34),
              ParagraphNumber(SECTION_6 + 98, 1),
              ParagraphNumber(SECTION_6 + 98, 2),
              ParagraphNumber(SECTION_6 + 98, 3),
              ParagraphNumber(SECTION_6 + 98, 4),
              ParagraphNumber(SECTION_6 + 98, 5),
              ParagraphNumber(SECTION_6 + 98, 6),
              ParagraphNumber(SECTION_6 + 98, 6),
              ParagraphNumber(SECTION_6 + 98, 7),
              ParagraphNumber(SECTION_6 + 98, 7),
              ParagraphNumber(SECTION_6 + 98, 8),
              ParagraphNumber(SECTION_6 + 98, 8),
              ParagraphNumber(SECTION_6 + 98, 9),
              ParagraphNumber(SECTION_6 + 98, 9),
              ParagraphNumber(SECTION_6 + 98, 10),
              ParagraphNumber(SECTION_6 + 98, 10),
              ParagraphNumber(SECTION_6 + 98, 11),
              ParagraphNumber(SECTION_6 + 98, 11),
              ParagraphNumber(SECTION_6 + 98, 12),
              ParagraphNumber(SECTION_6 + 98, 12),
              ParagraphNumber(SECTION_6 + 98, 13),
              ParagraphNumber(SECTION_6 + 98, 13),
              ParagraphNumber(SECTION_6 + 98, 14),
              ParagraphNumber(SECTION_6 + 98, 14),
              ParagraphNumber(SECTION_6 + 98, 15),
              ParagraphNumber(SECTION_6 + 98, 15),
          ]),
    # Removes 7a.
    Issue(Version(4, 1, 0),
          [],
          ["100-M2"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 39),
              ParagraphNumber(SECTION_6 + 39, 1),
              ParagraphNumber(SECTION_6 + 40),
              ParagraphNumber(SECTION_6 + 40, 1),
          ]),
    Issue(Version(4, 1, 0),
          [],
          ["102-C23"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 40, 2),
              ParagraphNumber(SECTION_6 + 40, 3),
              ParagraphNumber(SECTION_6 + 40, 3, 1),
              ParagraphNumber(SECTION_6 + 40, 4),
          ]),
    # Splits 13 from 11b.
    Issue(Version(4, 1, 0),
          [],
          ["94-M3"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 53, 4),
              ParagraphNumber(SECTION_6 + 53, 5),
              ParagraphNumber(SECTION_6 + 53, 6),
              ParagraphNumber(SECTION_6 + 53, 7),
              ParagraphNumber(SECTION_6 + 53, 8),
              ParagraphNumber(SECTION_6 + 56, 3),
              ParagraphNumber(SECTION_6 + 56, 4),
              ParagraphNumber(SECTION_6 + 56, 5),
          ]),
    # Creates 19b.
    Issue(Version(4, 0, 1),
          [],
          ["97-C25"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 1),
              ParagraphNumber(SECTION_6 + 101, 2),
          ]),
    # Splits 3b from 3a.
    Issue(Version(4, 0, 0),
          [],
          ["94-M2"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 21, 1, 1),
              ParagraphNumber(SECTION_6 + 21, 1, 2),
              ParagraphNumber(SECTION_6 + 22),
              ParagraphNumber(SECTION_6 + 25, 1),
              ParagraphNumber(SECTION_6 + 26),
              ParagraphNumber(SECTION_6 + 27),
              ParagraphNumber(SECTION_6 + 27, 1),
          ]),
    # Moves 15b to 18b (A).  Separate from the one below because the motion is 
    # only about 18b.
    Issue(Version(4, 0, 0),
          [],
          ["92-A64", "93-A96", "94-M4"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 98, 1),
              ParagraphNumber(SECTION_6 + 98, 2),
              ParagraphNumber(SECTION_6 + 98, 3),
          ]),
    # Adds 14a (F), adds 7c (J), moves 13 to 11b (K).
    Issue(Version(4, 0, 0),
          [],
          ["92-A64", "93-A96"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 40, 5),
              ParagraphNumber(SECTION_6 + 40, 6),
              ParagraphNumber(SECTION_6 + 40, 7),
              ParagraphNumber(SECTION_6 + 53, 4),
              ParagraphNumber(SECTION_6 + 53, 5),
              ParagraphNumber(SECTION_6 + 53, 6),
              ParagraphNumber(SECTION_6 + 63, 1),
              ParagraphNumber(SECTION_6 + 63, 2),
              ParagraphNumber(SECTION_6 + 63, 3),
              ParagraphNumber(SECTION_6 + 63, 4),
          ]),
    # Splits 7b from 6.
    Issue(Version(4, 0, 0),
          [],
          ["94-C6"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 3),
              ParagraphNumber(SECTION_6 + 33, 4),
              ParagraphNumber(SECTION_6 + 33, 5),
              ParagraphNumber(SECTION_6 + 35),
              ParagraphNumber(SECTION_6 + 40, 2),
              ParagraphNumber(SECTION_6 + 40, 3),
              ParagraphNumber(SECTION_6 + 40, 4),
          ]),
    Issue(Version(3, 2, 0),
          [],
          ["81-M6", "85-M7"],
          paragraphs=[ParagraphNumber(SECTION_6 + 58)],
          l2_docs=["L2/00-258"])
)