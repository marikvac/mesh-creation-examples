'''
This tutorial teaches Boolean operation available only in OCC kernel, that does difference of entities.
To show how it works we first create two overlaping 3D objects and generate their mesh.
After that, we cut the smaller one of these objects out.
We then look at the final mesh files and compare them.
'''
import gmsh

gmsh.initialize()


rectangle1 = gmsh.model.occ.addRectangle(
    x=0, y=0, z=0,
    dx=10, dy=5,tag=1
)

rectangle2 = gmsh.model.occ.addRectangle(
    x=2, y=7, z=0,
    dx=6, dy=2,tag=2
)
rectangle3 = gmsh.model.occ.addRectangle(
    x=4, y=0, z=0,
    dx=2, dy=10,tag=3
)
gmsh.model.occ.synchronize()
## We have to synchronize after every time we add elements and want to use functions outside of occ on them

gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/before_difference.msh")

gmsh.model.mesh.clear()
## This way we have cleared only the mesh part of our model. All of the elements in occ are still present.

objects = [(2,rectangle1), (2, rectangle2)]
tools = [(2,rectangle3)]
all_inputs = objects + tools

new_shapes, outDimTagsMap = gmsh.model.occ.cut(objectDimTags=objects, toolDimTags=tools)
print(50*"#")
print(f"Entities after boolean difference: {new_shapes}")

for input_entity, output_entity in zip(all_inputs, outDimTagsMap):
    print(f"{input_entity} --> {output_entity}")
print(50*"#")
## We can see, that the cylinder has been removed. We now have to synchronize to update the model with our changes.

## Let's now learn how to read outDimTagsMap:
## We have given occ.cut() three inputs, two as object and one as a tool,
## these will be represented in the output map as follows:
## First object will be outDimTagsMap[0], second object will be outDimTagsMap[1]
## and finally our tool will be outDimTagsMap[2]. They are in the same order as in the input!

## Don't forget to synchronize after changing the number of entities!
gmsh.model.occ.synchronize()
print(f"After synchronization: {gmsh.model.getEntities(dim=2)}")

## Now we know that the rectangles we had at the beginning are split into four pieces total.
## How do we know for example which one has a tag=3?
topleft_entity = gmsh.model.getEntitiesInBoundingBox(
    xmin=1.5, ymin=6.5,zmin=-0.5,
    xmax=4.5, ymax=9.5,zmax=0.5,
    dim=2
)
print(50*"#")
print(f"Tag of the rectangle that is located in top-left is {topleft_entity}.")

## This method assumes that we know the location of our entities.
## Be careful, the entity must be completely inside the bounding box you use as arguments!

## Reverse process is also possible, we can do the following:
print(50*"#")
for entity in new_shapes:
    print(f"Bounding box of entity with tag {entity[1]}:{gmsh.model.getBoundingBox(dim=2,tag=entity[1])}")
print(50*"#")

gmsh.model.mesh.generate(dim=2)
gmsh.write("meshes/after_difference.msh")

gmsh.finalize()