
charts = []
for chart in r['weeklychartlist']['chart']:
    start = int(chart['from'])
    end   = int(chart['to'])
    charts.append(Week(start, end))

print("Number: " + str(len(charts)))
for chart in charts:
    print(str(chart))
