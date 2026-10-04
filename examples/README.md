# Gmsh Python API Tutorial Folder
This folder contains a collection of educational code resources designed to explain the Gmsh usage.
Because the files are built as a study material, the code inside it is **heavily commented**.
## Cleaning the code
If you want to use these code snippets in your own project without the disturbing tutorial explanation comments, please consider using our cleaning script.

We prefix every tutorial style comment with a double hash (`##`), this way we can filter out these unwanted lines quite easily. 
To generate ready-to-use code run the script *comments_cleaner.py*.

# How to use this folder.
Scripts in this folder vary in complexity significantly. We start with entry-level Gmsh basics, and build up towards more advanced uses.

The ultimate goal of this whole github repository is to show the complete pipeline of creating a computational mesh of a brain. In order to do that, several parts of Gmsh are needed, namely:
1. Merging of STL files
2. Storing geometry in STEP/BREP files
2. Usage of OpenCASCADE kernel
2. Inspecting mesh elements

Each tutorial focuses on a single piece of this puzzle.
Ultimately we fuse our knowledge into a complete project.

### Complete examples
We have decided to create two complete examples that begin with an STL file and end with a mesh that is ready to be used in a FEM solver such as Firedrake. Namely we have created a model of a snowman with a top hat on which a heat equation is solved. Second example is creating of mesh of a left hemisphere of the brain.

### Tutorials on importing
Since Gmsh works with two geometry kernels, which can not share entities importing information from a file is brings some difficulties. If one proceeds with caution and knows, where the entities he is adding are "living" everything will work smoothly.

We have focused mainly on merging information that is stored in an STL file. Alternative are CAD files, which bear more elegant information which would potentially be very useful. Medical software however has STL as one of their main output formats. 

### Tutorials on OCC
We have focused mainly on Boolean operations, that are available in this kernel. Boolean union and difference are available, as well as a function occ.fragment(), which will be the most important for us. It will allow us to make interfaces conforming, ultimately leading to a mesh perfectly suited for FEM simulations.

### Tutorials on PhysicalGroups
PhysicalGroups are very important part of creating a mesh. They are a way of distinguishing parts of your mesh, so that you can for example impose a boundary condition or simulate different rate of glioma growth in white and grey matter.

Tip: Because this part heavily uses OCC Boolean functions, we recommend looking at OCC tutorials first.