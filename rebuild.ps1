foreach (
    $i in @(6, 7, 10, 12, 14, 15, 17, 19, 22, 24, 26, 28,
            30, 32, 33, 35, 37, 39, 41, 43, 45, 47, 49,
            51, 53)) {
  Invoke-WebRequest "https://www.unicode.org/reports/tr14/tr14-$i.html" -OutFile "tr14-$i.html"
}
python .\lb_rule_extractor.py --out=paragraphs.py
python .\lb_differ.py