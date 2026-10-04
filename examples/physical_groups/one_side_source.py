'''
In this example we create a domain using the geo kernel. We will build it from ground up, 
from entities of higher and higher dimension.
This will help us, because we will know which side of our rectangular domain has which tag.

We will simulate quite a simple setting. Left side of our rectangular domain will act
as an inlet of water flow and the opposite side will be an outlet.  
'''

import gmsh

gmsh.initialize()

points_coordinates = [[0,0,0],[5,0,0],[5,3,0],[0,3,0]]
points = []
for coordinates in points_coordinates:
    points.append(gmsh.model.geo.addPoint(
        x=coordinates[0],y=coordinates[1],z=coordinates[2]
    ))
print(points)
## We can store the points we create in a list like this.

lines_start_end = []
for i in range(len(points)):
    lines_start_end.append([points[i],points[(i+1) % len(points)]])
print(lines_start_end)
## And we then turn them into a list to prepare us for creation of lines in geo kernel

lines = []
for line in lines_start_end:
    lines.append(
        gmsh.model.geo.addLine(startTag=line[0], endTag=line[1])
        )
print(lines)
## In our example the number of points and lines is the same. We are also working in a completely
## new model. The tags of points and of lines will both be [1,2,3,4].
## We can't underestimate the importance of creating a code that works independently on tags.

#boundary = gmsh.model.geo.addCurveLoop(curveTags=lines)
boundary = gmsh.model.geo.addCurveLoop(curveTags=[1,3,2,4]) 
## It does not matter in which order you give the lines, but they must form a closed loop.
## Alternatively one can use a function gmsh.model.geo.addCurveLoops(), which is advanced.
## It can find loops out of a group of lines, if they form atleast one closed loop.

surface = gmsh.model.geo.addPlaneSurface(wireTags=[boundary])

## Don't forget to synchronize, this has to be done even in geo kernel!
gmsh.model.geo.synchronize()
print(f"entities: {gmsh.model.getEntities()}")
## We can now move on to adding the needed physical groups. It will be four physical groups in total.
## We have to put inlet and outlet into separate groups. We then have to create a physical group
## for the rest of the walls, where we can impose zero-flux boundary condition.
## Finally we will create a 2D Physical group for our domain where the fluid will flow.

## We know that the outlet will be a curve with a tag=2 and inlet is a curve with a tag=4,
## because we have constructed it this way.
outlet = gmsh.model.addPhysicalGroup(dim=1, tags=[2])
inlet = gmsh.model.addPhysicalGroup(dim=1, tags=[4])
walls = gmsh.model.addPhysicalGroup(dim=1, tags=[1,3])

domain = gmsh.model.addPhysicalGroup(dim=2,tags=[surface])

gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/inlet_outlet.msh")
gmsh.finalize()