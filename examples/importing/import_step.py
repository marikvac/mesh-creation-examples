'''
In this tutorial we take a look at importing shapes from STEP or BREP files.
This is a very important part of our process of turning STL files into fully functional
mesh used in FEM solvers.

This imports shapes from the files and creates their OpenCASCADE representation.
This also means that they are present in occ kernel, and we can thus use for example
boolean operations on them.

Ways of obtaining STEP and BREP files are described in another tutorial.
'''
import gmsh

gmsh.initialize()

