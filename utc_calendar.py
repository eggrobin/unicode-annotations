from datetime import date, timedelta
import sys

OFFSET = 44
UTC = [
    # https://www.unicode.org/L2/meetings/utc-meetings-early.html#UWG
    # https://www.unicode.org/L2/meetings/utc-meetings-early.html#distinct
    (date(1991, 2, 1), 2),  # UTC #44
    (date(1991, 2, 28), 2),  # UTC #45
    (date(1991, 3, 26), 2),  # UTC #46
    (date(1991, 6, 6), 2),  # UTC #47
    (date(1991, 9, 12), 2),  # UTC #48
    (date(1991, 10, 31), 2),  # UTC #49
    (date(1992, 1, 14), 1),  # UTC #50
    (date(1992, 3, 6), 1),  # UTC #51
    (date(1992, 5, 8), 1),  # UTC #52
    (date(1992, 7, 16), 2),  # UTC #53
    (date(1992, 9, 1), 1),  # UTC #54
    (date(1992, 11, 19), 2),  # UTC #55
    (date(1993, 4, 1), 2),  # UTC #56
    (date(1993, 6, 28), 2),  # UTC #57
    (date(1993, 9, 9), 2),  # UTC #58
    (date(1993, 12, 2), 2),  # UTC #59
    (date(1994, 3, 3), 2),  # UTC #60
    (date(1994, 6, 2), 1),  # UTC #61
    (date(1994, 9, 30), 1),  # UTC #62
    (date(1994, 12, 1), 1),  # UTC #63
    (date(1995, 3, 9), 2),  # UTC #64
    (date(1995, 6, 2), 1),  # UTC #65
    (date(1995, 9, 29), 1),  # UTC #66
    (date(1995, 12, 8), 1),  # UTC #67
    (date(1996, 3, 8), 1),  # UTC #68
    (date(1996, 6, 6), 2),  # UTC #69
    (date(1996, 9, 7), 1),  # UTC #70
    (date(1996, 12, 5), 2), # UTC #71 https://www.unicode.org/L2/L1996/UTC71-Minutes.htm
    # https://www.unicode.org/L2/meetings/utc-meetings-early.html#joint
    (date(1997, 5, 29), 2), # UTC #72:  UTC - L2 ad hoc May 29–30, 1997
    (date(1997, 8, 4), 2),  # UTC #73 https://www.unicode.org/L2/L1997/97255r.pdf
    (date(1997, 12, 5), 1),  # UTC #74 https://www.unicode.org/L2/L1998/98039.pdf
    (date(1998, 2, 24), 3),  # UTC #75 https://www.unicode.org/L2/L1998/98070.pdf
    (date(1998, 4, 20), 3),  # UTC #76 https://www.unicode.org/L2/L1998/98158.html
    (date(1998, 7, 29), 3),  # UTC #77 https://www.unicode.org/L2/L1998/98281r.pdf
    (date(1998, 12, 1), 4), # UTC #78 https://www.unicode.org/L2/L1998/98419.pdf
    (date(1999, 2, 3), 3),  # UTC #079
    (date(1999, 6, 8), 3),  # UTC #080?
    (date(1999, 10, 26), 4),  # UTC #081
    (date(2000, 1, 31), 4),  # UTC #082
    (date(2000, 4, 26), 3),  # UTC #083
    (date(2000, 8, 8), 4),  # UTC #084
    (date(2000, 11, 7), 4),  # UTC #085
    (date(2001, 1, 29), 4),  # UTC #086
    (date(2001, 5, 21), 4),  # UTC #087
    (date(2001, 8, 14), 4),  # UTC #088
    (date(2001, 11, 6), 4),  # UTC #089
    (date(2002, 2, 11), 4),  # UTC #090
    (date(2002, 4, 30), 4),  # UTC #091
    (date(2002, 8, 20), 4),  # UTC #092
    (date(2002, 11, 5), 4),  # UTC #093
    (date(2003, 3, 4), 4),  # UTC #094
    (date(2003, 6, 10), 4),  # UTC #095
    (date(2003, 8, 25), 4),  # UTC #096
    (date(2003, 11, 4), 4),  # UTC #097
    (date(2004, 2, 2), 4),  # UTC #098
    (date(2004, 6, 15), 4),  # UTC #099
    (date(2004, 8, 10), 4),  # UTC #100
    (date(2004, 11, 15), 4),  # UTC #101
    (date(2005, 2, 7), 4),  # UTC #102
    (date(2005, 5, 10), 4),  # UTC #103
    (date(2005, 8, 9), 4),  # UTC #104
    (date(2005, 11, 1), 4),  # UTC #105
    (date(2006, 2, 6), 4),  # UTC #106
    (date(2006, 5, 16), 4),  # UTC #107
    (date(2006, 11, 7), 4),  # UTC #108
    (date(2006, 11, 7), 4),  # UTC #109
    (date(2007, 2, 5), 4),  # UTC #110
    (date(2007, 5, 14), 5),  # UTC #111
    (date(2007, 8, 6), 5),  # UTC #112
    (date(2007, 10, 17), 3),  # UTC #113
    (date(2008, 2, 5), 4),  # UTC #114
    (date(2008, 5, 12), 5),  # UTC #115
    (date(2008, 8, 11), 5),  # UTC #116
    (date(2008, 11, 3), 5),  # UTC #117
    (date(2009, 2, 2), 5),  # UTC #118
    (date(2009, 5, 11), 5),  # UTC #119
    (date(2009, 8, 10), 5),  # UTC #120
    (date(2009, 11, 2), 5),  # UTC #121
    (date(2010, 2, 1), 5),  # UTC #122
    (date(2010, 5, 10), 5),  # UTC #123
    (date(2010, 8, 9), 5),  # UTC #124
    (date(2010, 11, 1), 5),  # UTC #125
    (date(2011, 2, 7), 5),  # UTC #126
    (date(2011, 5, 9), 5),  # UTC #127
    (date(2011, 8, 1), 5),  # UTC #128
    (date(2011, 10, 31), 5),  # UTC #129
    (date(2012, 2, 6), 5),  # UTC #130
    (date(2012, 5, 7), 5),  # UTC #131
    # https://www.unicode.org/L2/meetings/utc-meetings.html#recent
    (date(2012, 7, 30), 5),  # UTC #132
    (date(2012, 11, 5), 5),  # UTC #133
    (date(2013, 1, 28), 5),  # UTC #134
    (date(2013, 5, 6), 5),  # UTC #135
    (date(2013, 7, 29), 4),  # UTC #136
    (date(2013, 11, 4), 4),  # UTC #137
    (date(2014, 2, 3), 4),  # UTC #138
    (date(2014, 5, 6), 4),  # UTC #139
    (date(2014, 8, 5), 4),  # UTC #140
    (date(2014, 10, 27), 4),  # UTC #141
    (date(2015, 2, 2), 4),  # UTC #142
    (date(2015, 5, 4), 5),  # UTC #143
    (date(2015, 7, 27), 5),  # UTC #144
    (date(2015, 11, 2), 3),  # UTC #145
    (date(2016, 1, 25), 4),  # UTC #146
    (date(2016, 5, 9), 5),  # UTC #147
    (date(2016, 8, 2), 4),  # UTC #148
    (date(2016, 11, 1), 4),  # UTC #149
    (date(2017, 1, 23), 4),  # UTC #150
    (date(2017, 5, 8), 5),  # UTC #151
    (date(2017, 7, 31), 5),  # UTC #152
    (date(2017, 10, 23), 5),  # UTC #153
    (date(2018, 1, 22), 4),  # UTC #154
    (date(2018, 4, 30), 5),  # UTC #155
    (date(2018, 7, 23), 5),  # UTC #156
    (date(2018, 9, 18), 3),  # UTC #157
    (date(2019, 1, 14), 4),  # UTC #158
    (date(2019, 4, 30), 4),  # UTC #159
    (date(2019, 7, 23), 4),  # UTC #160
    (date(2019, 10, 7), 4),  # UTC #161
    (date(2020, 1, 13), 4),  # UTC #162
    (date(2020, 4, 28), 4),  # UTC #163
    # TODO(egg): The 2-day ones are wrong, there is a gap.
    (date(2020, 7, 28), 2),  # UTC #164
    (date(2020, 10, 28), 2),  # UTC #165
    (date(2021, 1, 28), 2),  # UTC #166
    (date(2021, 4, 28), 2),  # UTC #167
    (date(2021, 7, 28), 2),  # UTC #168
    (date(2021, 10, 28), 2),  # UTC #169
    (date(2022, 1, 28), 2),  # UTC #170
    (date(2022, 4, 28), 2),  # UTC #171
    (date(2022, 7, 26), 3),  # UTC #172
    (date(2022, 11, 1), 3),  # UTC #173
    (date(2023, 1, 24), 3),  # UTC #174
    (date(2023, 4, 25), 3),  # UTC #175
    (date(2023, 7, 25), 3),  # UTC #176
    (date(2023, 11, 1), 3),  # UTC #177
    (date(2024, 1, 23), 3),  # UTC #178
    (date(2023, 4, 23), 3),  # UTC #179
    (date(2023, 7, 23), 3),  # UTC #180
]

t = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()

next_utc = next(i for i, (date, duration) in enumerate(UTC) if date > t)
#print(next_utc)
days_to_next_utc = (UTC[next_utc][0] - t).days
days_since_previous_utc = (t - UTC[next_utc - 1][0]).days
if days_since_previous_utc < UTC[next_utc - 1][1]:
    # During UTC
    n = days_since_previous_utc + 1
    print(t.strftime("%A, ") +
        ("first" if n == 1 else
         "second" if n == 2 else
         "third" if n == 3 else f"{n}th") +
         f" day of UTC #{OFFSET + next_utc - 1}")
elif days_to_next_utc <= 7:
    print(t.strftime("%A ") + f"before UTC #{OFFSET + next_utc}")
else:
    year, week = UTC[next_utc][0].isocalendar()[:2]
    start_of_utc_week = date.fromisocalendar(year, week, 1)
    weeks = ((start_of_utc_week - t).days - 1) // 7 + 1
    print(t.strftime("%A, ") +
        ("last week" if weeks == 1 else
         f"{weeks} weeks") +
         f" before UTC #{OFFSET + next_utc}")