"""
In this tutorial we show what happens when we use and don't use a boolean fragments.
This is really important when computiong for example heat transfer. That is because
we need to make sure that the interface between two areas are conformal.
A conformal mesh means that the two neighboring subdomains share a node on the interface.

If we don't make sure that the interfaces are conformal, we can prevent diffusion
between two subdomain from working in our FEM solver.
"""
import gmsh

gmsh.initialize()

## We first have to create two rectangles. We want them to intersect and then we move
## on to making the interface conformal.

rect1 = gmsh.model.occ.addRectangle(x=0,y=0,z=0,dx=5,dy=10,tag=1)
rect2 = gmsh.model.occ.addRectangle(x=3,y=3,z=0,dx=6,dy=4,tag=2)

#-----------------Before fragment---------------------#

## We can all see, that the rectangles intersect. One might say that we can prepare our mesh 
## by simply cutting out the overlapping part by using a boolean difference operation and
## not removing the 'tool' this time.
## This however will not make the interfaces conforming and thus making it imposible
## for our FEM solver to work well. 

## We will now create the mesh, just out of curiosity.

gmsh.model.occ.cut(objectDimTags=[(2,rect1)], toolDimTags=[(2,rect2)],
                   removeTool=False)
## Here we ignore the return value of cut, because we mesh everything that was returned.
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/fragment_not_used.msh")


#--------Fragment used directly--------#
gmsh.clear()
rect1 = gmsh.model.occ.addRectangle(x=0,y=0,z=0,dx=5,dy=10,tag=1)
rect2 = gmsh.model.occ.addRectangle(x=3,y=3,z=0,dx=6,dy=4,tag=2)


## We can now start the process of fragmentation, notice that we don't need to synchronize now.
## That is because we are still working only in occ kernel.

outDimTags, outDimTagsMap = gmsh.model.occ.fragment(objectDimTags=[(2,rect1)],
                                                    toolDimTags=[(2,rect2)])
## When used this way, occ operation fragment splits input entities, whenever they intersect.
## It can see the overlaping area and turns it into a new entity.
## This way we actually got three regions, that have conforming interfaces.
## This can be really useful based on the model you are creating.  

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/fragment_directly.msh")

#----------------Fragment used together with cut-----------------#
gmsh.clear()
rect1 = gmsh.model.occ.addRectangle(x=0,y=0,z=0,dx=5,dy=10,tag=1)
rect2 = gmsh.model.occ.addRectangle(x=3,y=3,z=0,dx=6,dy=4,tag=2)
all_inputs = (rect1,rect2)
## We can now use fragment the way we have intended.
## We first have to cut out the overlaping area, all while keeping the 'tool'.
## Just after that can we call the fragment function to make the interfaces conforming.

outDimTags_cut, outDimTagsMap_cut = gmsh.model.occ.cut(objectDimTags=[(2,rect1)],toolDimTags=[(2,rect2)],
                   removeTool=False)
print(50*"#")
for input_entity, output_entity in zip(all_inputs, outDimTagsMap_cut):
    print(f"{input_entity} --> {output_entity}")

## We don't know which tag was given to the remains of rect1 and which was given to the rect2.
## Note that even though we have not removed the 'tool', doesn't mean that the tag is kept unchanged.
print(outDimTagsMap_cut)
remains_of_rect1 = outDimTagsMap_cut[0][0][1]
new_tag_of_rect2 = outDimTagsMap_cut[1][0][1]
## This is a rather obscure notation. Only the first one of them is important for us.
## It looks like this because outDimTagsMap is a list of lists of tuples.
## First brackets tell us, whether we want to look at entities, 
## that are related to object [0] OR tool [1]
## Second brackets tell us, that we want to look at the first entity out of many that are 
## related to them. In this example we know that only one was created, otherwise we would have
## to somehow loop over them. Do not rely on this assumption in general. Robust code should
## iterate over the mapping.
## The last brackets tell us that we want to look at the tag in the DimTag pair.

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/fragment_and_cut.msh")

gmsh.finalize()


## We do this because there is a big difference between sharing a side in the geometrical sense,
## by that we mean being literally next to each other, and sharing side in a topological sense.
## By using occ.fragment() we tell gmsh that we want to make the interface conforming.

## Think of occ.fragment() as not a tool to change the geometry of your model, but the topology.
## Correct topological definition of interfaces is needed, when one wants to do simulations of for
## example diffusion, without it diffusion would stop at the interface and the two parts wont be 
## able to communicate. When two parts are sharing a side in a topological sense, they are 
## literally sharing the node.


#TO-DO
#PRIDAT COMMON MISTAKES
#PRIDAT PHYSICAL GROUPS
#DULEZITE JE ZE FRAGMENT NEDELA JEN CONFORMING INTERFACE, DULEZITE JE, ZE MENI TOPOLOGII
