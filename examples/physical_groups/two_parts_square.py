import gmsh

gmsh.initialize()

big = gmsh.model.occ.addRectangle(x=0,y=0,z=0,
                            dx=1,dy=1,tag=1)
small = gmsh.model.occ.addRectangle(x=0.25,y=0.25,z=0,
                            dx=0.5,dy=0.5,tag=2)
'''Create two concentric squares, then using OpenCASCADE functions make them not overlap.
Turn the two parts into two Physical groups.'''

print(f"Bigger square has a tag: {big},\nsmaller square has a tag: {small}")

outDimTags, outDimTagsMap = gmsh.model.occ.fragment(objectDimTags = [(2,big)], toolDimTags = [(2,small)])
'''To cut the smaller square out of the bigger one we have to use gmsh.model.occ.fragment().
Notice that this functions takes vectors of DimTags as arguments. 

If we were to cut more holes we would have done that 
by using for example toolDimTags=[(2,tag_1),(2,tag_2),(2,tag_3)]'''
print(f"Entities created by a fragment: {outDimTags}")

gmsh.model.occ.synchronize()
'''Synchronization is needed, since we want to now use functions outside of occ kernel.'''

gmsh.model.addPhysicalGroup(dim = 2,tags = [3],tag = 1)
'''Bigger square will have PhysicalGroup tag 1, but will preserve tag 3 in Gmsh model.'''
gmsh.model.addPhysicalGroup(dim = 2, tags = [2], tag = 2)

print(gmsh.model.getPhysicalGroups(dim = 2))
'''If you want to see current Physical groups use this function.'''

gmsh.write("two_parts_square.msh")
gmsh.finalize()