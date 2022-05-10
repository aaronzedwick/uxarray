import xarray as xr


def _read_ugrid(filepath, ugrid_vars):
    """UGRID file reader.

    Parameters: string, required
        Name of file to be read

    Returns: the xarray Dataset loaded during init.
    """

    # TODO: obtain and change to Mesh2 construct, see Issue #27
    # simply return the xarray object loaded

    xr_ds = xr.open_dataset(filepath, mask_and_scale=False)

    #
    base_dv_mt = list(xr_ds.filter_by_attrs(cf_role="mesh_topology").keys())[0]

    ugrid_vars["Mesh2"] = base_dv_mt

    coord_names = xr_ds[base_dv_mt].node_coordinates.split()

    if len(coord_names) == 1:
        ugrid_vars["Mesh2_node_x"] = coord_names[0]
    elif len(coord_names) == 2:
        ugrid_vars["Mesh2_node_x"] = coord_names[0]
        ugrid_vars["Mesh2_node_y"] = coord_names[1]
    elif len(coord_names) == 3:
        ugrid_vars["Mesh2_node_x"] = coord_names[0]
        ugrid_vars["Mesh2_node_y"] = coord_names[1]
        ugrid_vars["Mesh2_node_z"] = coord_names[2]

    # set #nodes use x coordinates, y or z will be the same and can also be used
    coord_dim_name = xr_ds[ugrid_vars["Mesh2_node_x"]].dims
    ugrid_vars["nMesh2_node"] = coord_dim_name[0]

    face_node_names = xr_ds[base_dv_mt].face_node_connectivity.split()

    face_node_name = face_node_names[0]
    ugrid_vars["Mesh2_face_nodes"] = xr_ds[face_node_name].name
    ugrid_vars["nMesh2_face"] = xr_ds[face_node_name].dims[0]
    ugrid_vars["nMaxMesh2_face_nodes"] = xr_ds[face_node_name].dims[1]

    return xr_ds


# Write a uxgrid to a file with specified format.
def _write_ugrid(ds, outfile, ugrid_vars):
    """UGRID file writer.
    Parameters
    ----------
    ds : xarray.Dataset
        Dataset to be written to file
    outfile : string, required
        Name of output file

    Uses to_netcdf from xarray object.
    """

    print("Writing ugrid file: ", outfile)
    ds.to_netcdf(outfile)
