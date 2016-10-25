from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from urllib.request import urlopen

url = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT_CHARS = '#:'
data = []

for line in urlopen(url).readlines():
    line = line.decode('utf-8')
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])

pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
time = [row[0]+row[1]/12.0 for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.width = 300
lp.height = 125
lp.data = [list(zip(time,pred)),list(zip(time,high)),list(zip(time,low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

draw = Drawing(400,200)
s = String(250,150,'Sunspots',fontSize=14,fillColor=colors.red)
draw.add(lp)
draw.add(s)

renderPDF.drawToFile(draw,'report.pdf','Sunspots')