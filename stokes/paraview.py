from paraview.simple import *
import os

sources = []
for k in GetSources():
	s = GetSources()[k]
	sources.append(s)

models = []
names = []

for s in sources:
	name = s.FileName[0]
	name = os.path.splitext(os.path.basename(name))[0]
	print(name)

	Hide(s)
	modelDisplay = Show(s)
	ColorBy(modelDisplay, ('POINTS', 'solution', 'Magnitude'))

	models.append(s)
	names.append(name)



HideAll()
RenderAllViews()

renderView = GetActiveViewOrCreate('RenderView')
renderView.InteractionMode = '2D'
renderView.CameraPosition = [0.5, 0.5, 10000.0]
renderView.CameraFocalPoint = [0.5, 0.5, 0.0]
renderView.CameraParallelScale = 0.5843857695756589


for i in range(len(models)):
	m = models[i]
	n = names[i]
	Show(m)

	solutionLUT = GetColorTransferFunction('solution')
	solutionLUT.ApplyPreset('Rainbow Uniform', True)
	solutionLUT.NumberOfTableValues = 12
	solutionLUT.RescaleTransferFunction(0.0, 0.25)
	# solutionLUTColorBar.Enabled = True
	# solutionLUTColorBar = GetScalarBar(solutionLUT, renderView)
	RenderAllViews()
	SaveScreenshot('/Users/teseo/Desktop/tvh/stokes/images/' + n + '.png', renderView, ImageResolution=[2*2204, 2*960])
	Hide(m)
