import gmsh
gmsh.initialize()

gmsh.model.occ.addCylinder(x=0,y=0,z=0,dx=0,dy=0,dz=0.5,r=7)
gmsh.model.occ.addCylinder(x=0,y=0,z=0.5,dx=0,dy=0,dz=6.5,r=3.5)
gmsh.model.occ.addCylinder(x=0,y=0,z=0.5,dx=0,dy=0,dz=1.5,r=4)

vols = gmsh.model.occ.getEntities(dim=3)
gmsh.model.occ.fuse(objectDimTags=vols,toolDimTags=[(3,1)])

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(dim=3)
gmsh.model.mesh.refine()

gmsh.write("tophat.msh")
gmsh.write("tophat.stl")

gmsh.finalize()