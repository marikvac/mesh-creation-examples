# Gmsh

Gmsh is an open source 3D finite element mesh generator.

It allows the user to generate meshes using a graphical user interface, command line, Gmsh own scripting language and through C++, C, Python, Julia and Fortran API.

## Useful links
- See their [website](https://gmsh.info/) for general information.
- See their [reference_manual](https://gmsh.info/doc/texinfo/gmsh.html) for complete documentation.

It is on you to decide, how you want to use Gmsh. I however recomend it's Python API. To see the commands that it allows, please take a look at this [github](https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_15_2/api/gmsh.py).

## Begginer tutorial

## Our way of using Gmsh

Our situation is as follows:
- We have multiple STL files ready
- We intend to use Firedrake, thus we need to have supported mesh format
- We want the mesh to have differentiated PhysicalGroups of white and grey matter. 

## What we need to know about Gmsh


## Problem with Gmsh geometry/CAD kernels
The problem lays in the presence of different parts of our working pipeline in different kernels. When you load STL (which is boundary representation, so no volumes are present) into Gmsh using **DOPLNIT**, you get elements that live inside the *Built-in kernel*. These can't be interacted with using the *OpenCASCADE kernel*. And so what we have to do is manually build the elements of geometry into OCC and just after that call our favorite function occ.fragment().

When you are using Gmsh, you basically have to decide, whether or not you want to use OpenCASCADE kernel or just a Built-in geometry kernel. There is no common geometrical representation. Operations like translation, rotation and even more advanced ones are always done through a respective CAD kernel.
Said differently: once you create an element inside a Built-in kernel, you can't expect the OCC kernel operations to work on it. This will prove to be a problem for us.


There however is a work-around. We can turn our STL file into a .brep (boundary representation) file. Just after this can we load it into OCC kernel and continue working on it.

### Built-in kernel
Basic geometry kernel, which uses 4 types of model entities based on their topological dimension.
- Points
- Curves
- Surfaces
- Volumes

Element of higher dimension always has a dependence on elements of lower dimension. Erasing a point will lead to destruction of a curve. 

When looking for functions in a Python API, please search for **gmsh.model.geo.something**, for example:
```python
gmsh.model.geo.addPoint(10,10,5,tag=12)
gmsh.model.geo.addPoint(10,10,5,tag=13)
gmsh.model.geo.addLine(startTag=12,endTag=13,tag=4)
```

### OpenCASCADE kernel
This kernel will allow us to do advanced operations when compared to a Built-in kernel. It will also allow us to directly add CAD elements such as Box or BSpline with one simple call of a function. Most important for us is the support of Boolean operations. Since our goal is to create a mesh that consists of parts that represent white and grey matter of a brain, some kind of boolean operation definitely awaits us.

#### Important note
The choice of geometry kernel will change only how your elements are represented inside the machine and how you can work with them. The produced mesh won't be better simply because it was made using a more sophisticated kernel. In Gmsh the meshing itself is a separate part of the process.


### Loading an STL into Gmsh
Before even loading your STL file into Gmsh, please check that it has the qualities needed to continue our process. Namely the most important for us are water tightness of the surface and that edges don't intersect one another.
How to check this is written in a tutorial text on using the MeshLab.

Gmsh has implemented a function that allows us to load STL files into Built-in kernel.
```python
import gmsh

gmsh.initialize()
gmsh.merge("stl/my_model.stl")

node_tags, node_coords, node_param = gmsh.model.mesh.getNodes()
print(f"Number of nodes: {len(node_tags)}")
```
This way we will add elements that are present in the STL file into Gmsh current model. You can see that the function that allows us to see the element tags is inside the gmsh.model.mesh class. That is because they are now presenting a nodes in an actual mesh as well as 