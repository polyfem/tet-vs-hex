from paraview.simple import *
import os

sources = []
for k in GetSources():
	s = GetSources()[k]
	sources.append(s)

warpeds = []
names = []

for s in sources:
	name = s.FileName[0]
	name = os.path.splitext(os.path.basename(name))[0]
	print(name)

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
renderView.InteractionMode = '2D'
renderView.CameraPosition = [0.4999999925494194, 0.5000000074505806, 3.0191335456195794]
renderView.CameraFocalPoint = [0.4999999925494194, 0.5000000074505806, 0.0]
renderView.CameraParallelScale = 0.9455052061902393


for i in range(len(warpeds)):
	w = warpeds[i]
	n = names[i]
	Show(w)

	solutionLUT = GetColorTransferFunction('solution')
	solutionLUT.ApplyPreset('Rainbow Uniform', True)
	solutionLUT.NumberOfTableValues = 12
	solutionLUT.RescaleTransferFunction(0.0, 0.3)
	# solutionLUTColorBar.Enabled = True
	# solutionLUTColorBar = GetScalarBar(solutionLUT, renderView)
	RenderAllViews()
	SaveScreenshot('/Users/teseo/Desktop/tvh/incompressible/images/' + n + '.png', renderView, ImageResolution=[2*2204, 2*960])
	Hide(w)
