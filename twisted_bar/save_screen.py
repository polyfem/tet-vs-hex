from paraview.simple import *
import os

sources = []
for k in GetSources():
	s = GetSources()[k]
	sources.append(s)

warpeds = []
names = []

for source in sources:
	name = source.FileName[0]
	name = os.path.splitext(os.path.basename(name))[0]
	print(name)
	hexes = name.find('_h') > 0

	if hexes:
		calc = Calculator(source)
		calc.CoordinateResults = True
		calc.Function = 'coordsX*iHat+coordsY*jHat+(coordsZ-50)*kHat'
		calc.ResultArrayName='disp_' + name
		s = calc
	else:
		s = source

	warped = WarpByVector(Input=s)
	warped.Vectors = ['POINTS', 'solution']

	Hide(s)
	warpedDisplay = Show(warped)
	ColorBy(warpedDisplay, ('POINTS', 'solution', 'Magnitude'))

	warpeds.append(warped)
	names.append(name)



HideAll()
RenderAllViews()

renderView = GetActiveViewOrCreate('RenderView')
renderView.OrientationAxesVisibility = 0
renderView.CameraPosition = [-0.0009298324584960938, -207.86145358251065, 0.0]
renderView.CameraFocalPoint = [-0.0009298324584960938, 0.00030040740966796875, 0.0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]
renderView.CameraParallelScale = 53.79858068100626


for i in range(len(warpeds)):
	w = warpeds[i]
	n = names[i]
	Show(w)

	solutionLUT = GetColorTransferFunction('solution')
	solutionLUT.ApplyPreset('Rainbow Uniform', True)
	solutionLUT.NumberOfTableValues = 12
	solutionLUT.RescaleTransferFunction(0.0, 30)
	# solutionLUTColorBar.Enabled = True
	# solutionLUTColorBar = GetScalarBar(solutionLUT, renderView)
	RenderAllViews()
	SaveScreenshot('/Users/teseo/data/tvh/twisted_bar/images/' + n + '.png', renderView, ImageResolution=[2*2204, 2*960])
	Hide(w)
