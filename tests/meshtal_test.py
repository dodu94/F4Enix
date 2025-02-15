import os
import re
import pytest
import pyvista as pv
from importlib.resources import files, as_file

from f4enix.output.meshtal import Meshtal
import tests.resources.meshtal as resources
import tests.resources.meshtal.tests as res
import tests.resources.meshtal.expected as res_exp

resources_write = files(res)
expected = files(res_exp)
RESOURCES = files(resources)


class TestMeshtal:
    def test_thetest(self):
        assert True

    @pytest.mark.parametrize("input_meshtal",
                             ["meshtal_cuv",
                              "meshtal_cyl",
                              "meshtal_d1s_CSimpactStudy",
                              "meshtal_CUBE_SQUARE",
                              "meshtal_CUBE_ONES"])
    def test_mesh_print_tally_info(self, input_meshtal):
        # To check if the meshtal can be read without any problem"
        filetype = "MCNP"
        with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
            meshtally = Meshtal(inp, filetype)

        for i in meshtally.mesh.items():
            meshtally.mesh[i[0]].print_info()

        assert True

    def test_same_mesh(self):
        with as_file(RESOURCES.joinpath('meshtal_CUBE_SQUARE')) as inp:
            meshtally = Meshtal(inp)
        meshtally.readMesh()
        assert meshtally.mesh[124].sameMesh(meshtally.mesh[124])

    @pytest.mark.parametrize(
        "input_meshtal",
        [
            "meshtal_cuv",
            "meshtal_cyl",
            "meshtal_d1s_CSimpactStudy",
            "meshtal_CUBE_SQUARE",
            "meshtal_CUBE_ONES",
        ],
    )
    def test_read_mesh(self, input_meshtal):
        # To check if the meshtal can be read without any problem"
        filetype = "MCNP"
        with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
            meshtally = Meshtal(inp, filetype)

        for i in meshtally.mesh.items():
            meshtally.readMesh()

        assert True

    @pytest.mark.parametrize(
        "norm",
        [
            "vtot",
            "celf",
        ],
    )
    def test_read_mesh_cuv(self, norm):
        # To check if the meshtal can be read without any problem"
        filetype = "MCNP"
        with as_file(RESOURCES.joinpath('meshtal_cuv')) as inp:
            meshtally = Meshtal(inp, filetype)

        for i in meshtally.mesh.items():
            meshtally.readMesh(norm=norm)
            meshtally.readMesh(cell_filters=[1, 2], norm=norm)

        assert True

    @pytest.mark.parametrize(
        "input_meshtal",
        ["meshtal_cuv", "meshtal_cyl", "meshtal_d1s_CSimpactStudy"]
    )
    def test_mesh_print_info(self, input_meshtal):
        # To check if the meshtal can be read without any problem"
        filetype = "MCNP"
        with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
            meshtally = Meshtal(inp, filetype)

        for i in meshtally.mesh.items():
            meshtally.print_info()

        assert True

    def test_write_cyl(self, tmpdir):
        with as_file(RESOURCES.joinpath('meshtal_cyl')) as inp:
            meshtally = Meshtal(inp)
        meshtally.readMesh()
        outpath = tmpdir.mkdir('sub_cyl')
        meshtally.mesh[124].write(outpath)

    @pytest.mark.parametrize(
            ['file_read', 'list_array_names', 'out_format', 'out_name', 'file_exp'],
            [['example.vts', None, 'csv', 'meshtal_cyl_124_csv.csv', "example_['Values']_csv.csv"],
             ['test_VTK_CUBE_SQUARE.vtr', ["Value - Total"], 'csv', 'meshtal_cyl_124_csv.csv', "test_VTK_CUBE_SQUARE_['Value - Total']_csv.csv"],
             ['meshtal_14.vts', ["Value - Total"], 'csv', 'meshtal_cyl_124_csv.csv', "meshtal_14_['Value - Total']_csv.csv"],
             ['cuvmsh_44_CuV_CELF10.vtr', ["Value - Total"], 'csv', 'meshtal_cyl_124_csv.csv', "cuvmsh_44_CuV_CELF10_['Value - Total']_csv.csv"],
             ['PS_NHD_DIV_RHC_INBOARD.vtk', ["NHD[W/cm3]"], 'csv', 'meshtal_cyl_124_csv.csv', "PS_NHD_DIV_RHC_INBOARD_['NHD[W-cm3]']_csv.csv"],
             ['PS_NHD_DIV_RHC_INBOARD.vtk', ["NHD[W/cm3]"], 'ip_fluent', 'meshtal_cyl_124_ip_fluent.txt', "PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_ip_fluent.txt"],
             ['PS_NHD_DIV_RHC_INBOARD.vtk', ["NHD[W/cm3]"], 'point_cloud', 'meshtal_cyl_124_point_cloud.txt', "PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_point_cloud.txt"]
            ]
            )
    def test_write(self, file_read, list_array_names, out_format, out_name,
                   file_exp, tmpdir):
        # Whatever mesh can be read here, the grid will be overridden
        with as_file(RESOURCES.joinpath('meshtal_cyl')) as inp:
            meshtally = Meshtal(inp)
        meshtally.readMesh()
        fmesh = meshtally.mesh[124]

        with as_file(resources_write.joinpath(file_read)) as inp:
            fmesh._read_from_vtk(inp)

        outpath = tmpdir.mkdir('sub_csv')
        fmesh.write(outpath, out_format=out_format,
                    list_array_names=list_array_names)
        outfile = os.path.join(outpath, out_name)

        with as_file(expected.joinpath(file_exp)) as exp:
            with open(outfile, "r") as test, open(exp, 'r') as exp_file:
                for line1, line2 in zip(test, exp_file):
                    assert line1 == line2

        # Also always test the .vtk writing
        fmesh.write(outpath)

    @pytest.mark.parametrize("input_meshtal",
                             ['meshtal_cuv', 'meshtal_cyl',
                              'meshtal_d1s_CSimpactStudy',
                              'meshtal_d1s_IVVS_FDR',
                              'meshtal_rect_VV'])
    def test_reading(self, input_meshtal):
        # To check if the meshtal can be read without any problem"
        filetype = 'MCNP'
        with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
            Meshtal(inp, filetype)

        assert True
    
    def test_write_all(self, tmpdir):
        with as_file(RESOURCES.joinpath('meshtal_cyl')) as inp:
            meshtally = Meshtal(inp)
        meshtally.readMesh()
        meshtally.write_all(tmpdir)

