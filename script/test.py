
from LastFmApi import *
from Week      import Week

LastFmGet = LastFmApi(key='KEY', userAgent='LastFmTimeline by D3r3k523')


r = LastFmGet.user_weekly_chart_list('D3r3k523')

charts = []
for chart in r['weeklychartlist']['chart']:
    start = int(chart['from'])
    end   = int(chart['to'])
    charts.append(Week(start, end))

print("Number: " + str(len(charts)))
for chart in charts:
    print(str(chart))
