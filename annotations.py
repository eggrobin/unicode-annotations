from typing import Tuple
from typing import Sequence
from typing import Optional


class Issue:
  def __init__(
      self,
      version: Tuple[int, int, int],
      target_rules: Sequence[str],
      l2_refs: Sequence[str],
      l2_docs: Sequence[str] = [],
      affected_rules: Sequence[str] = [],
      reason: Optional[str] = None) -> None:
    self.version = version
    self.target_rules = target_rules
    self.l2_refs = l2_refs
    self.l2_docs = l2_docs
    self.affected_rules = affected_rules
    self.reason = reason


ISSUES = (
    Issue((14, 0, 0),
          ["30b"],
          ["168-C8"]),
    Issue((14, 0, 0),
          ["27"],
          ["163-A70"]),
    Issue((13, 0, 0),
          ["30"],
          ["160-A75", "161-A47", "162-A42"]),
    Issue((13, 0, 0),
          ["22"],
          ["142-A23", "160-A56"]),
    Issue((11, 0, 0),
          ["8a"],
          ["149-A53"],
          l2_docs=["L2/17-074"]),
    # Creates 8a.  The original proposal targets LB23 and LB24, but the relevant
    # parts become LB23a per the next issue.
    Issue((9, 0, 0),
          ["8a", "9", "10", "22", "23a", "30a", "30b"],
          ["146-A46", "147-C26"]),
    # Creates LB23a.
    Issue((9, 0, 0),
          ["23", "23a", "24"],
          ["143-A4", "146-C19"]),
    # Creates LB21b.
    Issue((8, 0, 0),
          ["21b"],
          ["137-C9"]),
    Issue((8, 0, 0),
          ["22"],
          ["142-C3"]),
    # Added LB30a.
    Issue((6, 2, 0),
          ["30a"],
          ["131-C16", "132-C33"]),
    # Added LB21a.
    Issue((6, 1, 0),
          ["21a"],
          ["125-A99"],  # Discussed in https://www.unicode.org/L2/L2011/11116-pre.htm#:~:text=Segmentation%20and%20Linebreak, approved in 129-A147.
          l2_docs=["L2/11-141R"],
          affected_rules=["22", "23", "24", "28", "29", "30"]),
    Issue((6, 1, 0),
          ["1"],
          ["129-C2"]),  # Rationale is in the review note https://www.unicode.org/reports/tr14/tr14-27d2.html#NS.
    Issue((6, 0, 0),
          ["8"],
          ["121-C5"]),
    # Re-added LB30.
    Issue((5, 2, 0),
          ["30"],
          ["114-A86, 120-M1"],
          affected_rules=["13", "16", "25"]),
    # Removed LB30.
    Issue((5, 1, 0),
          ["x30"],
          ["114-C30"]),
    # Split 12a from 12.
    Issue((5, 1, 0),
          ["12a"],
          ["110-C17"],
          affected_rules=["12"]),
    # Added LB30 (2); changes LB18 (3), but that one gets split into LB24 and LB25.
    Issue((5, 0, 0),
          ["30", "24", "25"],
          ["105-C37"]),
    # Splits 18 into 24 and 25.
    Issue((5, 0, 0),
          ["24", "25"],
          ["105-C6"]),
    # Splits 6 into 18b and 18c (4), removes 18b (5).
    Issue((4, 1, 0),
          ["18b", "18c", "x18b"],
          ["100-C40"]),
    # Removes 7a.
    Issue((4, 1, 0),
          ["x7a"],
          ["100-M2"]),
    Issue((4, 1, 0),
          ["7b"],
          ["102-C23"]),
    # Splits 13 from 11b.
    Issue((4, 1, 0),
          ["11b", "13"],
          ["94-M3"]),
    # Creates 19b.
    Issue((4, 0, 1),
          ["19b"],
          ["97-C25"]),
    # Splits 3b from 3a.
    Issue((4, 0, 0),
          ["3a", "3b"],
          ["94-M2"],
          affected_rules=["3c"]),
    # Moves 15b to 18b (A).  Separate from the one below because the motion is 
    # only about 18b.
    Issue((4, 0, 0),
          ["18b"],
          ["92-A64", "93-A96", "94-M4"]),
    # Adds 14a (F), adds 7c (J), moves 13 to 11b (K).
    Issue((4, 0, 0),
          ["14a", "7c", "11b"],
          ["92-A64", "93-A96"]),
    # Splits 7b from 6.
    Issue((4, 0, 0),
          ["6", "7b"],
          ["94-C6"]),
    Issue((3, 2, 0),
          ["13"],
          ["81-M6", "85-M7"],
          l2_docs=["L2/00-258"])
)