from paraview.simple import *

colors = {'P1': [9, 132, 227], 'P2': [108, 92, 231], 'Q1': [225, 112, 85], 'Q2': [214, 48, 49]}

centre = 9.5

ii = 0
sources = []
for k in GetSources():
	s = GetSources()[k]
	sources.append(s)

layout = GetLayout()
layout.SplitHorizontal(0, 0.5)
SetActiveView(None)
lineChartView = CreateView('XYChartView')
layout.AssignView(2, lineChartView)
SetActiveView(lineChartView)



for source in sources:
	s = None
	filename = source.FileName[0]
	title = filename[-6:-4].title()
	hexes = filename.find('_h') > 0

	if hexes:
		title = "Q" + title[-1]
	else:
		title = "P" + title[-1]

	# if hexes:
	# 	calc = Calculator(source)
	# 	calc.CoordinateResults = True
	# 	calc.Function = 'coordsX*iHat+coordsY*jHat+(coordsZ-50)*kHat'
	# 	calc.ResultArrayName='disp_' + title
	# 	s = calc
	# else:
	# 	s = source
	s = source

	calc = Calculator(s)
	calc.Function='atan(solution_X/solution_Y)'
	calc.ResultArrayName='angle_' + title
	# calc_res = Show(calc)

	line = PlotOverLine(calc)
	line.Source.Point1=[centre, centre, -50]
	line.Source.Point2=[centre, centre, 50]
	line_res = Show(line)
	line_res.SeriesVisibility = ['angle_' + title]
	line_res.SeriesLabel[1] = title + ' ' + str(centre)

	line_res.SeriesColor[1] = str(colors[title][0]/255.)
	line_res.SeriesColor[2] = str(colors[title][1]/255.)
	line_res.SeriesColor[3] = str(colors[title][2]/255.)

	SaveData('/Users/teseo/Desktop/tvh/twisted_bar/data/' + title + '.csv', proxy=line, Precision=30)
