# Freesurfer
In this chapter, we cover the first part of the process of turning MRI image into a computational mesh.

## We will do
1. Obtain a MRI image
1. Do a segmentation 
1. Turn these segments into STL files
1. Know how to use command line

## We will need 


## BrainWeb: Simulated Brain Database
BrainWeb is a database of MRI images, that was developed at the McConnell Brain Imaging Center (McBIC) at the Montreal Neurological Institute (MNI). It allows us to obtain simulated images with parameters decided by us.

The database can be accessed through their [website](https://brainweb.bic.mni.mcgill.ca/).
Here one can choose from two databases of brain images:
- Normal Brain Database
- MS Lesion Brain Database

You can decide which one to use based on your needs or interests. We will proceed by choosing Normal Brain Database in this text.

Once selected, you are met with a choice of multiple parameter settings. We want to avoid unnecessary problems and thus we *Noise* and *Intensity non-uniformity ("RF")* as small as possible. Choice of *Modality* depends on your needs. If you want to have a clear contrast between white and grey matter, choose **T1-weighted image**.  

### Data type
The data you obtain from BrainWeb database are in the **MINC (.mnc)** format. This format was developed at the McConnell Brain Imaging Center (McBIC) at the Montreal Neurological Institute (MNI). 

This is important, because FreeSurfer can't work with this format and so we need to turn the data into one of the standard formats used in medical imaging.

Tools used for conversion of data types are available [here](https://brainweb.bic.mni.mcgill.ca/about_data_formats.html) on their website. Further information about the MINC format and working with it are also available.

Standard size of a compressed MINC file from BrainWeb database with a thickess chosen as 1mm is around 8 MB. Once turned into **NIfTI (.nii)** format, expect around 28 MB.


## FreeSurfer: MRI processing

FreeSurfer is an open-source software, that we will use for segmentation of brain parts from our MRI image.

One can find it on their [website](https://surfer.nmr.mgh.harvard.edu/). To download FreeSurfer on Ubuntu, please, visit [downloads](https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads) part of their website.
Note that only Ubuntu20 and Ubuntu22 are supported and you can run into problems when using more recent versions.

If the file you downloaded looks like this *freesurfer.tar.gz*, it is a compressed archive and you have to unpack it. To do so, use this command:

`tar -zxvpf freesurfer.tar.gz`

Perfect, now that we have installed FreeSurfer, we can move on to the next step and configure the environment for using it. If your archive has been unpacked at */home/myself/freesurfer*, you have to add the following lines to the end of a file named **.bashrc** in your home directory.

```bash
export FREESURFER_HOME =/ home /me/ freesurfer
export SUBJECTS_DIR = $FREESURFER_HOME / subjects
source $FREESURFER_HOME / SetUpFreeSurfer .sh
```

Please note that to use FreeSurfer, you have to acquire a free license. To obtain it, [register](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) on their website.

In order to use FreeSurfer for segmenting our MRI, we have to install one more requirement: *tcsh* (specific type of Unix shell).
To install it use the following command lines in your terminal.
```bash
$ sudo apt update
$ sudo apt install tcsh
```

This was the final step of our setting up. We are now ready to turn MRI into STL. In other words we are ready to start using FreeSurfer.

We suggest creating a folder called *subjects*, where one can store all of the MRI data needed.

Following steps await us:
1. Create surfaces from MRI data
3. Generate Volume-mesh under these surfaces


### Creating surfaces from T1-weighted MRI 

We are about to generate surfaces that represent for example the interface between white and grey matter. 

We will use FreeSurfer command `recon-all`. Note that this command has likely run times of up to 24 hours. This command also asks to decide on subject identifier. That is what the folder with all of the generated data will be called. One can use for example *sub001*.

This folder will be created in SUBJECTS_DIR you have chosen during setting up the environment. In other words the output of `recon-all` will be stored in */SUBJECTS_DIR/sub001/*

To run `recon-all` please do the following:
- Move into the directory, where your BrainWeb MRI is located
- Decide on subject identifier

```bash
$ cd path/to/mri
$ recon-all -subjid sub001 -i brainT1_1mm_clean -all
```
Note that *-subjid* sets the folder name, *-i* chooses the input file and your file name can vary, and finally *-all* tells FreeSurfer to run the entire cortical reconstruction pipeline.

After segmentation, the folder *sub001* will have approximately 380 MB.


### Notes on the problematic parts, that book does no talk about

The following section heavily depends on whether your are using FEniCS or Firedrake for your FEM calculations. That is because there are differences in supported mesh file formats.

This leads us to the biggest problem and that is SVMTk does not support generating meshes in a format that is useful for Firedrake. That is why we have to use GMSH to create our mesh.