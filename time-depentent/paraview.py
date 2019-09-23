from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source

#dense
sources = {
    "P1": 17450,
    "P2": 17450,
    "Q1": 36864,
    "Q2": 36864,
    }

#coarse
# sources = {
#     "P1": 49531,
#     "P2": 49531,
#     "Q1": 26896,
#     "Q2": 26896,
# }

# Create a new 'Quartile Chart View'
quartileChartView = CreateView('QuartileChartView')
quartileChartView.ViewSize = [976, 426]

spreadSheetView = CreateView('SpreadSheetView')
spreadSheetView.BlockSize = 1024L


# get layout
layout = GetLayout()
layout.AssignView(2, quartileChartView)
layout.AssignView(3, spreadSheetView)


for k in sources:
    source = FindSource('{}_step_*'.format(k))

    # create a new 'Plot Selection Over Time'
    sel = SelectPoints(query="id=={}".format(sources[k]))
    plotSelectionOverTime = PlotSelectionOverTime(Input=source, Selection=sel)

    # show data in view
    plotSelectionOverTimeDisplay = Show(plotSelectionOverTime, quartileChartView)
    plotSelectionOverTimeTable = Show(plotSelectionOverTime, spreadSheetView)
    ExportView('/Users/teseo/data/tet-vs-hex/time-depentent/vtu/{}.csv'.format(k), view=spreadSheetView)


    # trace defaults for the display properties.
    plotSelectionOverTimeDisplay.AttributeType = 'Row Data'
    plotSelectionOverTimeDisplay.UseIndexForXAxis = 0
    plotSelectionOverTimeDisplay.XArrayName = 'Time'
    plotSelectionOverTimeDisplay.SeriesVisibility = ['solution (1) (stats)']
    plotSelectionOverTimeDisplay.SeriesLabel = ['discr (stats)', 'discr (stats)', 'scalar_value (stats)', 'scalar_value (stats)', 'scalar_value_avg (stats)', 'scalar_value_avg (stats)', 'solution (0) (stats)', 'solution (0) (stats)', 'solution (1) (stats)', k, 'solution (2) (stats)', 'solution (2) (stats)', 'solution (Magnitude) (stats)', 'solution (Magnitude) (stats)', 'tensor_value_11 (stats)', 'tensor_value_11 (stats)', 'tensor_value_12 (stats)', 'tensor_value_12 (stats)', 'tensor_value_21 (stats)', 'tensor_value_21 (stats)', 'tensor_value_22 (stats)', 'tensor_value_22 (stats)', 'vtkOriginalPointIds (stats)', 'vtkOriginalPointIds (stats)', 'X (stats)', 'X (stats)', 'Y (stats)', 'Y (stats)', 'Z (stats)', 'Z (stats)', 'N (stats)', 'N (stats)', 'Time (stats)', 'Time (stats)', 'vtkValidPointMask (stats)', 'vtkValidPointMask (stats)']
    plotSelectionOverTimeDisplay.SeriesColor = ['discr (stats)', '0', '0', '0', 'scalar_value (stats)', '0.89', '0.1', '0.11', 'scalar_value_avg (stats)', '0.22', '0.49', '0.72', 'solution (0) (stats)', '0.3', '0.69', '0.29', 'solution (1) (stats)', '0.6', '0.31', '0.64', 'solution (2) (stats)', '1', '0.5', '0', 'solution (Magnitude) (stats)', '0.65', '0.34', '0.16', 'tensor_value_11 (stats)', '0', '0', '0', 'tensor_value_12 (stats)', '0.89', '0.1', '0.11', 'tensor_value_21 (stats)', '0.22', '0.49', '0.72', 'tensor_value_22 (stats)', '0.3', '0.69', '0.29', 'vtkOriginalPointIds (stats)', '0.6', '0.31', '0.64', 'X (stats)', '1', '0.5', '0', 'Y (stats)', '0.65', '0.34', '0.16', 'Z (stats)', '0', '0', '0', 'N (stats)', '0.89', '0.1', '0.11', 'Time (stats)', '0.22', '0.49', '0.72', 'vtkValidPointMask (stats)', '0.3', '0.69', '0.29']
    plotSelectionOverTimeDisplay.SeriesPlotCorner = ['discr (stats)', '0', 'scalar_value (stats)', '0', 'scalar_value_avg (stats)', '0', 'solution (0) (stats)', '0', 'solution (1) (stats)', '0', 'solution (2) (stats)', '0', 'solution (Magnitude) (stats)', '0', 'tensor_value_11 (stats)', '0', 'tensor_value_12 (stats)', '0', 'tensor_value_21 (stats)', '0', 'tensor_value_22 (stats)', '0', 'vtkOriginalPointIds (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'N (stats)', '0', 'Time (stats)', '0', 'vtkValidPointMask (stats)', '0']
    plotSelectionOverTimeDisplay.SeriesLabelPrefix = ''
    plotSelectionOverTimeDisplay.SeriesLineStyle = ['discr (stats)', '1', 'scalar_value (stats)', '1', 'scalar_value_avg (stats)', '1', 'solution (0) (stats)', '1', 'solution (1) (stats)', '1', 'solution (2) (stats)', '1', 'solution (Magnitude) (stats)', '1', 'tensor_value_11 (stats)', '1', 'tensor_value_12 (stats)', '1', 'tensor_value_21 (stats)', '1', 'tensor_value_22 (stats)', '1', 'vtkOriginalPointIds (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
    plotSelectionOverTimeDisplay.SeriesLineThickness = ['discr (stats)', '2', 'scalar_value (stats)', '2', 'scalar_value_avg (stats)', '2', 'solution (0) (stats)', '2', 'solution (1) (stats)', '2', 'solution (2) (stats)', '2', 'solution (Magnitude) (stats)', '2', 'tensor_value_11 (stats)', '2', 'tensor_value_12 (stats)', '2', 'tensor_value_21 (stats)', '2', 'tensor_value_22 (stats)', '2', 'vtkOriginalPointIds (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'N (stats)', '2', 'Time (stats)', '2', 'vtkValidPointMask (stats)', '2']
    plotSelectionOverTimeDisplay.SeriesMarkerStyle = ['discr (stats)', '0', 'scalar_value (stats)', '0', 'scalar_value_avg (stats)', '0', 'solution (0) (stats)', '0', 'solution (1) (stats)', '0', 'solution (2) (stats)', '0', 'solution (Magnitude) (stats)', '0', 'tensor_value_11 (stats)', '0', 'tensor_value_12 (stats)', '0', 'tensor_value_21 (stats)', '0', 'tensor_value_22 (stats)', '0', 'vtkOriginalPointIds (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'N (stats)', '0', 'Time (stats)', '0', 'vtkValidPointMask (stats)', '0']

# update the view to ensure updated data information
quartileChartView.Update()

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
