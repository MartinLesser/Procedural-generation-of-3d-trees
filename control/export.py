def export_model_obj(vertex_list, indices, tex_coord):
    """
    Exports the model to the OBJ format. The trunk and branches are exported first and the leafs after that.
    The triangles are listed first with a "v" in the beginning of a line. Then follows the texture coordinates "vt".
    Lastly the indices are listed with a "f" in the beginning then follows the the three indices with a "/" in between
    them e.g. f 23/12/17
    :param vertex_list: List contains one list with all trunk and branches vertices and one list with all leaf vertices
    :param indices: List contains two lists. One list with the trunk/branches indices and one with leaf indices
    :param tex_coord: List contains one list for trunk/branches coordinates and a list for leafs coordinates
    """
    model_vertices = vertex_list[0]
    leafs_vertices = vertex_list[1]
    model_indices = indices[0]
    leafs_indices = indices[1]
    model_coord = tex_coord[0]
    leafs_coord = tex_coord[1]

    fobj = open("../resources/model.obj", "w")
    fobj.write("# Model was created by Martin Lesser\n")
    fobj.write("mtllib tree.mtl\n")
    fobj.write("o tree\n")

    # trunk and branches
    fobj.write("g trunk\n")
    for vertex in model_vertices:
        fobj.write("v "+str(round(vertex[0],6))+" "+str(round(vertex[1],6))+" "+str(round(vertex[2],6))+"\n")
    for coord in model_coord:
        fobj.write("vt "+str(round(coord[0],6))+" "+str(round(coord[1],6))+" "+str(round(coord[2],6))+"\n")
    fobj.write("usemtl bark_seamless\n")
    fobj.write("s 1\n")
    triangles = model_indices[0]
    inverse_triangles = model_indices[1]
    for i in range(0, len(triangles), 3):
        v = str(triangles[i]+1)
        v2 = str(triangles[i+1]+1)
        v3 = str(triangles[i+2]+1)
        fobj.write("f "+v+"/"+str(i+1)+" "+v2+"/"+str(i+2)+" "+v3+"/"+str(i+3)+"\n")
    for i in range(0, len(inverse_triangles), 3):
        v = str(inverse_triangles[i]+1)
        v2 = str(inverse_triangles[i+1]+1)
        v3 = str(inverse_triangles[i+2]+1)
        fobj.write("f "+v+"/"+str(i+len(triangles)+1)+" "+v2+"/"+str(i+len(triangles)+2)+" "+v3+"/"+str(i+len(triangles)+3)+"\n")

    # leafs
    fobj.write("g leafs\n")
    for vertex in leafs_vertices:
        fobj.write("v "+str(round(vertex[0],6))+" "+str(round(vertex[1],6))+" "+str(round(vertex[2],6))+"\n")
    for coord in leafs_coord:
        fobj.write("vt "+str(round(coord[0],6))+" "+str(round(coord[1],6))+" "+str(round(coord[2],6))+"\n")
    fobj.write("usemtl leafs\n")
    fobj.write("s off\n")
    num_trunk_indices = len(model_vertices)
    sum_trunk_coords = len(triangles) + len(inverse_triangles)
    for i in range(0, len(leafs_indices), 3):
        v = str(num_trunk_indices+leafs_indices[i]+1)
        v2 = str(num_trunk_indices+leafs_indices[i+1]+1)
        v3 = str(num_trunk_indices+leafs_indices[i+2]+1)
        fobj.write("f "+v+"/"+str(i+sum_trunk_coords+1)+" "+v2+"/"+str(i+sum_trunk_coords+2)+" "+v3+"/"+str(i+sum_trunk_coords+3)+"\n")

    fobj.close()