#!/usr/bin/env python
"""Generate CSV files (one per component type) from the database"""
from symbench_athens_client.models.components import (
    Battery,
    ComponentsBuilder,
    Motor,
    Propeller,
    Wing,
    get_all_components_of_class,
)

if __name__ == "__main__":

    for cls in Battery, Motor, Propeller, Wing:
        builder = ComponentsBuilder(cls, get_all_components_of_class(Battery))
        builder.to_csv(f"{cls.__name__}.csv")
