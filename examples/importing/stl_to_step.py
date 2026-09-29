'''
In this tutorial we show, how to turn information from STL files into STEP files.
STEP is a common CAD exchange format, used mainly for transfering data between different
CAD based systems.
'''
import gmsh
import numpy as np

gmsh.initialize()
stl_file_name = "stl_files/ball.stl"
gmsh.merge(stl_file_name)

# Let's now compare where the entity created by this process lives
print(gmsh.model.getEntities())
print(gmsh.model.occ.getEntities())
# We can see that this merging creates one two-dimensional entity in the current model.
# No entity is created in occ kernel! This is important, because this prevents us from using
# functions available in occ, for example boolean operations and fragment.
# We will use STEP to get access to OpenCASCADE kernel.

# We know that occ kernel is our end goal, it is better to work with occ kernel from the start.
# This way we won't rely on the export from Gmsh native geometry kernel.


#================================================================================================================#
#================================================================================================================# 


# Because STL only provides a triangular surface tessellation, we must use the mesh itself as the
# the source of CAD topology.

print(gmsh.model.mesh.getElements())
# We can see the output format is rather cryptic, but it is quite simple to understand. This function has three return values in
# total. The first one is a Gmsh code of element type, for example 2 stands for a triangle, 3 stands for a quadrilateral...
# Second returned is an array of element tags, since we started with an empty model, this is just a series of integers.
# Finally, the third is an array of elements' node tags. This array is three times longer in our case, since triangles have 
# three vertices.
# We need to use simple operations on list to turn this list into triplets for future work. We achieve this by calling reshape.


node_tags, node_coords, node_param = gmsh.model.mesh.getNodes()
print(f"Number of nodes: {len(node_tags)}")
node_coords_triplets = node_coords.reshape(-1,3)
# Only elements are not enough for us. We want to create it all in occ from ground up and so we have to start with Points/Nodes.
# Reshaping will give us one XYZ coordinate triplet per node. 
# We preserve the original node tags, because they are not guaranteed to be 1,2,3,... in general.

elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
print("Element types:", elem_types)

elem_node_tags = np.array(elem_node_tags)  #we have to turn it into numpy array to use reshape
elem_node_tags_triplets = elem_node_tags.reshape(-1,3)   #we assume that the STL contains only triangles, so we make triplets

for coord,ntag in zip(node_coords_triplets,node_tags):        #add points to occ
    gmsh.model.occ.addPoint(*coord, tag=ntag)


#================================================================================================================#
#================================================================================================================#


# We have to solve an interesting topological problem here. Each triangle has three edges, 
# but neighboring triangles share an edge. We cannot create three new occ lines independetly for every triangle.
# Two neighboring triangles might reference the same edge with opposite node ordering. 
# We solve this by using make_key(), which makes (A,B), (B,A) represent the same undirected edge.

def make_key(A,B):
    return tuple(sorted((A,B)))

line_tags_dict = {}
line_tags_list = []
for line_tags in elem_node_tags_triplets:
    edges = [[line_tags[0],line_tags[1]],[line_tags[1],line_tags[2]],[line_tags[2],line_tags[0]]]
    for edge in edges:
        key = make_key(edge[0],edge[1])
        if key in line_tags_dict:
            line_tags_list.append(line_tags_dict[key])
        else:
            new_key = gmsh.model.occ.addLine(*key)
            print(new_key)
            line_tags_list.append(new_key)
            line_tags_dict[key] = new_key

# This construction allows us to not add one edge twice. We achieve that by creating a dictionary that maps
# each unique pair of mesh-node tags to the OCC line representing the edge.

# When an edge is encountered for the first time, a new OCC line is created and stored in line_tags_dict. If the same
# edge is encountered again, while processing another triangle, the existing OCC line tag is retrieved from the dictionary
# instead of creating a duplicate line.

# Notice that the dictionary ignores edge orientation. The geometricedge is identified only by its two endpoints. 
# Curve orientation is a separate concept and is handled when the curves are assembled into a curve loop

# line_tags_list stores the OCC line tag corresponding to every edge of every triangle. 
# Since each triangle has three edges, this list will contain threeentries per triangle and can later be reshaped
# into groups of three when constructing the corresponding OCC curve loops.

line_tags_list = np.array(line_tags_list)
line_tags_list_triplets = line_tags_list.reshape(-1,3)
print(f"Is line_tags_list divisible by 3?: {len(line_tags_list)%3}")

curves_list = []
for sides in line_tags_list_triplets:
    curves_list.append(gmsh.model.occ.addCurveLoop(sides))    
print(f"Lenght of curves_list: {len(curves_list)}")


#=================================================================================================================#
#=================================================================================================================#


surfaces_list = []
step = 0
for loop in curves_list:
    surfaces_list.append(gmsh.model.occ.addPlaneSurface([loop]))
    step +=1
    if step%1000==0:
        print(step)
print(f"Number of surfaces: {len(surfaces_list)=}")
# We have created OCC representation of all triangles that were inside the STL. We now have to turn them all into 
# a surface loop. That creates a shell, that will be used as a boundary for creation of a volume.
print("Now making surface loop")
final_loop = gmsh.model.occ.addSurfaceLoop(surfaceTags=surfaces_list)
print(f"Finished making surface loop with tag: {final_loop}")

#try to healShapes before making a Volume
print("Now healing")
healed_shapes = gmsh.model.occ.healShapes([(2,final_loop)])

healed_surfs = []

for dimtag in healed_shapes:
    if dimtag[0] == 2:
        healed_surfs.append(dimtag[1])
#print(f"{healed_surfs=}")
healed_surface_loop = gmsh.model.occ.addSurfaceLoop(surfaceTags=healed_surfs)

# The STL triangles have now been converted into individual OCC faces and
# assembled into a surface loop. Although the STL may be watertight, the
# independently reconstructed OCC geometry can still contain small topological
# or geometric inconsistencies.
#
# healShapes() asks OpenCASCADE to repair and clean the supplied shapes. It may
# modify the topology or geometry and therefore returns the resulting shapes.
#
# We extract the healed 2D entities and use them to construct a new surface
# loop. This healed shell is then used as the boundary of the final OCC volume.

# This is more of a robustness step rather than a required step.


#=============================================================================#
#=============================================================================#


volume = gmsh.model.occ.addVolume([healed_surface_loop])    #Here we can put final_loop, if we are convinced healShapes()
                                                            # is unnecessary.
print(f"Created a volume with tag: {volume}")

# Finally we generate a Volume.

print(f"Number of 0D entities: {len(gmsh.model.occ.getEntities(dim=0))}")
print(f"Number of 1D entities: {len(gmsh.model.occ.getEntities(dim=1))}")
print(f"Number of 2D entities: {len(gmsh.model.occ.getEntities(dim=2))}")
print(f"Number of 3D entities: {len(gmsh.model.occ.getEntities(dim=3))}")

gmsh.model.occ.synchronize()

vols = gmsh.model.getEntities(dim=3)
print(vols)

print("Now Volume is done, we write it into a STEP file")


out_file="step/example_step.step"
print(f"write into {out_file}")
gmsh.write(out_file)

gmsh.finalize()