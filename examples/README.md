# What is this folder
This is a folder in which a lot of possibly useful code is presented.
It is intended to serve as a study material, and so the code inside it is heavily commented.
## Cleaning the code
If you want to clear the code of disturbing comments, please consider using our cleaning script.
We have started every tutorial style comment with a double hash ##, this way we can filter out these unwanted lines quite easily. The script is called *comments_cleaner.py*.

# How to use this folder.
Content of this folder varies in complexity significantly. We have decided to present the completely entry level uses of Gmsh, as well as the more complex uses.
The ultimate goal of this whole github repository is to show the pipeline of creating a computational mesh of a brain. In order to do that several parts of Gmsh are needed, namely:
1. Merging of STL files
2. Storing geometry in STEP/BREP files
2. Usage of OpenCASCADE kernel
2. Inspecting mesh elements

To show every part of this process we have created a number of tutorial scripts that try to focus on only a single part of this process.
Ultimately we fuse our knowledge into a single project.

### Complete examples
We have decided to create two complete examples that begin with an STL file and end with a mesh that is ready to be used in a FEM solver such as Firedrake. Namely we have created a model of a snowman with a top hat on which a heat equation is solved. Second example is creating of mesh of a left hemisphere of the brain.

### Tutorial on importing
Since Gmsh works with two geometry kernels, which can not share entities importing information from a file is brings some difficulties. If one proceeds with caution and knows, where the entities he is adding are "living" everything will work smoothly.

We have focused mainly on merging information that is stored in an STL file. Alternative are CAD files, which bear more elegant information which would potentially be very useful. Medical software however has STL as one of their main output formats. 

Inside STL files, only the information about 