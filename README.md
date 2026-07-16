# mesh-creation
Description of mesh creation workflow. This repository contains example scripts showing how to turn MRI images into computational mesh. 

This repository consists of example scripts and also readable tutorials focusing mainly on description of steps, that are needed to do,
in order to turn MRI images into computational mesh files.


In order to do this one needs to use the following:
- FreeSurfer
- SVMTK 
- MeshLab
- GMSH

In this workflow, there are many problematic moments, which we try overcome.

***

If you have a STL file and want to turn it into a computational mesh, you can start with MeshLab step.


## How to use this repository

A tutorial text presented in a directory ***doplnit*** is divided into files, which one can think of as chapters in a novel.
The steps come one after another and can not be ommited.
Together with this text, example scripts are presented. They always present one small step. Even though we try to use comments in code to make
it readable, additional ideas are presented in tutorial text. 



## Used software and useful links
- For working with MRI images and segmentation of the brain, we use [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)
- For working with brain segments, we use [SVMTK](https://github.com/SVMTK/SVMTK)
- For working with STL files, we use [MeshLab](https://www.meshlab.net/)
- For creating the computational mesh itself, we use [GMSH](https://gmsh.info/) 
