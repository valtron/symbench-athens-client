from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field


class ComponentsNotFoundException(Exception):
    pass


class ComponentNotFoundException(Exception):
    pass


class FDMInputField(BaseModel):
    """The fdm input fields class."""

    __input_file_prefix__: ClassVar[str] = None

    number: Optional[int] = Field(
        None, description="The number(count) for this input field"
    )

    comment: str = Field(default="", description="The comment string", alias="Comment")

    @classmethod
    def from_input_lines(
        cls, lines: List[str], number: Optional[int] = None
    ) -> "FDMInputField":
        if number is None:
            fields = {
                cls.__input_file_prefix__ + "%" + field.alias: name
                for name, field in cls.__fields__.items()
            }
        else:
            fields = {
                cls.__input_file_prefix__ + f"({number})%" + field.alias: name
                for name, field in cls.__fields__.items()
            }
        cls_dict = {"number": number}

        for line in lines:
            splitted = line.split("=", maxsplit=1)
            field_key = splitted[0].strip()
            if field_key in fields:
                value_and_comment = splitted[-1].split("!")

                if cls_dict.get(fields[field_key]):
                    if not isinstance(cls_dict.get(fields[field_key]), list):
                        cls_dict[fields[field_key]] = [cls_dict[fields[field_key]]]
                    cls_dict[fields[field_key]].append(value_and_comment[0].strip())
                else:
                    cls_dict[fields[field_key]] = value_and_comment[0].strip()

        return cls(**cls_dict)

    class Config:
        allow_population_by_field_name = True


class EMPInput(FDMInputField):
    """The input fields for propellers, motors and ESC."""

    __input_file_prefix__: ClassVar[str] = "propeller"

    cname: str = Field(..., description="The cname of the propeller", alias="cname")

    ctype: str = Field(..., description="The ctype of the propeller", alias="ctype")

    prop_fname: str = Field(
        ...,
        description="The Performance filename for the propeller",
        alias="prop_fname",
    )

    x: float = Field(
        ..., description="The x-coordinates of the center of the propeller", alias="x"
    )

    y: float = Field(
        ..., description="The y-coordinates of the center of the propeller", alias="y"
    )

    z: float = Field(
        ..., description="The x-coordinates of the center of the propeller", alias="z"
    )

    nx: float = Field(..., description="X-Vector of propeller orientation", alias="nx")

    ny: float = Field(..., description="Y-Vector of propeller orientation", alias="ny")

    nz: float = Field(..., description="Z-vector of propeller orientation", alias="nz")

    radius: float = Field(
        ..., description="The radius of the propeller", alias="radius"
    )

    ir: float = Field(..., description="The Ir parameter", alias="Ir")

    motor_fname: str = Field(..., description="The motor filename", alias="motor_fname")

    kv: float = Field(..., description="The motor kv", alias="KV")

    kt: float = Field(..., description="The motor kt", alias="KT")

    i_max: float = Field(..., description="I_max", alias="I_max")

    i_idle: float = Field(..., description="I_idle", alias="I_idle")

    maxpower: float = Field(..., description="maxpower", alias="maxpower")

    rw: float = Field(..., description="Rw", alias="Rw")

    icontrol: int = Field(..., description="icontrol", alias="icontrol")

    ibattery: int = Field(..., description="ibattery", alias="ibattery")

    spin: int = Field(..., description="spin", alias="spin")


class WingInput(FDMInputField):
    """The wing input fields."""

    __input_file_prefix__: ClassVar[str] = "wing"

    surface_area: float = Field(
        ..., description="The surface area of the wing", alias="surface_area"
    )

    a: float = Field(..., description="The a field", alias="a")

    c_l0: float = Field(..., description="The c_l0 parameter", alias="C_L0")

    c_lmax: float = Field(..., description="The C_LMax", alias="C_Lmax")

    c_lmin: float = Field(..., description="The C_LMin", alias="C_Lmin")

    c_d0: float = Field(..., description="C_D0", alias="C_D0")

    k: float = Field(..., description="k", alias="k")

    c_dfp: float = Field(..., description="C_Dfp", alias="C_Dfp")

    bias1: float = Field(..., description="Bias1", alias="bias1")

    bias2: float = Field(..., description="Bias2", alias="bias2")

    icontrol1: int = Field(..., description="icontrol1", alias="icontrol1")

    icontrol2: int = Field(..., description="icontrol1", alias="icontrol2")

    tau_a: float = Field(..., description="Tau_a", alias="tau_a")

    x: float = Field(..., description="x", alias="x")

    y: float = Field(..., description="y", alias="y")

    z: float = Field(..., description="z", alias="z")

    nx: float = Field(..., description="nx", alias="nx")

    ny: float = Field(..., description="ny", alias="ny")

    nz: float = Field(..., description="nz", alias="nz")


