'''
Import an STL surface and generate a 3D tetrahedral mesh.

A STL file describes a surface using triangles. It does not explicitly 
describe the volume enclosed by that surface.
In this example, we:
1. Import the STL surface
2. Create a surface surface_loop from the imported surfaces.
3. Create a volume bounded by that surface surface_loop.
4. Generate a 3D tetrahedral mesh.
5. Save the resulting mesh as a Gmsh MSH file.
'''
import gmsh

'''In this example code we shown how to import information from an STL file
and then use to to generate 3D mesh.
It is important to note that STL file has information only about the shell of the model 
you want. That is why we need to give Gmsh enough information to create a Volume under this shell.'''

gmsh.initialize()

gmsh.merge("stl_files/ball.stl")
'''Note that the STL you are importing must form a closed surface in order to be able to create a 
volume this surface encloses. Use STL-healing tools to ensure the STL is watertight.'''


surface_entities = gmsh.model.getEntities(dim=2)
triangle_elements_types, triangle_elements_tags, triangle_elements_nodes = gmsh.model.mesh.getElements(dim=2)
print(f"Number of surface_entities: {len(surface_entities)}")
print(surface_entities)
print(f"Number of 2D elements: {len(triangle_elements_tags[0])}")
print(triangle_elements_tags)
print(triangle_elements_types)
'''What you can see here is really important when working with STL files and 
importing into Gmsh in general.
You can see that Surface entities are represented by a standard dimtags vector. This a structure,
that is typical of Gmsh and we will see it often.
On the other hand, when you call getElements() you will get a different structure. Data is
stored as arrays with a defined type. When accessing it one must know that he has to interact with 
the first element of this array, i.e. array[0].

In this example only triangles were present, that is why triangle_elements_types
is simply a number 2, that stands for triangles.

Every mesh element belongs to exactly one model entity. Think of elements as our final product.
We want to make a tetrahedral mesh. In order to tell Gmsh where to build these tetrahedra we
create an entity, for example a rectangle or a ball.
When however we merge a STL file, it consists information both about entities and elements in it.
'''

surface_loop_tag = gmsh.model.geo.addSurfaceLoop([1])
#Before creating a Volume, we first have to stitch our Surface into a SurfaceLoop.
#Surface is a 2D entity, imagine a sheet of fabric.
#We have to turn it into a SurfaceLoop, that must be watertight/without holes and has to 
#enclose a Volume. Only then can we tell Gmsh to add Volume.
#Surface looking like a shell is not enough, it has to actually be represented like one.
volume_tag = gmsh.model.geo.addVolume(shellTags=[surface_loop_tag])

print(f"The dimension of our model is now: {gmsh.model.getDimension()}")
#This shows the importance of synchronizing. We can see that before synchronization, Gmsh 
#doesn't recognize the Volume we have just created.
gmsh.model.geo.synchronize()
print("Now we have synchronized")
print(f"The dimension of our model is now: {gmsh.model.getDimension()}")

volume_entities = gmsh.model.getEntities(dim=3)
print(f"Number of 3D Volume entities: {len(volume_entities)}")

gmsh.model.mesh.generate(dim=3)
'''This time we generate a 3-dimensional mesh.'''
gmsh.write("volume_mesh.msh")

gmsh.finalize()