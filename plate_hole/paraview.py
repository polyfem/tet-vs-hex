import re
from paraview.simple import *

group0 = GroupDatasets()
group0.Input.Clear()
group1 = GroupDatasets()
group1.Input.Clear()
group2 = GroupDatasets()
group2.Input.Clear()
group3 = GroupDatasets()
group3.Input.Clear()

sources = []
ii = 0
for k in GetSources():
	s = GetSources()[k]
	if s == group0 or s == group1 or s == group2 or s == group3:
		continue
	sources.append(s)




for s in sources:
	name = s.FileName[0]
	print(name)

	current_group = None
	if "_0_" in name:
		current_group = group0
		print("group " + str(0))
	elif "_1_" in name:
		current_group = group1
		print("group " + str(1))
	elif "_2_" in name:
		current_group = group2
		print("group " + str(2))
	elif "_3_" in name:
		current_group = group3
		print("group " + str(3))

	Hide(s)
	if re.search('hole_q_\\d_k2', name):
		calc = Calculator(s)
		calc.Function='jHat*0'
		warped = WarpByVector(calc)
		current_group.Input.append(warped)

	elif re.search('hole_q_\\d_k1', name):
		calc = Calculator(s)
		calc.Function='-iHat*5'
		warped = WarpByVector(calc)
		r = Reflect(warped)
		r.CopyInput = False

		current_group.Input.append(r)

	elif re.search('hole_\\d_k2', name):
		calc = Calculator(s)
		calc.Function='jHat*5'
		warped = WarpByVector(calc)
		r = Reflect(warped)
		r.CopyInput = False
		r.Plane = 'Y Max'

		current_group.Input.append(r)

	elif re.search('hole_\\d_k1', name):
		calc = Calculator(s)
		calc.Function='-iHat*5 + jHat*5'
		warped = WarpByVector(calc)
		r = Reflect(warped)
		r.CopyInput = False
		r.Plane = 'Y Max'

		r1 = Reflect(r)
		r1.CopyInput = False

		current_group.Input.append(r1)

	calc = None
	warped = None
	r = None
	r1 = None
	s = None
