'''
In this example code we use the STEP files we have created to finish our mesh preparation.
We know that the top hat model is badly located, so our first task will be to translate it.
We can then use occ kernel functions to generate a completed mesh.
'''

import gmsh
gmsh.initialize()

snowman_file = "step_files/snowman.step"
tophat_file = "step_files/tophat.step"

## We begin by importing geometry of the top hat, we will use translation and only after that will we import the snowman model.
tophat = gmsh.model.occ.importShapes(fileName=tophat_file)
tophat = gmsh.model.occ.getEntities(dim=3)
print(f"The top hat Entity has a tag: {tophat}") 

## We now do the translation. We know that the top of snowman's hat has coordinates (0,0,36) and we know
## that bottom of the hat has coordinates (0,0,0)
gmsh.model.occ.translate(dimTags=tophat,dx=0,dy=0,dz=34.5)

## We will now import the snowman model
snowman = gmsh.model.occ.importShapes(fileName=snowman_file)

## Now we have to use occ.fragment() to create a mesh, that can be used for FEM simulations.
outDimTags, outDimTagsMap = gmsh.model.occ.fragment(objectDimTags=snowman,toolDimTags=tophat)
print("-----------")
print(outDimTags)
print(outDimTagsMap)

gmsh.model.occ.synchronize()
## We add PhysicalGroups to increase the options for FEM simulations.
gmsh.model.addPhysicalGroup(dim=3,tags=[1],tag=1,name="tophat")
gmsh.model.addPhysicalGroup(dim=3,tags=[2],tag=2,name="hothead")
gmsh.model.addPhysicalGroup(dim=3,tags=[3],tag=3,name="snowman")

gmsh.model.mesh.generate(dim=3)
gmsh.write("snowman_with_hat.msh")

gmsh.finalize()