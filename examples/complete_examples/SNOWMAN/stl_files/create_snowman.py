import gmsh

gmsh.initialize()

base = gmsh.model.occ.addSphere(xc=0,yc=0,zc=0,radius=10)
base_button1 = gmsh.model.occ.addSphere(xc=0,yc=9,zc=3,radius=1)
base_button2 = gmsh.model.occ.addSphere(xc=0,yc=9,zc=-3,radius=1)


body = gmsh.model.occ.addSphere(xc=0,yc=0,zc=17,radius=8)
body_button = gmsh.model.occ.addSphere(xc=0,yc=8,zc=17,radius=1)

head = gmsh.model.occ.addSphere(xc=0,yc=0,zc=30,radius=6)
left_eye = gmsh.model.occ.addSphere(xc=2.5,yc=4,zc=30+1.5,radius=1.5)
left_eye = gmsh.model.occ.addSphere(xc=-2.5,yc=4,zc=30+1.5,radius=1.5)
carrot = gmsh.model.occ.addCone(x=0,y=5,z=30,dx=0,dy=4,dz=0,r1=1,r2=0) 

vols = gmsh.model.occ.getEntities(dim=3)

print(carrot)
print(vols)
gmsh.model.occ.fuse(objectDimTags=vols,toolDimTags=[(3,carrot)])

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(dim=3)
gmsh.model.mesh.refine()

gmsh.write("snowman_parts.msh")
gmsh.write("snowman_parts.stl")

gmsh.finalize()