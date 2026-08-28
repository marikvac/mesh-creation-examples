import gmsh
'''Import your Gmsh. If you are using python's virtual environment, 
make sure that you have Gmsh installed in it'''

gmsh.initialize()
'''This way you initialize the gmsh API. This has to be called because you are basically using
Python to interact with Gmsh functionality.'''

rect = gmsh.model.occ.addRectangle(
    x=0,
    y=0,
    z=0,
    dx=10,
    dy=10,
    tag=1
)
'''Use the OpenCASCADE kernel function to add a rectangle in a OpenCASCADE CAD representation
 with a tag 1 to your model. If you don't want to choose a tag you can use tag=-1 or do nothing.
 This function returns the tag and it is stored in rect variable'''
print(f"Rectangle has a tag: {rect}")
print(f"Rectangle has a type: {type(rect)}")

gmsh.model.occ.synchronize()
'''You have to synchronize the OpenCASCADE representations with current Gmsh model.
This operation is nontrivial and number of synchronizations should thus be minimized.
Until you synchronize you can use only functions from occ on the entities.'''

gmsh.model.mesh.generate(dim=2)
"""Generate a mesh of the current model."""

gmsh.write("meshes/rectangle.msh")
'''To save your mesh use gmsh.write(). 
Note that .msh is not the only supported format. You can also save your creation in 
formats like: stl, brep, mesh, vtk. These will be useful for us later.'''
gmsh.finalize()