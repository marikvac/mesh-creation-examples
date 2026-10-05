'''
In this example code we use the STEP files we have created to finish our mesh preparation.
We know that the top hat model is badly located, so our first task will be to translate it.
We can then use occ kernel functions to generate a completed mesh.

This time we will do something different opposed to what we did with a SNOWMAN.
This time we have to cut the ventricular volume out of our brain structure and
we also have to create a sharp interface between white and grey matter.
'''

import gmsh
gmsh.initialize()

pial_file = "step_files/pial.step"
white_file = "step_files/white.step"
ventricles_file = "step_files/ventricles.step"
## We begin by importing geometry of the white and grey matter. We are going to process them in a way,
## that creates a sharp inteface between GM and WM. In our file called pial.step the whole volume
## bounded by pial surface is stored, i.e. both WM and GM.
## Our first step is to cut WM out of it, while "keeping the tool".
pial = gmsh.model.occ.importShapes(fileName=pial_file)
white = gmsh.model.occ.importShapes(fileName=white_file)
ventricles = gmsh.model.occ.importShapes(fileName=ventricles_file)

print(pial)
print(white)
print(pial + white)
print(ventricles)


## We will now use the function occ.cut(), while "keeping the tool" to create an interface between 
## white matter and grey matter
print("Start of the first cut")
afterCutDimTags,outDimTagsMap = gmsh.model.occ.cut(objectDimTags=pial,
                                              toolDimTags=white,
                                              removeTool=False)
print(f"After the cut we have the following Entities: {afterCutDimTags}")
print(outDimTagsMap)

# Sort by volume, largest first
cut_volumes = sorted(
    outDimTagsMap[0],
    key=lambda entity: gmsh.model.occ.getMass(entity[0], entity[1]),
    reverse=True
)
print(cut_volumes)

# Print results
for entity in cut_volumes:
    volume = gmsh.model.occ.getMass(entity[0], entity[1])
    print(f"{entity}: {volume}")

# Keep largest volume
largest_volume = cut_volumes[0]

# Remove the smaller fragments
small_volumes = cut_volumes[1:]

gmsh.model.occ.remove(
    small_volumes,
    recursive=True
)

gmsh.model.occ.synchronize()

print(gmsh.model.getEntities(dim=3))
print("++++++++++++++++++++")

pial_result = [largest_volume]
white_result = outDimTagsMap[1] #This is a robustness step, if it happened that the tag of WM changed

## Now that we have created a sharp interface, we can use occ.fragment() to create a conforming interface.
print("Start fragment for conforming interface")
outDimTags,outDimTagsMap = gmsh.model.occ.fragment(objectDimTags=pial_result,
                                                   toolDimTags=white_result)
gmsh.model.occ.synchronize()
print(outDimTags)
print(outDimTagsMap)

pial_after_fragment = outDimTagsMap[0]
white_after_fragment = outDimTagsMap[1]
print("+++++++++++++++++")
## We will now cut the ventricular volume out of our model.
print("Start the cut of ventricles")
object_tags = pial_after_fragment + white_after_fragment
tool_tags = ventricles
outDimTags,outDimTagsMap = gmsh.model.occ.cut(objectDimTags=object_tags,toolDimTags=ventricles)
print(outDimTags)
print(outDimTagsMap)
print(f"Length of outDimTagsMap= {len(outDimTagsMap)}") # Notice that cut created map with three parts
pial_final = outDimTagsMap[0]
white_final = outDimTagsMap[1]
# The ventricles have beed erased
print("Geometry processing done")
gmsh.model.occ.synchronize()
## Now we have done everything we wanted to do in OCC kernel. We have created a model of human brain,
## in which white and grey matter are differetiated and ventricles are cut out.
## Next step is creating PhysicalGroups for these parts.

## We add PhysicalGroups to increase the options for FEM simulations.
gmsh.model.addPhysicalGroup(dim=3,tags=[pial_final[0][1]],tag=1,name="Grey")
gmsh.model.addPhysicalGroup(dim=3,tags=[white_final[0][1]],tag=2,name="White")


gmsh.model.mesh.generate(dim=3)
gmsh.write("brain.msh")
gmsh.write("brain.step") # We will save also the step file if we ever wanted to continue with processing

gmsh.finalize()