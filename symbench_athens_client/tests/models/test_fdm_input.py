import pytest

from symbench_athens_client.models.fdm_input import FDMInput
from symbench_athens_client.tests.utils import get_test_file_path


class TestFDMInput:
    @pytest.fixture(scope="session")
    def hplane_fdm_input(self) -> FDMInput:
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

    def test_emp_data(self, hplane_fdm_input):
        emp_data = hplane_fdm_input.emps[0]
        assert emp_data.cname == "'apc_propellers_10x5E'"
        assert emp_data.ctype == "'MR'"
        assert emp_data.prop_fname == "'../../../Tables/PropData/PER3_10x5E.dat'"
        assert emp_data.x == -745.5444084969597
        assert emp_data.y == -340.63999999999993
        assert emp_data.z == -35.56166666666681
        assert emp_data.nx == 0.0
        assert emp_data.ny == -0.0
        assert emp_data.nz == -1.0
        assert emp_data.radius == 127.0
        assert emp_data.ir == 107.52666666666666
        assert emp_data.motor_fname == "'../../Motors/MN3510KV360'"
        assert emp_data.kv == 360.0
        assert emp_data.kt == 0.026525823848649224
        assert emp_data.i_max == 15.0
        assert emp_data.i_idle == 0.4
        assert emp_data.maxpower == 330.0
        assert emp_data.rw == 0.188
        assert emp_data.icontrol == 4
        assert emp_data.ibattery == 1
        assert emp_data.spin == 1

    def test_battery_data(self, hplane_fdm_input):
        battery_data = hplane_fdm_input.batteries[0]
        assert battery_data.num_cells == 6
        assert battery_data.voltage == 22.2
        assert battery_data.capacity == 6000
        assert battery_data.c_continuous == 75
        assert battery_data.c_peak == 150

    def test_wing_data(self, hplane_fdm_input):
        wing_left = hplane_fdm_input.wings[-1]
        assert wing_left.surface_area == 154838.4
        assert wing_left.a == 0.102
        assert wing_left.c_l0 == 0.0102
        assert wing_left.c_lmax == 0.88
        assert wing_left.c_lmin == -0.88
        assert wing_left.c_d0 == 0.0065
        assert wing_left.k == 0.11234476060548583
        assert wing_left.c_dfp == 1
        assert wing_left.bias1 == -0.5
        assert wing_left.bias2 == 0.5
        assert wing_left.icontrol1 == 8
        assert wing_left.icontrol2 == 9
        assert wing_left.tau_a == 0.4
        assert wing_left.x == 1.4210854715202004e-14
        assert wing_left.y == -254.0
        assert wing_left.z == -92.081296
        assert wing_left.nx == 0.0
        assert wing_left.ny == -0.0
        assert wing_left.nz == -1.0

    def test_controls_data(self, hplane_fdm_input):
        control_data = hplane_fdm_input.control
        assert control_data.i_flight_path == 1
        assert control_data.requested_lateral_speed == 16.0
        assert control_data.requested_vertical_speed == 2.0
        assert control_data.i_aileron == 6
        assert control_data.i_flap == 7
        assert control_data.q_position == 1.0
        assert control_data.q_velocity == 1.0
        assert control_data.q_angular_velocity == 1.0
        assert control_data.q_angles == 1.0
        assert control_data.r == 1.0
