'''In this example code file we merge two STL files: of a snowman and of a top hat. We process them and
generate STEP files, which we then use to generate a mesh ready for calculations.'''

import gmsh
import numpy as np

def write_model_info(filename="model_info.txt"):
    '''
    Utility function to extract and write diagnostic information about the current Gmsh model into a formated text file.
    '''
    with open(filename,"w") as f:
        def write(text=""):
            print(text)
            f.write(text + "\n")

        write("="*70)
        write("GMSH MODEL INFORMATION")
        write("="*70)

        # GEOMETRY INFORMATION
        write("GEOMETRY")
        points = gmsh.model.occ.getEntities(dim=0) 
        curves = gmsh.model.occ.getEntities(dim=1) 
        surfaces = gmsh.model.occ.getEntities(dim=2) 
        volumes = gmsh.model.occ.getEntities(dim=3) 
        
        write(f"Number of points : {len(points)}") 
        write(f"Number of curves : {len(curves)}") 
        write(f"Number of surfaces : {len(surfaces)}") 
        write(f"Number of volumes : {len(volumes)}") 
        write()

        # BOUNDING BOX
        write("BOUNDING BOX")
        # Bounding box of the entire OCC model
        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(dim = -1,tag = -1)

        dx = xmax - xmin 
        dy = ymax - ymin 
        dz = zmax - zmin

        center_x = (xmin+xmax) / 2
        center_y = (ymin+ymax) / 2
        center_z = (zmin+zmax) / 2

        write(f"X min : {xmin:.8g}") 
        write(f"X max : {xmax:.8g}") 
        write(f"Y min : {ymin:.8g}") 
        write(f"Y max : {ymax:.8g}") 
        write(f"Z min : {zmin:.8g}") 
        write(f"Z max : {zmax:.8g}") 
        write()

        write(f"X dimension : {dx:.8g}") 
        write(f"Y dimension : {dy:.8g}") 
        write(f"Z dimension : {dz:.8g}") 
        write()

        write("Bounding box center:") 
        write(f" X : {center_x:.8g}") 
        write(f" Y : {center_y:.8g}") 
        write(f" Z : {center_z:.8g}") 
        write()

        write("MESH")
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes() 
        number_of_nodes = len(node_tags) 
        write(f"Number of mesh nodes : {number_of_nodes}")
        write()

def stl_to_step(stl_file,model_name):
    '''
    Core pipeline function that loads an STL file, recostructs the geometry in OCC kernel, 
    builds a bounded 3D volume and exports to STEP.
    '''
    gmsh.clear()

    
    gmsh.merge(stl_file)

    node_tags, node_coords, node_param = gmsh.model.mesh.getNodes()
    print(f"Number of nodes: {len(node_tags)}")
    node_coords_triplets = node_coords.reshape(-1,3)

    elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
    print("Element types:", elem_types)

    elem_node_tags = np.array(elem_node_tags)  #turn into numpy array to use reshape
    elem_node_tags_triplets = elem_node_tags.reshape(-1,3)   #we assume the STL contains only triangles, so we make triplets

    for coord,ntag in zip(node_coords_triplets,node_tags):        
        gmsh.model.occ.addPoint(*coord, tag=ntag)


    def make_key(A,B):
        return tuple(sorted((A,B)))

    line_tags_dict = {}
    line_tags_list = []
    for line_tags in elem_node_tags_triplets:
        edges = [[line_tags[0],line_tags[1]],[line_tags[1],line_tags[2]],[line_tags[2],line_tags[0]]]
        for edge in edges:
            key = make_key(edge[0],edge[1])
            if key in line_tags_dict:
                line_tags_list.append(line_tags_dict[key])
            else:
                new_key = gmsh.model.occ.addLine(*key)
                line_tags_list.append(new_key)
                line_tags_dict[key] = new_key

    line_tags_list = np.array(line_tags_list)
    line_tags_list_triplets = line_tags_list.reshape(-1,3)
    print(f"Is line_tags_list divisible by 3?: {len(line_tags_list)%3}")

    curves_list = []
    for sides in line_tags_list_triplets:
        curves_list.append(gmsh.model.occ.addCurveLoop(sides))    
    print(f"Lenght of curves_list: {len(curves_list)}")

    surfaces_list = []
    step = 0
    for loop in curves_list:
        surfaces_list.append(gmsh.model.occ.addPlaneSurface([loop]))
        step +=1
        if step%1000==0:
            print(step)
    print(f"Number of surfaces: {len(surfaces_list)=}")
    ## We have created OCC representation of all triangles that were inside the STL. We now have to turn them all into 
    ## a surface loop. That creates a shell, that will be used as a boundary for creation of a volume.
    print("Now making surface loop")
    final_loop = gmsh.model.occ.addSurfaceLoop(surfaceTags=surfaces_list)
    print(f"Finished making surface loop with tag: {final_loop}")

    volume = gmsh.model.occ.addVolume([final_loop])    
    print(f"Created a volume with tag: {volume}")

    print(f"Number of 0D entities: {len(gmsh.model.occ.getEntities(dim=0))}")
    print(f"Number of 1D entities: {len(gmsh.model.occ.getEntities(dim=1))}")
    print(f"Number of 2D entities: {len(gmsh.model.occ.getEntities(dim=2))}")
    print(f"Number of 3D entities: {len(gmsh.model.occ.getEntities(dim=3))}")

    gmsh.model.occ.synchronize()
    
    print(f"Writing into {model_name}.step")
    gmsh.write(f"step_files/{model_name}.step")

    write_model_info(filename=f"{model_name}.txt")
    

gmsh.initialize()
stl_to_step(stl_file="stl_files/snowman_parts.stl", model_name="snowman")
stl_to_step(stl_file="stl_files/tophat.stl", model_name="tophat")
gmsh.finalize()