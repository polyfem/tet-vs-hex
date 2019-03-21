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
	ColorBy(warpedDisplay, ('POINTS', 'scalar_value_avg'))

	warpeds.append(warped)
	names.append(name)



HideAll()
RenderAllViews()

renderView = GetActiveViewOrCreate('RenderView')
renderView.OrientationAxesVisibility = 0
renderView.CameraPosition = [4.2528865459817435, 1.758183607362867, -4.761903658658314]
renderView.CameraFocalPoint = [-0.9194307035427889, -0.0903877956036081, 1.7056893390118553]
renderView.CameraViewUp = [-0.1470083030936321, 0.9758847754930258, 0.16136128340608114]
renderView.CameraParallelScale = 1.5


for i in range(len(warpeds)):
	w = warpeds[i]
	n = names[i]
	Show(w)

	solutionLUT = GetColorTransferFunction('scalar_value_avg')
	solutionLUT.ApplyPreset('Rainbow Uniform', True)
	solutionLUT.NumberOfTableValues = 12
	solutionLUT.RescaleTransferFunction(0, 140000)
	# solutionLUTColorBar.Enabled = True
	# solutionLUTColorBar = GetScalarBar(solutionLUT, renderView)
	RenderAllViews()
	SaveScreenshot('./images/' + n + '.png', renderView, ImageResolution=[2*2204, 2*960])
	Hide(w)
