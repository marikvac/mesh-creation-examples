'''
In this example we describe the process that will lead to creation of a model, that might
be useful in computing heat transfer.
We will create adomain, whose boundary will be a separate Physical group.
This is useful because you can then make this boundary a source of heat in your favorite
FEM solver.
'''

import gmsh

gmsh.initialize()
domain = gmsh.model.occ.addRectangle(0,0,0,10,5)  #We don't have to give the tag explicitly here
gmsh.model.occ.synchronize()  #Don't forget to synchronize when adding elements

boundary = gmsh.model.getBoundary(dimTags=[(2,domain)])
boundary_tags = [side[1] for side in boundary]
print(f"boundary tags: {boundary_tags}")
domain_group = gmsh.model.addPhysicalGroup(dim=2, tags=[domain])
gmsh.model.setPhysicalName(dim=2, tag=domain_group, name="Domain")

boundary_group = gmsh.model.addPhysicalGroup(dim=1, tags=boundary_tags)
gmsh.model.setPhysicalName(dim=1, tag=boundary_group, name="Boundary")

#Inspecting the Physical groups
print(f"Physical groups: {gmsh.model.getPhysicalGroups()}")

gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/boundary_source.msh")

gmsh.finalize()
