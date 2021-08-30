from typing import ClassVar, List

from pydantic import BaseModel, Field


class FDMInputField(BaseModel):
    """The fdm input class"""

    __input_file_prefix__: ClassVar[str] = None

    comment: str = Field("", description="The comment string", alias="Comment")


class EMPInput(FDMInputField):
    __input_file_prefix__: ClassVar[str] = "propeller"

    number: int = Field(
        ...,
        description="The number this Propeller input section gets assigned",
        alias="",
    )

    comment: int = Field(
        ...,
    )

    prop_fname: str = Field(
        ..., description="The Performance filename for the propeller"
    )

    x: float = Field(
        ..., description="The x-coordinates of the center of the propeller"
    )

    y: float = Field(
        ..., description="The y-coordinates of the center of the propeller"
    )

    z: float = Field(
        ..., description="The x-coordinates of the center of the propeller"
    )

    nx: float = Field(..., description="X-Vector of propeller orientation")

    ny: float = Field(..., description="Y-Vector of propeller orientation")

    nz: float = Field(..., description="Z-vector of propeller orientation")

    radius: float = Field(..., description="The radius of the propeller")


class WingInput(FDMInputField):
    """The wing input fields."""

    __input_file_prefix__: ClassVar[str] = "wing"

    surface_area: float = Field(
        ..., description="The surface area of the wing", alias="surface_area"
    )

    a: float = Field(..., description="The a field", alias="a")

    c_l0: float = Field(..., description="The c_l0 parameter", alias="C_L0")

    c_lmax: float = Field(..., description="The C_LMax", alias="C_LMax")

    c_d0: float = Field(..., description="C_D0", alias="C_D0")

    k: float = Field(..., description="k", alias="k")

    c_dfp: float = Field(..., description="C_Dfp", alias="C_Dfp")

    bias1: float = Field(..., description="Bias1", alias="bias_1")

    bias2: float = Field(..., description="Bias2", alias="bias_2")

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

    x_fuseuu: float = Field(..., description="The x-fuseuu parameter", alias="x_fuseuu")

    y_fusevv: float = Field(..., description="The y-fusevv parameter", alias="y_fusevv")

    z_fuseww: float = Field(..., description="The x-fuseww parameter", alias="z_fuseww")

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


class BatteryInputs(AircraftInput):
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


class ControlInputs(FDMInputField):
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

    i_aileron: int = Field(..., description="The iaileron", alias="i_aileron")

    i_flap: int = Field(..., description="The iflap", alias="i_flap")

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
        alias="Q_angluar_velocity",
    )

    q_angles: float = Field(..., description="The Q-Angles parameter", alias="Q_angles")

    r: float = Field(..., description="The R parameter in LQR controller", alias="R")
