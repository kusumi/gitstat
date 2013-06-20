#!/usr/bin/env python

if __name__ == '__main__':
    import re
    import util

    test_date, sort = util.parse_option()
    d = dict([(x, 0) for x in range(24)])
    s = util.popen_hglog("--template", "{date|isodate}\n")
    r = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d+):\d+ ")

    for x in s.split('\n'):
        if x:
            m = r.match(x)
            if m:
                date = m.groups()[0]
                hour = int(m.groups()[1])
                if test_date(date):
                    d[hour] += 1
    if sort:
        l = sorted([(v, k) for k, v in d.items()])
        g = reversed([x[1] for x in l])
    else:
        g = range(24)

    tot = sum(d.values())
    for k in g:
        v = d[k]
        if k < 12:
            s = "AM"
        else:
            s = "PM"
            k -= 12
        if not tot:
            p = 0
        else:
            p = 100.0 * v / tot
        print("%2d %s %5d %4.1f[%%]" % (k, s, v, p))

    print('-' * 40)
    print("      %5d" % tot)
