# mesh-creation
Description of mesh creation workflow. This repository contains example scripts showing how to turn MRI images into computational mesh. 

This repository consists of example scripts and also readable tutorials focusing mainly on description of steps, that are needed to do,
in order to turn MRI images into computational mesh files.


In order to do this, one needs to use the following:
- FreeSurfer
- SVMTK 
- MeshLab
- GMSH

In this workflow, there are many problematic parts, which we try overcome.

***
NOTE:
If you have a STL file and want to turn it into a computational mesh, you can start with MeshLab step.


## How to use this repository

A tutorial text presented in a directory ***tutorial-text*** is divided into files, which one can think of as chapters in a novel.
The steps come one after another and can not be omitted.
Together with this text, example scripts are presented. Each code example focuses on demonstrating a single feature or functionality of the library we need.

Code examples contain a vast amount of comments, if you want to get rid of them to copy clean code, you can do that by means of a littl cleaning script offered in the repository.


## Used software and useful links
- For working with MRI images and segmentation of the brain, we use [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/)
- For working with brain segments, we use [SVMTK](https://github.com/SVMTK/SVMTK)
- For working with STL files, we use [MeshLab](https://www.meshlab.net/)
- For creating the computational mesh itself, we use [GMSH](https://gmsh.info/), precisely the  [Python](https://www.python.org/) API