class AircraftInput(FDMInputField):
    """Aircraft input fields"""

    __input_file_prefix__: ClassVar[str] = "aircraft"

    cname: str = Field(..., description="The name of the aircraft", alias="cname")

    ctype: str = Field(..., description="The ctype of the aircraft", alias="ctype")

    num_wings: int = Field(
        ..., description="The number of wings in the aircraft", alias="num_wings"
    )

    mass: float = Field(..., description="The mass of the aircraft", alias="mass")

    x_cm: float = Field(
        ..., description="The x-coordinates of the center of mass", alias="x_cm"
    )

    y_cm: float = Field(
        ..., description="The y-coordinates of the center of mass", alias="y_cm"
    )

    z_cm: float = Field(
        ..., description="The z-coordinates of the center of mass", alias="z_cm"
    )

    x_fuse: float = Field(..., description="The x-fuse parameter", alias="x_fuse")

    y_fuse: float = Field(..., description="The y-fuse parameter", alias="y_fuse")

    z_fuse: float = Field(..., description="The z-fuse parameter", alias="z_fuse")

    x_fuseuu: float = Field(..., description="The x-fuseuu parameter", alias="X_fuseuu")

    y_fusevv: float = Field(..., description="The y-fusevv parameter", alias="Y_fusevv")

    z_fuseww: float = Field(..., description="The x-fuseww parameter", alias="Z_fuseww")

    i_xx: float = Field(..., description="The Ixx parameter", alias="Ixx")

    i_yy: float = Field(..., description="The Iyy parameter", alias="Iyy")

    i_zz: float = Field(..., description="The Izz parameter", alias="Izz")

    i_xy: float = Field(..., description="The Ixy parameter", alias="Ixy")

    i_xz: float = Field(..., description="The Ixz parameter", alias="Ixz")

    i_yz: float = Field(..., description="The Iyz parameter", alias="Iyz")

    uc_initials: List[str] = Field(
        ..., description="The uc-initial conditions", alias="uc_initial"
    )

    time: str = Field(..., description="The time parameter", alias="time")

    dt: str = Field(..., description="The dt parameter", alias="dt")

    dt_output: str = Field(
        ..., description="The time between two output lines", alias="dt_output"
    )

    time_end: str = Field(..., description="The end time", alias="time_end")

    un_wind: str = Field(
        ..., description="The north wind speed in world frame", alias="Unwind"
    )

    ve_wind: str = Field(
        ..., description="The east wind speed in world frame", alias="Vewind"
    )

    wd_wind: str = Field(
        ..., description="The down wind speed in world frame", alias="Wdwind"
    )

    debug: int = Field(..., description="Verbose print outs to dferiv", alias="debug")

    num_propellers: int = Field(
        ..., description="The number of propellers", alias="num_propellers"
    )

    num_batteries: int = Field(
        ..., description="The number of batteries", alias="num_batteries"
    )

    i_analysis_type: int = Field(
        ..., description="The analysis type", alias="i_analysis_type"
    )

    x_initial: str = Field(description="The X-initial parameter", alias="x_initial")


class BatteryInput(FDMInputField):
    """Battery input fields"""

    __input_file_prefix__ = "battery"

    num_cells: int = Field(
        ..., description="The number of cells in the battery", alias="num_cells"
    )

    voltage: float = Field(
        ..., description="The voltage rating of the battery", alias="voltage"
    )

    capacity: float = Field(
        ..., description="The capacity of the battery", alias="capacity"
    )

    c_continuous: float = Field(
        ..., description="The continuous current of the battery", alias="C_Continuous"
    )

    c_peak: float = Field(
        ..., description="The peak current of the battery", alias="C_Peak"
    )


class ControlInput(FDMInputField):
    """Control input fields"""

    __input_file_prefix__: ClassVar[str] = "control"

    i_flight_path: int = Field(
        ..., description="The flight path", alias="i_flight_path"
    )

    requested_lateral_speed: float = Field(
        ..., description="The requested lateral speed", alias="requested_lateral_speed"
    )

    requested_vertical_speed: float = Field(
        ..., description="The requested lateral speed", alias="requested_vertical_speed"
    )

    i_aileron: int = Field(..., description="The iaileron", alias="iaileron")

    i_flap: int = Field(..., description="The iflap", alias="iflap")

    q_position: float = Field(
        ...,
        description="The Q-Position of the LQR controller",
        alias="Q_position",
    )

    q_velocity: float = Field(
        ..., description="The Q-Velocity of the LQR controller", alias="Q_velocity"
    )

    q_angular_velocity: float = Field(
        ...,
        description="The Q-Angular velocity of the LQR controller",
        alias="Q_angular_velocity",
    )

    q_angles: float = Field(..., description="The Q-Angles parameter", alias="Q_angles")

    r: float = Field(..., description="The R parameter in LQR controller", alias="R")


class FDMInput(BaseModel):
    aircraft_data: AircraftInput = Field(
        ..., description="The aircraft inputs", alias="aircraft_data"
    )

    emps: List[EMPInput] = Field(..., description="The EMP inputs", alias="emps")

    batteries: List[BatteryInput] = Field(
        ..., description="The battery inputs", alias="batteries"
    )

    wings: List[WingInput] = Field(..., description="The wing inputs", alias="wings")

    control: ControlInput = Field(
        ..., description="The control inputs", alias="control"
    )

    @property
    def start(self):
        return "&aircraft_data"

    @property
    def end(self):
        return "/\n"

    @classmethod
    def read(cls, input_file):
        with open(input_file, "r") as fdm_input_file:
            input_lines = fdm_input_file.readlines()
            aircraft_data = AircraftInput.from_input_lines(input_lines)
            control = ControlInput.from_input_lines(input_lines)
            batteries = []
            wings = []
            emps = []

            num_batteries = aircraft_data.num_batteries
            num_propellers = aircraft_data.num_propellers
            num_wings = aircraft_data.num_wings

            for i in range(num_batteries):
                batteries.append(BatteryInput.from_input_lines(input_lines, i + 1))

            for i in range(num_wings):
                wings.append(WingInput.from_input_lines(input_lines, i + 1))

            for i in range(num_propellers):
                emps.append(EMPInput.from_input_lines(input_lines, i + 1))

            return cls(
                aircraft_data=aircraft_data,
                emps=emps,
                batteries=batteries,
                wings=wings,
                control=control,
            )

    class Config:
        arbitrary_types_allowed = True