# ************** STATUS OF TESTING *****************
# Mesh scale               (scale)      ---> DONE
# Mesh sum                 (sum)        ---> DONE
# Mesh difference          (diff)       ---> DONE
# Energy bin sum           (binsum)     ---> PENDING
# Check identical mesh     (identical)  ---> DONE
# Change correlation       (corr)       ---> DONE
# CuV testing                           ---> PENDING

# 'meshtal_CUBE_SQUARE'
#  ^
#  |   9  16
#  |   1  4
#  Y
#     X --->

# 'meshtal_CUBE_ONES'
#  ^
#  |   1  1
#  |   1  1
#  Y
#     X --->


# @pytest.mark.parametrize("input_meshtal",
#                          ["meshtal_CUBE_SQUARE",
#                           'meshtal_rect_VV',
#                           'meshtal_cyl',
#                           'meshtal_d1s_CSimpactStudy'])
# def test_mesh_VTKwrite(input_meshtal, tmpdir):
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
#         meshtally = Meshtal(inp, filetype)

#     # get the first mesh
#     mesh_key = list(meshtally.mesh.keys())[0]
#     meshtally.mesh[mesh_key].print_info()
#     meshtally.readMesh([mesh_key])
#     meshobj = meshtally.mesh[mesh_key]

#     outpath = tmpdir.mkdir('sub_cube')

#     meshobj.writeVTK(outpath)
#     assert True


# @pytest.mark.parametrize("input_meshtal",
#                          ["meshtal_CUBE_SQUARE",
#                           'meshtal_rect_VV',
#                           'meshtal_cyl',
#                           'meshtal_d1s_CSimpactStudy'])
# def test_mesh_VTKwrite(input_meshtal, tmpdir):
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath(input_meshtal)) as inp:
#         meshtally = Meshtal(inp, filetype)

