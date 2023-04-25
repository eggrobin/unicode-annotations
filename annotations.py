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
        [],  # TODO(egg): if this annotation thing ever makes it to the UTC, put an AI here.
        [
            Discussion(
                (11, 'a'),
                "This Annotated Line Breaking Algorithm contains the entire"
                " text of Unicode Standard Annex #14, Unicode Line"
                " Breaking Algorithm, plus certain annotations. The annotations"
                " give a more in-depth analysis of the algorithm. They describe"
                " the reason for each nonobvious rule, and point out"
                " interesting ramifications of the rules and interactions among"
                " the rules (interesting to Unicode maintainers, that is). (The"
                " text you are reading now is an annotation.)"),
            Annotation(
                (11, 'b'),
                "The structure of this document is heavily inspired by that of"
                " the Annotated Ada Reference Manual.  For a description of the"
                " various kinds of annotations, see paragraphs 1(2.dd) through"
                " 1(2.ll) in that document."),
            Annotation(
                (11, 'c'),
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
                " inserted between paragraphs 3 and 3.1 is numbered 3.0.1."
                " Inserted text is indicated by highlighting, and deleted text"
                " is indicated by strikethroughs. Colour is used to indicate"
                " the version of the change."
                " Deleted paragraphs are indicated by the text “This paragraph"
                " was deleted.”, or by a description of the new location of"
                " any text retained. Compare the Annotated Ada 2012 Reference"
                " Manual, Introduction (77.5)."),
            Annotation(
                (11, 'd'),
                "Annotations are numbered similarly, except that the first"
                " insertion number is alphabetic rather than numeric."),
            Discussion(
                (11, 'e'),
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
                (401, 7, 'a'),
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
            ParagraphNumber(596, 0, 0, 0, 1, 12),
        ]),
    Issue(
        Version(14, 0, 0),
        ["167-A94", "168-C7", "168-C8"],
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
        ]
        ),
    Issue(Version(14, 0, 0),
          ["163-A70"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 98, 12),
          ]),
    Issue(Version(13, 0, 0),
          ["160-A75", "161-A47", "162-A42"],
          paragraphs=[
              ParagraphNumber(SECTION_6 + 101, 7),
              ParagraphNumber(SECTION_6 + 101, 8),
              ParagraphNumber(SECTION_6 + 101, 9, 1),
              ParagraphNumber(SECTION_6 + 101, 9, 2),
              ParagraphNumber(SECTION_6 + 101, 9, 3),
          ]),
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
                " slash other than in this context.” See CLDR-6616."),
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
                (401, 11, 'a'),
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
                  (SECTION_6 + 51, 1, 'a'),
                  "When a quote is known to be opening or closing, OP and CL"
                  " should respectively be used.  Class QU (for ambiguous"
                  " quotation marks) is a Unicode innovation compared to the"
                  " ancestor standard JIS X 4051, necessitated by the variety"
                  " of quotation mark styles across languages; see The Unicode"
                  " Standard, Chapter 6."),
              Ramification(
                  (SECTION_6 + 51, 1, 'b'),
                  "The rules pertaining to class QU in the algorithm may be"
                  " expressed as heuristics for its resolution into OP and CL,"
                  " as follows, where treating a quotation mark as both OP and"
                  " CL means disallowing breaks according to both"
                  " interpretations:"),
              Annotation(
                  (SECTION_6 + 51, 1, 'c'),
                  "Treat QU as OP in QU SP+ OP. (LB15)"),
              Annotation(
                  (SECTION_6 + 51, 1, 'd'),
                  "Treat QU as OP in QU [^SP]. (LB19)"),
              Annotation(
                  (SECTION_6 + 51, 1, 'e'),
                  "Treat QU as CL in [^SP] QU. (LB19)"),
              Discussion(
                  (SECTION_6 + 51, 1, 'f'),
                  "While the latter two heuristics are self-explanatory, the"
                  " first one (LB15) is weird.  It applies to cases such"
                  " as the opening quotation mark in « [Le livre] tuera"
                  " [l’édifice] », but not to the closing quotation mark."
                  " It can misfire, as in “All Gaul is divided into three"
                  " parts” ×(Caes. BGall. 1.1.1)."),
              Annotation(
                  (SECTION_6 + 51, 1, 'g'),
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
              ParagraphNumber(596, 66),
              ParagraphNumber(596, 67),
          ],
          l2_docs=["L2/22-244"],
          pri=["L2/22-243@Wed Sep 21 07:53:00 CDT 2022"]),
    # Third style.
    Issue(Version(15, 1, 0),
          ["173-A8"],
          paragraphs=[
              ParagraphNumber(94, 1),
              ParagraphNumber(595),
              ParagraphNumber(596, 64),
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
              ParagraphNumber(596, 65),
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
              ParagraphNumber(596, 63),
          ],
          l2_docs=["L2/22-229R", "L2/22-234R2"]),
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
)
