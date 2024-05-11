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
      l2_refs: Sequence[str],
      annotations: Sequence[Annotation] = [],
      paragraphs: Sequence[ParagraphNumber] = [],
      l2_docs: Sequence[str] = [],
      pri: Sequence[str] = []) -> None:
    self.source_line = inspect.getframeinfo(inspect.stack()[1][0]).lineno
    self.version = version
    self.l2_refs = l2_refs
    self.l2_docs = l2_docs
    self.paragraphs = paragraphs
    self.annotations = annotations
    self.pri = pri

  def __repr__(self):
    return "(Issue in %s, l. %s)" % (self.version, self.source_line)



ISSUES = (
    Issue(
        Version(3, 0, 0),
        ["175-A67"],
        [
            Discussion(
                (10, 'a'),
                "This Annotated Line Breaking Algorithm contains the entire"
                " text of Unicode Standard Annex #14, Unicode Line"
                " Breaking Algorithm, plus certain annotations. The annotations"
                " give a more in-depth analysis of the algorithm. They describe"
                " the reason for each nonobvious rule, and point out"
                " interesting ramifications of the rules and interactions among"
                " the rules (interesting to Unicode maintainers, that is). (The"
                " text you are reading now is an annotation.)"),
            Annotation(
                (10, 'b'),
                "The structure of this document is heavily inspired by that of"
                " the Annotated Ada Reference Manual.  For a description of the"
                " various kinds of annotations, see paragraphs 1(2.dd) through"
                " 1(2.ll) in that document."),
            Annotation(
                (10, 'c'),
                "A version number of the form /v[.v[.v]] follows the paragraph"
                " number for any paragraph that has been modified from the"
                " original Unicode Line Breaking Algorithm (Unicode"
                " Version 3.0.0)."
                " Paragraph numbers are of the form pp{.nn}, where pp is a"
                " sequential numbering of the paragraphs of Version 3.0.0,"
                " and the nn are insertion numbers. For instance, the first"
                " paragraph inserted after paragraph 3 is numbered 3.1, the"
                " second is numbered 3.2, etc. A paragraph inserted between"
                " paragraphs 3.1 and 3.2 is numbered 3.1.1, a paragraph"
                " inserted between paragraphs 3 and 3.1 is numbered 3.0.1,"
                " a paragraph inserted between paragraphs 3 and 3.0.1 is"
                " numbered 3.-1.1."
                " Inserted text is indicated by highlighting, and deleted text"
                " is indicated by strikethroughs. Colour is used to indicate"
                " the version of the change."
                " Deleted paragraphs are indicated by the text “This paragraph"
                " was deleted.”, or by a description of the new location of"
                " any text retained. Compare the Annotated Ada 2012 Reference"
                " Manual, Introduction (77.5)."),
            Annotation(
                (10, 'd'),
                "Annotations are numbered similarly, except that the first"
                " insertion number is alphabetic rather than numeric."),
            Discussion(
                (10, 'e'),
                "This document is available as an interactive web page; the bar"
                " on the right-hand side of the document allows for the"
                " selection of the base version from which changes are shown"
                " and the “head” version which determines the most recent"
                " changes shown.  Paragraph deleted by the base version or"
                " by earlier versions may be suppressed.  Clicking on a version"
                " number sets the head to that version and the base to the"
                " preceding version, thus showing the changes from that"
                " version.  These settings are reflected as URL parameters."),
            ToBeHonest(
                (12, 'a'),
                "The document that has been reviewed by the UTC is the actual"
                " UAX #14, available at"
                " https://www.unicode.org/unicode/reports/tr14/."
                " While the text outside of the annotations comes from that"
                " UAX, it has been processed in a way that is not stable and"
                " may alter its meaning; in particular, most formatting is"
                " lost."),
            Annotation(
                (12, 'b'),
                "The annotations have not been considered, reviewed, nor"
                " approved by the UTC nor by any other Technical Committee."),
            Annotation(
                (12, 'c'),
                "This Annotated UAX is not a stable document."
                " It has not been approved by any of the Unicode Technical"
                " Committees, nor is it part of the Unicode Standard or any"
                " other Unicode specification."),
            Ramification(
                (SECTION_6 + 31, 'a'),
                "Lines do not start with spaces, except after a hard line break"
                " or at the start of text."),
            Ramification(
                (SECTION_6 + 31, 'b'),
                "A sequence of spaces is unbreakable; a prohibited break after"
                " X is expressed in subsequent rules by disallowing the break"
                " after any spaces following X (X SP* ×), and a prohibited break"
                " before X by disallowing the break before X (× X)."),
            Reason(
                (SECTION_6 + 47, 'a'),
                "× EX and × IS accomodate French typographical conventions in"
                " cases where a normal space (rather than NBSP or NNBSP, class"
                " GL) is used before the exclamation or question marks, or the"
                " colon and semicolon. × CL likewise caters to French"
                " « quotation marks » if QU has been resolved for French."
                " See [Suign98]."),
            Ramification(
                (400, 1, 'a'),
                "The “do not break” part of these rules does not require extended"
                " context, but the “treat as” means that most subsequent rules"
                " implicitly have extended context across combining marks."),
            Ramification(
                (410, 'a'),
                "This rule requires extended context."),
            Ramification(
                (412, 'a'),
                "This rule requires extended context."),
            Ramification(
                (414, 'a'),
                "This rule requires extended context."),
        ]),

    Issue(
        Version(3, 1, 0),
        [],  # Adds LB11a with a description inconistent with the formula, based on the pair table.
        paragraphs=[
            ParagraphNumber(414, 1),
            ParagraphNumber(414, 2),
            ParagraphNumber(596, 8),
        ]),
    Issue(
        Version(4, 1, 0),
        [],  # Changes the formula of LB11a to match the description.
        [
            Ramification(
                (414, 2, 'a'),
                "This rule requires extended context."),
        ],
        paragraphs=[
            ParagraphNumber(596, -3, 1, 12),
        ]),
    Issue(
        Version(14, 0, 0),
        ["167-A94", "168-C7", "168-C8", "168-A98"],
        [
            Reason(
                (SECTION_6 + 101, 15, 'a'),
                "The property-based rule provides some degree of"
                " future-proofing, by preventing implementations running"
                " earlier of Unicode from breaking emoji sequences encoded"
                " in later versions.  Any future emoji will be encoded in the"
                " space preallocated as \p{Extended_Pictographic} in Unicode"
                " Version 13.0.0, see 168-C7."),
            Ramification(
                (SECTION_6 + 101, 15, 'b'),
                "As emoji get encoded, new line break opportunities may appear"
                " between those that did not turn out to be an emoji base and"
                " subsequent (dangling) emoji modifiers."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 101, 13),
            ParagraphNumber(SECTION_6 + 101, 15),
            ParagraphNumber(596, 53),
        ],
        l2_docs=["L2/21-135R"]),
    Issue(Version(14, 0, 0),
          ["163-A70"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 98, 12),
              ParagraphNumber(596, 52)
          ]),
    Issue(Version(13, 0, 0),
          ["160-A75", "161-A47", "162-A42"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 7),
              ParagraphNumber(SECTION_6 + 101, 8),
              ParagraphNumber(SECTION_6 + 101, 9, 1),
              ParagraphNumber(SECTION_6 + 101, 9, 2),
              ParagraphNumber(SECTION_6 + 101, 9, 3),
          ],
          pri=["406@Mon Oct 14 18:46:18 CDT 2019"]),
    Issue(Version(13, 0, 0),
          ["142-A23", "160-A56"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 72),
              ParagraphNumber(SECTION_6 + 72, 1),
              ParagraphNumber(SECTION_6 + 72, 1, 1),
              ParagraphNumber(SECTION_6 + 72, 2),
              ParagraphNumber(SECTION_6 + 73),
              ParagraphNumber(SECTION_6 + 74),
          ]),
    # Remove the RHS of LB8a.
    Issue(Version(11, 0, 0),
          ["149-A53", "155-A27", "155-C14", "155-A112"],
          [
            Discussion(
                (401, 4, 'a'),
                "Absent tailoring, this rule has no effect in the case of ZWJ."
                " The breaks on both sides of ZWJ have already been resolved,"
                " except in SP ZWJ, which gets resolved at the latest in LB18"
                " without classes AL nor ZWJ being involved as extended"
                " context."
                " The rule is written like this for consistency with combining"
                " marks following LB9."),
            Discussion(
                (401, 4, 'b'),
                "In contrast to SP CM which is either deprecated or anomalous,"
                " SP ZWJ can occur in practice, and SP ÷ ZWJ is desired; a"
                " leading ZWJ can be used to force a leading medial or final"
                " form, such as this final alif: ‍ا (contrast the isolated ا)."),
          ],
          l2_docs=["L2/17-074"],
          paragraphs=[
              ParagraphNumber(350, 3),
              ParagraphNumber(SECTION_6 + 33, 1, 2),
              ParagraphNumber(SECTION_6 + 33, 1, 3),
              ParagraphNumber(SECTION_6 + 33, 1, 4),
              ParagraphNumber(SECTION_6 + 33, 1, 5),
              ParagraphNumber(596, 29),
          ]),
    # Creates 8a.  The original proposal targets LB23 and LB24, but the relevant
    # parts become LB23a per the next issue.
    Issue(Version(9, 0, 0),
          ["146-A46", "147-C26"],
          [
            Ramification(
                (462, 12, 'a'),
                "This rule requires extended context."),
          ],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 1, 2),
              ParagraphNumber(SECTION_6 + 33, 1, 3),
              ParagraphNumber(SECTION_6 + 33, 1, 4),
              ParagraphNumber(SECTION_6 + 33, 1, 5),
              ParagraphNumber(397),
              ParagraphNumber(398),
              ParagraphNumber(401, 2),
              ParagraphNumber(401, 3),
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
        ["147-A79"],
        [
            Discussion(
                (46, 0, 1, 'a'),
                "While many rules depend only on the code points either side of"
                " the break (those of the form A # B or simply A # or # B, where # is "
                " either ÷, ×, or !), others depend on context further away. Such"
                " rules are said to require extended context."),
            Annotation(
                (46, 0, 1, 'b'),
                " Rules requiring extended context used to be a concern for pair"
                " table-based implementations, and were listed in Section 7."
                " As more rules of this kind have been added, pair table-based"
                " implementations have become intractable, and this section has"
                " been removed."),
            Annotation(
                (46, 0, 1, 'c'),
                "However, extended context can lead to unexpected interactions"
                " between the rules, so they are called out in this annotated"
                " version with the annotation"
                " “Ramification: This rule requires extended context.” in"
                " order to facilitate the analysis of the algorithm."),
            Discussion(
                (49, 2, 'a'),
                "Indirect breaks can be represented with such a rule requiring"
                " extended context, but within the algorithm, they are"
                " instead expressed as × SP, SP ÷, B × A, which does not"
                " require extended context."),
            Discussion(
                (50, 1, 'a'),
                "Not all prohibited breaks involve a rule requiring extended"
                " context: a rule × A before the rule SP ÷ is a prohibited"
                " break before A. However, prohibited breaks with context"
                " before spaces require  extended context."),
        ],
        paragraphs=[
            ParagraphNumber(10),
            ParagraphNumber(23),
            ParagraphNumber(24),
            ParagraphNumber(25),
            ParagraphNumber(26),
            ParagraphNumber(27),
            ParagraphNumber(28),
            ParagraphNumber(28, 2),
            ParagraphNumber(36),
            ParagraphNumber(37, 2),
            ParagraphNumber(48, 1),
            ParagraphNumber(49, 2),
            ParagraphNumber(50, 1),
            ParagraphNumber(102),
            ParagraphNumber(112, 5),
            ParagraphNumber(347, 5),
            ParagraphNumber(364),
            ParagraphNumber(SECTION_6 + 3),
            ParagraphNumber(466),  # TODO(egg): .. 573.51
            ParagraphNumber(573, 52),
            ParagraphNumber(579, 5),
            ParagraphNumber(581),
            ParagraphNumber(582),
            ParagraphNumber(582, 1),
            ParagraphNumber(583, 1),
            ParagraphNumber(584, 1),
            ParagraphNumber(585),
            ParagraphNumber(587, 5, 7),
            ParagraphNumber(587, 20, 1),
        ]),
    # Creates LB23a.
    Issue(
        Version(9, 0, 0),
        ["143-A4", "146-C19"],
        [
            Reason(
                (SECTION_6 + 82, 5, 'a'),
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
        ["137-C9"],
        [
            Reason(
                (SECTION_6 + 71, 4, 'a'),
                "From CLDR.  “Hebrew makes extensive use of the / character to"
                " create gender-neutral verb forms, with the feminine suffix"
                " coming after the slash. […] It is quite rare in Hebrew to use a"
                " slash other than in this context.” See CLDR-6116."),
        ],
        paragraphs=[
            ParagraphNumber(SECTION_6 + 71, 3),
            ParagraphNumber(SECTION_6 + 71, 4),
        ]),
    Issue(Version(8, 0, 0),
          ["142-C3"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 72),
              ParagraphNumber(SECTION_6 + 72, 1, 1),
          ]),
    # Added LB30a.
    Issue(Version(6, 2, 0),
          ["131-C16", "132-C33"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 10),
              ParagraphNumber(SECTION_6 + 101, 11),
          ]),
    # Added LB21a.
    Issue(
        Version(6, 1, 0),
        ["125-A99"],  # Discussed in https://www.unicode.org/L2/L2011/11116-pre.htm#:~:text=Segmentation%20and%20Linebreak, approved in 129-A147.
        [
            Ramification(
                (401, 8, 'a'),
                "Since this is not a “treat as” rule, the WJ remains in the sequence"
                " for subsequent rules to see.  In the presence of rules that require"
                " extended context, this means that introducing a WJ can paradoxically"
                " create break opportunities."
                " For instance, LB21 and LB21a yield HL × HY × AL, but"
                " LB21a does not apply in HL × WJ × HY ÷ AL."),
            Reason(
                (SECTION_6 + 71, 2, 'a'),
                "“With <hebrew hyphen non-hebrew>, there is no break on either side of the hyphen.”"),
            Discussion(
                (SECTION_6 + 71, 2, 'b'),
                "The Hebrew ICU “and” list format with a non-Hebrew last element"
                " provides an example of such a sequence: ⁧John ו-Michael⁩; with"
                " a Hebrew last word, the letter ו is prefixed to the word:"
                " יוחנן ומיכאל."
                " See ICU-21016."),
            Ramification(
                (432, 2, 'c'),
                "This rule requires extended context."),
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
        ["121-C5"],
        [
            Ramification(
                (SECTION_6 + 33, 'a'),
                "This rule requires extended context."),
            Reason(
                (SECTION_6 + 33, 'b'),
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
          ["114-C30"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 3),
              ParagraphNumber(SECTION_6 + 101, 4),
              ParagraphNumber(SECTION_6 + 101, 5),
              ParagraphNumber(SECTION_6 + 101, 6),
          ]),
    Issue(Version(5, 1, 0),
          [],
          [
              Discussion(
                  (321, 'a'),
                  "Class QU (for ambiguous"
                  " quotation marks) is a Unicode innovation compared to the"
                  " ancestor standard JIS X 4051, necessitated by the variety"
                  " of quotation mark styles across languages; see The Unicode"
                  " Standard, Chapter 6."),
              Annotation(
                  (321, 'b'),
                  "Some rules pertaining to class QU in the algorithm may be"
                  " expressed as heuristics for its resolution into OP and CL,"
                  " as follows, where treating a quotation mark as both OP and"
                  " CL means disallowing breaks according to both"
                  " interpretations:"),
              Annotation(
                  (321, 'c'),
                  "Treat QU as OP in QU [^SP]. (LB19)"),
              Annotation(
                  (321, 'd'),
                  "Treat QU as CL in [^SP] QU. (LB19)"),

          ],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 51, 1),
          ]),
    # Split 12a from 12.
    Issue(Version(5, 1, 0),
          ["110-C17"],
          paragraphs=[
              ParagraphNumber(401, 10),
              ParagraphNumber(401, 11),
              ParagraphNumber(401, 13),
              ParagraphNumber(401, 15),
              ParagraphNumber(401, 16),
              ParagraphNumber(401, 17),
              ParagraphNumber(401, 18),
              ParagraphNumber(401, 19),
              ParagraphNumber(SECTION_6 + 42),
          ]),
    # Added LB30 (2); changes LB18 (3), but that one gets split into LB24 and LB25.
    # Changes to discusssions of tailoring are from (5).
    Issue(Version(5, 0, 0),
          ["105-C37"],
          [
              ToBeHonest(
                  (SECTION_6 + 11, 3, 'a'),
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
          ["100-M2"],
          paragraphs=[
              ParagraphNumber(396, 1),
              ParagraphNumber(396, 2),
              ParagraphNumber(396, 3),
              ParagraphNumber(396, 4),
          ]),
    # Excludes SP, BK, CR, LF, NL, ZW from X in X CM* ×.
    Issue(Version(4, 1, 0),
          ["102-C23"],
          paragraphs=[
              ParagraphNumber(400, 1),
              ParagraphNumber(401, 1),
              ParagraphNumber(401, 4),
          ]),
    # Splits 13 from 11b.
    Issue(Version(4, 1, 0),
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
          ["97-C25"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 1),
              ParagraphNumber(SECTION_6 + 101, 2),
          ]),
    # Splits 3b from 3a.
    Issue(Version(4, 0, 0),
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
          ["92-A64", "93-A96", "94-M4"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 98, 1),
              ParagraphNumber(SECTION_6 + 98, 2),
              ParagraphNumber(SECTION_6 + 98, 3),
          ]),
    # Adds 14a (F), adds 7c (J), moves 13 to 11b (K).
    Issue(Version(4, 0, 0),
          ["92-A64", "93-A96"],
          paragraphs=[
              ParagraphNumber(401, 2),
              ParagraphNumber(401, 3),
              ParagraphNumber(401, 4),
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
          ["94-C6"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 33, 3),
              ParagraphNumber(SECTION_6 + 33, 4),
              ParagraphNumber(SECTION_6 + 33, 5),
              ParagraphNumber(SECTION_6 + 35),
              ParagraphNumber(397),
              ParagraphNumber(398),
              ParagraphNumber(401, 1),
          ]),
    Issue(Version(3, 2, 0),
          ["81-M6", "85-M7"],
          paragraphs=[
              ParagraphNumber(61),
              ParagraphNumber(214, 1),
              ParagraphNumber(216),
              ParagraphNumber(248),
              ParagraphNumber(347),
              ParagraphNumber(596, 0, 5),
              ParagraphNumber(SECTION_6 + 58),
          ],
          l2_docs=["L2/00-258"]),
    # CGJ.
    Issue(Version(3, 2, 0),
          ["83-AI43", "84-M10", "85-M13"],
          paragraphs=[
              ParagraphNumber(61),
              ParagraphNumber(219, 1),
              ParagraphNumber(219, 2),
              ParagraphNumber(596, 0, 6),
          ],
          l2_docs=["L2/00-156"]),
    # UAX.
    Issue(Version(3, 0, 1),
          ["83-C6"],
          paragraphs=[
              ParagraphNumber(1),
              ParagraphNumber(3),
              ParagraphNumber(8, 1),
              ParagraphNumber(12),
              ParagraphNumber(12, 1),
              ParagraphNumber(13),
              ParagraphNumber(13, 1),
              ParagraphNumber(597, 1),
          ],
          l2_docs=["L2/00-118"]),
    # Math symbols.
    Issue(Version(3, 2, 0),
          ["83-M11"],
          paragraphs=[
              ParagraphNumber(324, 1),
              ParagraphNumber(324, 6),
              ParagraphNumber(596, 0, 6),
          ],
          l2_docs=["L2/00-119"]),
    # ⎶.
    Issue(Version(15, 0, 0),
          ["172-A98"],
          paragraphs=[
              ParagraphNumber(324, 6),
              ParagraphNumber(596, 60),
          ],
          l2_docs=["L2/22-124"],
          pri=["446@Fri Jun 3 10:22:13 CDT 2022"]),
    # Possible tailorings.
    Issue(Version(15, 1, 0),
          ["173-A6"],
          paragraphs=[
              ParagraphNumber(583),
              ParagraphNumber(587, 2),
              ParagraphNumber(587, 2, 1),
              ParagraphNumber(596, 68),
              ParagraphNumber(596, 69),
          ],
          l2_docs=["L2/22-244"],
          pri=["L2/22-243@Wed Sep 21 07:53:00 CDT 2022"]),
    # Third style.
    Issue(Version(15, 1, 0),
          ["173-A8"],
          paragraphs=[
              ParagraphNumber(94, 1),
              ParagraphNumber(595),
              ParagraphNumber(596, 66),
          ],
          l2_docs=["L2/22-244"],
          pri=["446@Sun Apr 10 20:12:11 CDT 2022"]),
    # Dictionary usage CP-1252 nonsense.
    Issue(Version(15, 1, 0),
          ["173-A13"],
          paragraphs=[
              ParagraphNumber(354),
              ParagraphNumber(355),
              ParagraphNumber(356),
              ParagraphNumber(357),
              ParagraphNumber(358),
              ParagraphNumber(359),
              ParagraphNumber(360),
              ParagraphNumber(361),
              ParagraphNumber(596, 67),
          ],
          l2_docs=["L2/22-244"],
          pri=["L2/22-243@Wed Sep 21 02:47:38 CDT 2022"]),
    # SCWG.
    Issue(Version(15, 1, 0),
          ["173-C29", "173-A128"],
          paragraphs=[
              ParagraphNumber(168, 1),
              ParagraphNumber(169, 1),
              ParagraphNumber(386, 2),
              ParagraphNumber(596, 65),
          ],
          l2_docs=["L2/22-229R", "L2/22-234R2"]),
    # Line breaking around quotation marks.
    Issue(Version(15, 1, 0),
          ["175-C23", "175-A71"],
          [
              Annotation(
                  (321, 'e'),
                  "Treat Initial Punctuation (gc=Pi) as OP at the beginning of"
                  " a line, at the beginning of a parenthetical or quotation,"
                  " or after spaces. (LB15a)"),
              Annotation(
                  (321, 'e'),
                  "Treat Final Punctuation (gc=Pf) as CL at the end of a line,"
                  " before a prohibited break (including at the end of a"
                  " parenthetical or quotation, as well as before trailing"
                  " punctuation), or before spaces. (LB15b)"),
              Annotation(
                (46, 0, 1, 'c', 1),
                " Implementations based on state machines may require special"
                " treatment for rules of the form A # B C or similar that"
                " require more than one character of lookahead beyond the"
                " break. These are annotated with “Ramification: This"
                " rule requires extended context after the break.”."),
              Ramification(
                  (412, 3, 'a'),
                  "Ramification: This rule requires extended context."),
              Ramification(
                  (412, 5, 'a'),
                  "Ramification: This rule requires extended context after the"
                  " break."),
              Reason(
                  (412, 5, 'b'),
                  "In some typographic traditions, such as German, initial"
                  " punctuation can be opening, and final punctuation can be"
                  " be closing, „like this“, or »like that«.  In others, such"
                  " as French and Vietnamese, opening and closing quotation"
                  " marks are separated from their contents by spaces, « like"
                  " this »."
                  "  These inner spaces must not be broken."
                  "  Crucially, these two sets do not intersect (no-one does"
                  " » this «), so an “isolated” quotation mark, is likely one"
                  " from the French tradition."),
              Annotation(
                  (412, 5, 'c'),
                  "Besides hard line breaks and spaces, the alternatives in"
                  " LB15a encompass characters that may be expected to occur"
                  " before a quotation, such as opening parentheses (« like"
                  " this »), or other quotation marks (for „« nested »"
                  " quotations”)."),
              Annotation(
                  (412, 5, 'c'),
                  "ZW is also included, for two reasons. One is technical: some"
                  " major state-machine based implementations are incapable of"
                  " considering context across break opportunities, so that the"
                  " position following ZW is indistinguishable from sot for"
                  " them. The other is semantic: ZW is an overriding control"
                  " character that creates a break opportunity; it is similar"
                  " to a hard line break, and is a strong signal that the"
                  " following character may begin a line, which suggests it is"
                  " not a closing quotation mark."),
              Annotation(
                  (412, 5, 'e'),
                  "The alternatives in LB15b comprise the closing counterparts,"
                  " as well as classes encompassing terminal punctuation, for"
                  " the case of quotations before « commas », or before « full"
                  " stops »."),
            Ramification(
                  (412, 5, 'f'),
                  "When text starting with a full stop is quoted within German"
                  " text and the German quotation marks are not resolved, the"
                  " algorithm fails to allow breaks that should be"
                  " permitted, before the „ quotation mark in Die Patrone"
                  " „.30 Carbine“."),
          ],
          paragraphs=[
              ParagraphNumber(411),
              ParagraphNumber(412),
              ParagraphNumber(412, 1),
              ParagraphNumber(412, 2),
              ParagraphNumber(412, 3),
              ParagraphNumber(412, 4),
              ParagraphNumber(412, 5),
              ParagraphNumber(596, 64),
          ],
          l2_docs=["L2/23-063"]),
    # Orthographic syllables.
    Issue(Version(15, 1, 0),
          ["162-A43", "175-C27", "175-A77", "175-A79"],
          [
            Ramification(
                  (462, 0, 5, 'a'),
                  "Ramification: This rule requires extended context after the"
                  " break."),
          ],
          paragraphs=[
              ParagraphNumber(79, 1, 2),
              ParagraphNumber(79, 3, 1),
              ParagraphNumber(79, 3, 2),
              ParagraphNumber(81, 1),
              ParagraphNumber(81, 2),
              ParagraphNumber(87),
              ParagraphNumber(90, 1),
              ParagraphNumber(94, 1, 1),
              ParagraphNumber(94, 2),
              ParagraphNumber(112, 7),
              ParagraphNumber(112, 8),
              ParagraphNumber(112, 9),
              ParagraphNumber(112, 10),
              ParagraphNumber(112, 11),
              ParagraphNumber(112, 12),
              ParagraphNumber(112, 13),
              ParagraphNumber(112, 14),
              ParagraphNumber(112, 15),
              ParagraphNumber(112, 16),
              ParagraphNumber(112, 17),
              ParagraphNumber(112, 18),
              ParagraphNumber(112, 19),
              ParagraphNumber(112, 20),
              ParagraphNumber(112, 21),
              ParagraphNumber(112, 22),
              ParagraphNumber(112, 23),
              ParagraphNumber(116, 9),
              ParagraphNumber(116, 10),
              ParagraphNumber(116, 11),
              ParagraphNumber(116, 12),
              ParagraphNumber(116, 13),
              ParagraphNumber(116, 14),
              ParagraphNumber(116, 15),
              ParagraphNumber(116, 16),
              ParagraphNumber(116, 17),
              ParagraphNumber(116, 18),
              ParagraphNumber(116, 19),
              ParagraphNumber(116, 20),
              ParagraphNumber(116, 21),
              ParagraphNumber(153, 56),
              ParagraphNumber(153, 57),
              ParagraphNumber(153, 58),
              ParagraphNumber(153, 59),
              ParagraphNumber(153, 60),
              ParagraphNumber(153, 61),
              ParagraphNumber(153, 62),
              ParagraphNumber(153, 63),
              ParagraphNumber(153, 64),
              ParagraphNumber(196),
              ParagraphNumber(288),
              ParagraphNumber(288, 0, 1),
              ParagraphNumber(288, 0, 2),
              ParagraphNumber(288, 0, 3),
              ParagraphNumber(345, 0, 1),
              ParagraphNumber(345, 0, 2),
              ParagraphNumber(345, 0, 3),
              ParagraphNumber(345, 0, 4),
              ParagraphNumber(345, 0, 5),
              ParagraphNumber(345, 0, 6),
              ParagraphNumber(345, 0, 7),
              ParagraphNumber(345, 0, 8),
              ParagraphNumber(345, 0, 9),
              ParagraphNumber(345, 0, 10),
              ParagraphNumber(345, 0, 11),
              ParagraphNumber(462, 0, 1),
              ParagraphNumber(462, 0, 2),
              ParagraphNumber(462, 0, 3),
              ParagraphNumber(462, 0, 4),
              ParagraphNumber(462, 0, 5),
              ParagraphNumber(587, 10, 1),
              ParagraphNumber(587, 11),
              ParagraphNumber(595),
              ParagraphNumber(596, 63),
          ],
          l2_docs=["L2/23-072", "L2/22-080R2", "L2/22-086"],
          pri=["335@Thu May 4 18:29:06 CDT 2017",
               "406@Tue Nov 5 18:25:35 CST 2019"]),
    # Update UAX #14 to point to the CLDR tailoring, for version 12.0.
    Issue(Version(12, 0, 0),
          ["173-A128"],
          paragraphs=[
              ParagraphNumber(96, 1, 2, 3, 1),
              ParagraphNumber(579, 2, 1, 2),
              ParagraphNumber(596, 38),
          ],
          l2_docs=[]),
    # Typos from PRI.
    Issue(Version(12, 0, 0),
          ["173-A128"],
          paragraphs=[
              ParagraphNumber(324, 11),
              ParagraphNumber(579, 3),
              ParagraphNumber(586),
              ParagraphNumber(596, 37),
          ],
          l2_docs=[],
          pri=["383@Sun Jan 6 23:07:34 CST 2019"]),
    # Mongolian NNBSP.
    Issue(Version(12, 0, 0),
          ["155-A31"],
          paragraphs=[
              ParagraphNumber(219),
              ParagraphNumber(219, 0, 1),
              ParagraphNumber(219, 0, 3),
              ParagraphNumber(596, 36),
          ],
          l2_docs=[]),
    # Tab-delimited.
    Issue(Version(11, 0, 0),
          ["154-A128"],
          paragraphs=[
              ParagraphNumber(102, 2),
              ParagraphNumber(596, 31),
          ],
          l2_docs=["L2/18-009@Fri Nov 10 17:16:01 CST 2017"]),
    # Character names.
    Issue(Version(11, 0, 0),
          ["155-A26"],
          paragraphs=[
              ParagraphNumber(54),
              ParagraphNumber(153, 3),
              ParagraphNumber(153, 4),
              ParagraphNumber(153, 12, 5),
              ParagraphNumber(153, 12, 12),
              ParagraphNumber(153, 49, 2),
              ParagraphNumber(171),
              ParagraphNumber(174),
              ParagraphNumber(175),
              ParagraphNumber(222),
              ParagraphNumber(315),
              ParagraphNumber(318, 1),
              ParagraphNumber(361, 0, 11),
              ParagraphNumber(361, 16, 1),
              ParagraphNumber(596, 30),
          ],
          pri=["376@Sat Apr 14 08:42:52 CDT 2018"]),
    # Emoji rules from CLDR, and the UTR becomes a UTS.
    Issue(Version(10, 0, 0),
          ["150-A58", "150-C22"],
          paragraphs=[
              ParagraphNumber(205, 3),
              ParagraphNumber(205, 10),
              ParagraphNumber(350, 4),
              ParagraphNumber(394, 1, 4),
              ParagraphNumber(394, 1, 5),
              ParagraphNumber(579, 2, 2),
          ],
          l2_docs=["L2/16-315R"]),
    # RI.
    Issue(Version(10, 0, 0),
          ["150-A28"],
          paragraphs=[
              ParagraphNumber(324, 10),
          ]),
    # lb=PR defaults in the Currency Symbols block, undocumented for ages.
    Issue(Version(16, 0, 0),
          ["133-C26"],
          paragraphs=[
              ParagraphNumber(312),
              ParagraphNumber(596, 77),
          ]),
    # Correct the description of the behaviour of line breaking classes PO and
    # PR when separated from numbers by spaces, so that the description matches
    # the rules.
    Issue(Version(16, 0, 0),
          ["179-A97"],
          pri=["446@Tue Apr 5 07:14:53 CDT 2022"],
          paragraphs=[
              ParagraphNumber(293),
              ParagraphNumber(310),
              ParagraphNumber(595),
              ParagraphNumber(596, 88),
          ]),
    # Line breaking around quotation marks, follow-up documentation.
    Issue(Version(16, 0, 0),
          ["175-C23", "175-A71"],
          paragraphs=[
              ParagraphNumber(71),
              ParagraphNumber(320),
              ParagraphNumber(596, 83),
          ],
          l2_docs=["L2/23-063"]),
    # Changed LB19, added LB19a.
    # TODO(egg): destination in L2 doc is h.fxg3io80cki1.
    Issue(Version(16, 0, 0),
          ["179-C28", "179-A102"],
          [
            Annotation(
                (321, 'c', 1),
                "Except for \p{Pf} in East Asian context. (LB19a)"),
            Annotation(
                (321, 'd', 1),
                "Except for \p{Pi} in East Asian context. (LB19a)"),
            Reason(
                (424, 0, 5, 'a'),
                "In some typographic traditions, such as German, initial"
                " punctuation can be opening, and final punctuation can be"
                " be closing, „like this“.  However, this is not the case in"
                " East Asian typographic traditions where (in particular in"
                " Simplified Chinese) the lb=QU “” and ‘’ are used."
                "  At the same time, these East Asian traditions benefit from"
                " classifying the quotation marks opening and closing, as,"
                " contrary to the Western case, they do not separate the"
                " quotation marks from surrounding words by spaces."
                "  Thus, if the context is East Asian, we should treat initial"
                " punctuation as opening and final punctuation as closing."
                "  Otherwise, we need to be cautious and disallow breaks on"
                " either side."),
            Annotation(
                (424, 0, 5, 'b'),
                "  Having East Asian characters on one side is not enough to"
                " establish an East Asian context, as, for instance, a Chinese"
                " word could be quoted inside of German text.  For instance,"
                " the ‚‘ quotation marks must not be considered to be in East"
                " Asian context in the following, as this would incorrectly"
                " allow breaks inside the quotation marks:"
                " Anmerkung: „White“ bzw. ‚白人‘ – in der Amtlichen Statistik"),
            Ramification(
                (424, 0, 5, 'c'),
                "When non-East Asian text is quoted within Simplified Chinese"
                " text and the quotation marks U+2018 and U+2019 are not"
                " resolved, the algorithm fails to allow breaks that should be"
                " permitted, as outside the “” quotation marks in 2000年获得了"
                "《IGN》的“Best Game Boy Strategy”奖。 In that example, breaks"
                " are correctly permitted outside 《》 because these are"
                " unambiguous, lb=OP and lb=CL."),
          ],
          paragraphs=[
              ParagraphNumber(320),
              ParagraphNumber(370, 0, 1),  # $EastAsian
              ParagraphNumber(422),
              ParagraphNumber(423),
              ParagraphNumber(424),
              ParagraphNumber(424, 0, 1),
              ParagraphNumber(424, 0, 2),
              ParagraphNumber(424, 0, 3),
              ParagraphNumber(424, 0, 4),
              ParagraphNumber(424, 0, 5),
              ParagraphNumber(462, 7),  # $EastAsian
              ParagraphNumber(462, 8),  # $EastAsian
              ParagraphNumber(462, 9, 1),  # $EastAsian
              ParagraphNumber(596, 78),
              ParagraphNumber(596, 83),
          ]),
    # Change rule LB21a from HL (HY | BA) × to HL (HY | BA) × [^HL]
    Issue(Version(16, 0, 0),
          ["179-C25", "179-A98"],
          [
            Ramification(
                (432, 2, 'd'),
                "A break is allowed after the hyphen in Hebrew + Hyphen +"
                " Hebrew."),
          ],
          pri=["335@Sat Apr 29 23:16:48 CDT 2017"],
          paragraphs=[
              ParagraphNumber(248, 8),
              ParagraphNumber(432, 1),
              ParagraphNumber(432, 2),
              ParagraphNumber(595),
              ParagraphNumber(596, 81),
              ParagraphNumber(596, 84),
          ]),
    # LB21b, follow-up documentation.
    Issue(
        Version(16, 0, 0),
        ["137-C9"], # TODO(egg): CLDR ticket CLDR-6116.
        paragraphs=[
              ParagraphNumber(248, 8),
              ParagraphNumber(596, 84),
        ]),
    # LB=CP for closing phonetic brackets.
    Issue(Version(16, 0, 0),
          ["172-A100"],  # TODO(egg): Needs consensus at UTC #180.
          pri=["446@Fri Jun 3 19:49:05 CDT 2022"],
          paragraphs=[
              ParagraphNumber(202, 4),
              ParagraphNumber(202, 7),
              ParagraphNumber(202, 8),
              ParagraphNumber(202, 9),
              ParagraphNumber(202, 10),
              ParagraphNumber(595),
              ParagraphNumber(596, 89),
          ]),
    # lb=GL half marks.
    Issue(Version(16, 0, 0),
          ["179-C29", "179-A105"],
          pri=["335@Sat Apr 29 22:48:11 CDT 2017"],
          paragraphs=[
              ParagraphNumber(225, 3),
              ParagraphNumber(225, 4),
              ParagraphNumber(225, 5),
              ParagraphNumber(225, 6),
              ParagraphNumber(225, 7),
              ParagraphNumber(225, 8),
              ParagraphNumber(225, 9),
              ParagraphNumber(225, 10),
              ParagraphNumber(225, 11),
              ParagraphNumber(225, 12),
              ParagraphNumber(225, 13),
              ParagraphNumber(595),
              ParagraphNumber(596, 85),
          ]),
    # LB change of presentation forms for vertical whatever.
    Issue(Version(16, 0, 0),
          ["179-C30", "179-A107"],
          paragraphs=[
              ParagraphNumber(185, -1, 1),
              ParagraphNumber(263, 1, 1),
              ParagraphNumber(263, 1, 2),
              ParagraphNumber(263, 1, 3),
              ParagraphNumber(279, 3),
              ParagraphNumber(279, 4),
              ParagraphNumber(596, 86),
          ]),
    # LB20a word-initial hyphen.
    # TODO(egg): CLDR and ICU tickets, an annotation.
    Issue(Version(16, 0, 0),
          ["179-C32", "179-A111"],
          paragraphs=[
              ParagraphNumber(424, 5),
              ParagraphNumber(424, 6),
              ParagraphNumber(424, 7),
              ParagraphNumber(596, 80),
          ]),
    # LB25, LB13, LB15c, LB15d, numbers.
    Issue(Version(16, 0, 0),
          ["179-C35", "179-A116"],
          # TODO(egg): Many old L2 references to add. Also ICU tickets. + a PRI.
          paragraphs=[
              ParagraphNumber(404),
              ParagraphNumber(406, 1),
              ParagraphNumber(412, 6),
              ParagraphNumber(412, 7),
              ParagraphNumber(412, 8),
              ParagraphNumber(412, 9),
              ParagraphNumber(445),
              ParagraphNumber(446),
              ParagraphNumber(447),
              ParagraphNumber(448),
              ParagraphNumber(448, 1),
              ParagraphNumber(448, 1, 0, 1),
              ParagraphNumber(448, 1, 1),
              ParagraphNumber(448, 1, 1, 1),
              ParagraphNumber(448, 1, 2),
              ParagraphNumber(448, 1, 3),
              ParagraphNumber(448, 1, 4),
              ParagraphNumber(448, 1, 4, 1),
              ParagraphNumber(448, 1, 6),
              ParagraphNumber(448, 1, 6, 1),
              ParagraphNumber(448, 4),
              ParagraphNumber(454),
              ParagraphNumber(459),
              ParagraphNumber(587, 3),
              ParagraphNumber(587, 4),
              ParagraphNumber(587, 5),
              ParagraphNumber(587, 5, 1),
              ParagraphNumber(587, 5, 2),
              ParagraphNumber(587, 5, 3),
              ParagraphNumber(587, 5, 4),
              ParagraphNumber(587, 5, 5),
              ParagraphNumber(587, 5, 6),
              ParagraphNumber(587, 5, 7),
              ParagraphNumber(587, 5, 8),
              ParagraphNumber(587, 6),
              ParagraphNumber(587, 6, 1),
              ParagraphNumber(587, 7),
              ParagraphNumber(587, 8),
              ParagraphNumber(587, 9),
              ParagraphNumber(587, 10),
              ParagraphNumber(587, 11, 23),
              ParagraphNumber(596, 79),
          ]),
    # Much ado about ◌
    Issue(Version(16, 0, 0),
          ["178-A20"],
          paragraphs=[
              ParagraphNumber(462, 0, 2),
              ParagraphNumber(462, 0, 3),
              ParagraphNumber(462, 0, 4),
              ParagraphNumber(462, 0, 5),
              ParagraphNumber(462, 0, 6),
              ParagraphNumber(596, 76),
          ]),
    # LB9 unclear that the CM|ZWJ vanishes
    Issue(Version(16, 0, 0),
          [],  # No action.
          l2_docs=["L2/24-009R"], # TODO(egg): Section 6.2.
          pri=["L2/24-008@Tue Nov 07 14:09:48 CST 2023"], # TODO(egg): #ID20231107140948
          paragraphs=[
              ParagraphNumber(401, 1),
              ParagraphNumber(596, 75),
          ]),
    # LB=ID plane 1 range
    Issue(Version(10, 0, 0),
          ["147-C25"],
          paragraphs=[
              ParagraphNumber(248, 0, 12),
              ParagraphNumber(248, 0, 13),
          ]),
    # LB=ID holes, one from 13.0 missed in documentation.
    Issue(Version(16, 0, 0),
          ["177-A115", "177-C47", "162-A67"],
          l2_docs=["L2/23-234"], # TODO(egg): 5.3
          paragraphs=[
              ParagraphNumber(248, 0, 12),
              ParagraphNumber(248, 0, 13),
              ParagraphNumber(248, 0, 14),
              ParagraphNumber(248, 0, 15),
              ParagraphNumber(596, 73),
          ]),
    # LB=AS digits.
    Issue(Version(16, 0, 0),
          ["177-C46", "177-A113"],
          l2_docs=["L2/23-234"], # TODO(egg): 5.1
          paragraphs=[
              ParagraphNumber(116, 14),
              ParagraphNumber(116, 14, 1),
              ParagraphNumber(116, 15, 1),
              ParagraphNumber(116, 16, 1),
              ParagraphNumber(116, 19, 1),
              ParagraphNumber(596, 72),
          ]),
    # Dictionary usage to the core spec.
    Issue(Version(16, 0, 0),
          ["173-A14"],
          l2_docs=["L2/22-244"], # TODO(egg): Seg7
          pri=["L2/22-243@Wed Sep 21 02:47:38 CDT 2022"],
          paragraphs=[
              ParagraphNumber(352),
              ParagraphNumber(353),
              ParagraphNumber(353, 1),
              ParagraphNumber(354),
              ParagraphNumber(355),
              ParagraphNumber(356),
              ParagraphNumber(357),
              ParagraphNumber(358),
              ParagraphNumber(359),
              ParagraphNumber(360),
              ParagraphNumber(361),
              ParagraphNumber(361, 0, 1),
              ParagraphNumber(596, 74),
          ]),
    # Drop the X?[ABP] stuff.
    Issue(Version(16, 0, 0),
          ["179-A110", "162-A45"],
          l2_docs=["L2/24-064"], # TODO(egg): 5.10
          pri=["406@Wed Dec 4 15:18:53 CST 2019"],
          paragraphs=[
              ParagraphNumber(104),
              ParagraphNumber(104, 1),
              ParagraphNumber(105),
              ParagraphNumber(106),
              ParagraphNumber(107),
              ParagraphNumber(108),
              ParagraphNumber(109),
              ParagraphNumber(110),
              ParagraphNumber(110, 1),
              ParagraphNumber(111, 0, 1),
              ParagraphNumber(112, 7),
              ParagraphNumber(112, 7, 1),
              ParagraphNumber(113),
              ParagraphNumber(113, 1),
              ParagraphNumber(116, 9),
              ParagraphNumber(116, 9, 1),
              ParagraphNumber(116, 13),
              ParagraphNumber(116, 13, 1),
              ParagraphNumber(117),
              ParagraphNumber(117, 1),
              ParagraphNumber(154),
              ParagraphNumber(154, 0, 1),
              ParagraphNumber(163),
              ParagraphNumber(163, 1),
              ParagraphNumber(167),
              ParagraphNumber(167, 1),
              ParagraphNumber(179),
              ParagraphNumber(179, 1),
              ParagraphNumber(182, 1, 1),
              ParagraphNumber(183),
              ParagraphNumber(183, 1),
              ParagraphNumber(193),
              ParagraphNumber(193, 1),
              ParagraphNumber(202, 3),
              ParagraphNumber(202, 3, 1),
              ParagraphNumber(203),
              ParagraphNumber(203, 1),
              ParagraphNumber(205, 2),
              ParagraphNumber(205, 2, 1),
              ParagraphNumber(205, 9),
              ParagraphNumber(205, 9, 1),
              ParagraphNumber(206),
              ParagraphNumber(206, 1),
              ParagraphNumber(213),
              ParagraphNumber(215, 1),
              ParagraphNumber(226, 1),
              ParagraphNumber(226, 1, 1),
              ParagraphNumber(226, 4),
              ParagraphNumber(226, 4, 1),
              ParagraphNumber(227),
              ParagraphNumber(227, 1),
              ParagraphNumber(231),
              ParagraphNumber(231, 2),
              ParagraphNumber(248, 6),
              ParagraphNumber(248, 6, 1),
              ParagraphNumber(249),
              ParagraphNumber(249, 1),
              ParagraphNumber(256),
              ParagraphNumber(257, 1),
              ParagraphNumber(263, 4),
              ParagraphNumber(263, 4, 1),
              ParagraphNumber(263, 7),
              ParagraphNumber(263, 7, 1),
              ParagraphNumber(263, 9),
              ParagraphNumber(263, 9, 1),
              ParagraphNumber(264),
              ParagraphNumber(264, 1),
              ParagraphNumber(266, 1),
              ParagraphNumber(266, 1, 1),
              ParagraphNumber(267),
              ParagraphNumber(267, 1),
              ParagraphNumber(286),
              ParagraphNumber(286, 1),
              ParagraphNumber(289),
              ParagraphNumber(289, 1),
              ParagraphNumber(292),
              ParagraphNumber(292, 1),
              ParagraphNumber(309),
              ParagraphNumber(309, 1),
              ParagraphNumber(319),
              ParagraphNumber(319, 1),
              ParagraphNumber(324, 7),
              ParagraphNumber(324, 7, 1),
              ParagraphNumber(325),
              ParagraphNumber(325, 1),
              ParagraphNumber(333),
              ParagraphNumber(333, 1),
              ParagraphNumber(336),
              ParagraphNumber(336, 1),
              ParagraphNumber(341),
              ParagraphNumber(341, 1),
              ParagraphNumber(345, 0, 1),
              ParagraphNumber(345, 0, 1, 1),
              ParagraphNumber(345, 0, 5),
              ParagraphNumber(345, 0, 5, 1),
              ParagraphNumber(345, 1),
              ParagraphNumber(345, 1, 1),
              ParagraphNumber(346),
              ParagraphNumber(346, 0, 1),
              ParagraphNumber(348),
              ParagraphNumber(348, 1),
              ParagraphNumber(350, 1),
              ParagraphNumber(350, 1, 1),
              ParagraphNumber(596, 82),
          ]),
    # UTN #54 instead of the renumbering table.
    Issue(Version(16, 0, 0),
          ["175-A67"],
          paragraphs=[
              ParagraphNumber(30, 3),
              ParagraphNumber(37, 6),
              ParagraphNumber(587, 41),
              ParagraphNumber(587, 42),
              ParagraphNumber(587, 43),
              ParagraphNumber(587, 44),
              ParagraphNumber(587, 45),
              ParagraphNumber(587, 46),
              ParagraphNumber(587, 47),
              ParagraphNumber(587, 48),
              ParagraphNumber(587, 49),
              ParagraphNumber(587, 50),
              ParagraphNumber(587, 51),
              ParagraphNumber(587, 52),
              ParagraphNumber(587, 52, 1),
              ParagraphNumber(587, 53),
              ParagraphNumber(587, 54),
              ParagraphNumber(587, 55),
              ParagraphNumber(587, 56),
              ParagraphNumber(587, 57),
              ParagraphNumber(587, 58),
              ParagraphNumber(587, 59),
              ParagraphNumber(587, 60),
              ParagraphNumber(587, 61),
              ParagraphNumber(587, 61, 1),
              ParagraphNumber(587, 61, 2),
              ParagraphNumber(587, 62),
              ParagraphNumber(587, 63),
              ParagraphNumber(587, 64),
              ParagraphNumber(587, 65),
              ParagraphNumber(587, 66),
              ParagraphNumber(587, 67),
              ParagraphNumber(587, 67, 1),
              ParagraphNumber(587, 67, 2),
              ParagraphNumber(587, 68),
              ParagraphNumber(587, 69),
              ParagraphNumber(587, 69, 1),
              ParagraphNumber(587, 70),
              ParagraphNumber(587, 71),
              ParagraphNumber(587, 72),
              ParagraphNumber(587, 73),
              ParagraphNumber(587, 74),
              ParagraphNumber(587, 75),
              ParagraphNumber(587, 75, 1),
              ParagraphNumber(587, 76),
              ParagraphNumber(587, 77),
              ParagraphNumber(587, 77, 1),
              ParagraphNumber(587, 77, 2),
              ParagraphNumber(587, 78),
              ParagraphNumber(587, 79),
              ParagraphNumber(587, 80),
              ParagraphNumber(587, 81),
              ParagraphNumber(596, 87),
          ]),
)
