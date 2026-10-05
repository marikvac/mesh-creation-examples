'''
In this tutorial we take a look at importing shapes from STEP or BREP files.
This is a very important part of our process of turning STL files into fully functional
mesh used in FEM solvers.

This imports shapes from the files and creates their OpenCASCADE representation.
This also means that they are present in occ kernel, and we can thus use for example
boolean operations on them.

Ways of obtaining STEP and BREP files are described in another tutorial.
'''
import gmsh

## We will obtain geometry from a STEP file, inspect it to see what entities are present
## and create PhysicalGroups for the 3D domain and the boundary.


gmsh.initialize()
step_file = "step_files/component.step"
gmsh.model.occ.importShapes(fileName=step_file)

## These entities now live in the OCC kernel and we want to transfer them into the current model
gmsh.model.occ.synchronize()

volumes = gmsh.model.getEntities(3)
surfaces = gmsh.model.getEntities(2)
curves = gmsh.model.getEntities(1)
points = gmsh.model.getEntities(0)

print(f"Volumes:\n{volumes}")
print(f"Surfaces\n{surfaces}")
print(f"Curves:\n{curves}")
print(f"Points:\n{points}")

volumes_tags = [tag for dim,tag in volumes]
surface_tags = [tag for dim,tag in surfaces]

# Add PhysicalGroups

gmsh.model.addPhysicalGroup(dim=3,tags=volumes_tags,name="Domain")
gmsh.model.addPhysicalGroup(dim=2,tags=surface_tags,name="Boundary")

## Note that alternatively one can use Gmsh function that lists boundaries of a volume you have chosen
boundary = gmsh.model.getBoundary(dimTags=volumes)
print(f"Boundary is: {boundary}")

## We save our processed mesh with PhysicalGroups
gmsh.model.mesh.generate(dim=3)
gmsh.write("msh_files/component.msh")

gmsh.finalize()