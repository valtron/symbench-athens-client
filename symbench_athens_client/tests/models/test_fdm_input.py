import pytest

from symbench_athens_client.models.fdm_input import FDMInput
from symbench_athens_client.tests.utils import get_test_file_path


class TestFDMInput:
    @pytest.fixture(scope="session")
    def hplane_fdm_input(self):
        return FDMInput.read(get_test_file_path("hplane_input.inp"))

    def test_aircraft_data(self, hplane_fdm_input):
        aircraft_data = hplane_fdm_input.aircraft_data
        assert aircraft_data.cname == "'UAV'"
        assert aircraft_data.ctype == "'SymCPS UAV Design'"
        assert aircraft_data.num_wings == 2
        assert aircraft_data.mass == 2.729888450734746
        assert aircraft_data.x_cm == 46.31692567520146
        assert aircraft_data.y_cm == 0.16496910005986176
        assert aircraft_data.z_cm == -23.405671386550907
        assert aircraft_data.x_fuse == 46.31692567520146
        assert aircraft_data.y_fuse == 0.16496910005986176
        assert aircraft_data.z_fuse == -23.405671386550907
        assert aircraft_data.x_fuseuu == 4160.179274859671
        assert aircraft_data.y_fusevv == 25204.13201711869
        assert aircraft_data.z_fuseww == 31125.170166609518
        assert aircraft_data.i_xx == 127438.8048796813
        assert aircraft_data.i_yy == 660551.4129423498
        assert aircraft_data.i_zz == 782006.8585281011
        assert aircraft_data.i_xy == -789.9455882059922
        assert aircraft_data.i_xz == -6346.200685243803
        assert aircraft_data.i_yz == -9.531424531304378
        assert aircraft_data.uc_initials == [
            "0.4d0, 0.5d0, 0.6d0, 0.7d0",
            "0.5d0, 0.5d0, 0.5d0, 0.5d0",
        ]
        assert aircraft_data.time == "0.d0"
        assert aircraft_data.dt == "1.d-03"
        assert aircraft_data.dt_output == "1.0d0"
        assert aircraft_data.time_end == "1000.d0"
        assert aircraft_data.un_wind == "0.d0"
        assert aircraft_data.ve_wind == "0.d0"
        assert aircraft_data.wd_wind == "0.d0"
        assert aircraft_data.debug == 0
        assert aircraft_data.num_propellers == 5
        assert aircraft_data.num_batteries == 1
        assert aircraft_data.i_analysis_type == 3
        assert (
            aircraft_data.x_initial
            == "0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 1.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0"
        )