#     # read all meshes
#     meshtally.readMesh()
#     outpath = tmpdir.mkdir('sub_write_all')
#     meshtally.writeVTK(outpath)

#     assert True


# @pytest.mark.parametrize("filename", ["test_VTK_CUBE_SQUARE.vtr"])
# def test_mesh_VTKcheck(filename):
#     with as_file(RESOURCES.joinpath(filename)) as inp:
#         mesh = pv.read(inp)

#     assert mesh["Value - Total"][0] == 1
#     assert mesh["Value - Total"][1] == 9
#     assert mesh["Value - Total"][2] == 4
#     assert mesh["Value - Total"][3] == 16


# @pytest.mark.parametrize("sfactor", [1, 2, 3, 10, 20])
# def test_mesh_scale(sfactor):
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath("meshtal_CUBE_SQUARE")) as inp:
#         meshtally = Meshtal(inp, filetype)
#     meshtally.readMesh([124])
#     meshobj = meshtally.mesh[124]

#     smesh = scalemesh(meshobj, sfactor)

#     assert smesh.dat[0][0][0][0] == 1 * sfactor
#     assert smesh.dat[0][0][0][1] == 9 * sfactor
#     assert smesh.dat[0][0][1][0] == 4 * sfactor
#     assert smesh.dat[0][0][1][1] == 16 * sfactor


# def test_mesh_sum():
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath("meshtal_CUBE_SQUARE")) as inp:
#         meshtally = Meshtal(inp, filetype)

#     meshtally.readMesh([124])
#     meshobj = meshtally.mesh[124]

#     smesh = addmesh(meshobj, meshobj, f1=1.0, f2=1.0, corr=False)

#     assert smesh.dat[0][0][0][0] == 1 * 2
#     assert smesh.dat[0][0][0][1] == 9 * 2
#     assert smesh.dat[0][0][1][0] == 4 * 2
#     assert smesh.dat[0][0][1][1] == 16 * 2


# def test_mesh_corr():
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath("meshtal_CUBE_ONES")) as inp:
#         meshtally = Meshtal(inp, filetype)

#     meshtally.readMesh([124])
#     meshobj = meshtally.mesh[124]

#     smesh = addmesh(meshobj, meshobj, f1=1.0, f2=1.0, corr=True)

#     assert smesh.err[0][0][0][0] == 1
#     assert smesh.err[0][0][0][1] == 1
#     assert smesh.err[0][0][1][0] == 1
#     assert smesh.err[0][0][1][1] == 1

#     smesh = addmesh(meshobj, meshobj, f1=1.0, f2=1.0, corr=False)

#     assert smesh.err[0][0][0][0] == ((1 + 1) ** 0.5) / 2
#     assert smesh.err[0][0][0][1] == ((1 + 1) ** 0.5) / 2
#     assert smesh.err[0][0][1][0] == ((1 + 1) ** 0.5) / 2
#     assert smesh.err[0][0][1][1] == ((1 + 1) ** 0.5) / 2


# def test_mesh_diff():

#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath("meshtal_CUBE_SQUARE")) as inp:
#         meshtally = Meshtal(inp, filetype)

#     meshtally.readMesh([124])
#     meshobj = meshtally.mesh[124]

#     smesh = diffmesh(meshobj, meshobj)

#     assert smesh.dat[0][0][0][0] == 0
#     assert smesh.dat[0][0][0][1] == 0
#     assert smesh.dat[0][0][1][0] == 0
#     assert smesh.dat[0][0][1][1] == 0


# def test_mesh_identical():
#     filetype = "MCNP"
#     with as_file(RESOURCES.joinpath("meshtal_CUBE_SQUARE")) as inp:
#         meshtally = Meshtal(inp, filetype)

#     meshtally.readMesh([124])
#     meshobj = meshtally.mesh[124]

#     part, mesh, mtype = identical_mesh(meshobj, meshobj)

#     assert part is True
#     assert mesh is True
#     assert mtype is True



