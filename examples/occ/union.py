'''
This tutorial teaches Boolean operation available only in OCC kernel, that does union of entities.
To show how it works we first create three overlaping 3D objects and generate their mesh.
After that, we unite these objects into a single entity and do the same.
We then look at the final mesh files and compare them.
'''
import gmsh

gmsh.initialize()

sphere1 = gmsh.model.occ.addSphere(
    xc=0, yc=0, zc=0,
    radius=4, tag=1
)

cylinder = gmsh.model.occ.addCylinder(
    x=0, y=0, z=0,
    dx=10, dy=10, dz=5,
    r=3, tag=2
)

sphere2 = gmsh.model.occ.addSphere(
    xc=10,yc=10,zc=5,
    radius=4,tag=3
)
## First we add 3 objects in OpenCASCADE CAD representation. 
## We have explicitly defined their tags, this however wasn't necessary.
## We can see that these objects are overlaping.

print(f"Before synchronization: {gmsh.model.getEntities(dim=3)}")
gmsh.model.occ.synchronize()  
print(f"After synchronization: {gmsh.model.getEntities(dim=3)}")
## Don't forget to always synchronize after adding entities. This makes the entities available to
## functions outside the occ kernel.

gmsh.model.mesh.generate(dim=3)
gmsh.write("meshes/before_union.msh")
## Take a good look at this mesh in Gmsh graphical interface or possibly in a different app.
## You can see, that all of the entities are distinguished by color. You can also see, that 
## all of these entities have a mesh around them generated, these meshes overlap and create 
## a very dense net in the overlaping areas, this is unwanted behavior. 


gmsh.model.mesh.clear()

united_entity, outDimTagsMap = gmsh.model.occ.fuse(objectDimTags=[(3,sphere1)], toolDimTags=[(3,cylinder),(3,sphere2)])

print(f"New entity after fuse: {united_entity}")
print(f"Mapping of tags before and after fuse: {outDimTagsMap}")
print(f"Entities after fuse: {gmsh.model.getEntities(dim=3)}")
gmsh.model.occ.synchronize()
print(f"Entities after fuse and synchronization: {gmsh.model.getEntities(dim=3)}")
## Without the synchronization done here, Gmsh still remembers the old setup.
## We need to tell Gmsh that there has been changes in the model.


gmsh.model.mesh.generate(dim=3)
gmsh.write("meshes/after_union.msh")
## Here we can see, that after the call of fuse(), only one Volume is present in the model.

gmsh.finalize()