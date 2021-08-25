#!/usr/bin/env python3
"""
FDM Experiments Optimizer


This script tries to find optimal parameter assignments for FDM experiments
(i.e.) for designs for which we already we have a trained/fitted CAD
approximator.
"""
from math import exp
import sys
import argparse
import logging
from itertools import product
from pathlib import Path
from csv import DictWriter

import numpy as np
from symbench_athens_client import fdm_experiments
from symbench_athens_client.fdm_experiment import FlightDynamicsExperiment

log = logging.getLogger("fdm_optimizer")

param_sweeps = {
    "arm_length": np.linspace(180, 600, 10),
    "support_length": np.linspace(10, 100, 5),
    "batt_mount_x_offset": np.linspace(-20, 20, 10),
    "batt_mount_z_offset": np.linspace(-20, 20, 10),
    "q_position": [1.0],
    "q_angles": [1.0],
    "q_velocity": [1.0],
    "q_angular_velocity": [1.0],
    "r": np.geomspace(0.1, 100.0, 10),
}

req_lateral_speed = "requested_lateral_speed"
req_vertical_speed = "requested_vertical_speed"


def get_best_score(experiment, params, min_lateral_speed, vertical_speed):
    """Find the best score with a design point (trying to fly the fastest)"""
    best_score = 0
    best_reqs = reqs = {
        req_lateral_speed: min_lateral_speed,
        req_vertical_speed: vertical_speed,
    }
    max_lateral_speed = 50

    while reqs[req_lateral_speed] <= max_lateral_speed:
        result = experiment.run_for(params, reqs)
        max_lateral_speed = result["Max_Speed"]  # shorten this loop
        score = result["TotalPathScore"]
        if score > best_score:
            best_score = score
            best_reqs = reqs.copy()
        reqs[req_lateral_speed] += 1

    return score, best_reqs


def optimize(experiment, min_lateral_speed, vertical_speed, output_file):
    """Find the best parameters for the given experiment"""

    assert req_lateral_speed in experiment.valid_requirements
    assert req_vertical_speed in experiment.valid_requirements

    param_names = list(
        set(param_sweeps.keys()) & set(experiment.valid_parameters)
    )

    writer = DictWriter(
        output_file,
        ["score"] + param_names + [req_lateral_speed, req_vertical_speed],
    )
    writer.writeheader()

    for param_values in product(*[param_sweeps[p] for p in param_names]):
        params = dict(zip(param_names, param_values))

        best_score, best_reqs = get_best_score(
            experiment, params, min_lateral_speed, vertical_speed
        )
        log.info(f"best score for {params}: {best_score} at {best_reqs}")
        writer.writerow({"score": best_score, **params, **best_reqs})
        output_file.flush()


def main():
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--experiment", help="experiment to optimize")
    parser.add_argument("-o", "--output", help="output CSV file name")
    parser.add_argument(
        "-l", "--list", action="store_true", help="list available experiments"
    )
    parser.add_argument(
        "-m", "--min-speed", help="minimum lateral speed", default=35, type=int
    )
    parser.add_argument(
        "--vertical-speed",
        help="vertical speed for lift & hover",
        default=-2.0,
        type=float,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    args = parser.parse_args()

    experiments = {}
    for name in dir(fdm_experiments):
        obj = getattr(fdm_experiments, name)
        if type(obj) == FlightDynamicsExperiment:
            experiments[name] = obj

    if args.list:
        print("\n".join(list(experiments.keys())))
        sys.exit(0)

    if args.verbose:
        log.setLevel(logging.DEBUG)

    experiment_names = list(experiments.keys())
    experiment_name = experiment_names[0]
    if args.experiment:
        if args.experiment not in experiment_names:
            log.error(f"experiment {args.experiment} is not available")
            sys.exit(-1)
        else:
            experiment_name = args.experiment

    if args.output is None:
        args.output = f"{experiment_name}_opt.csv"

    # if Path(args.output).exists():
    #     # better not to automatically overwrite these valuable files
    #     log.error(f"output file already exists: {args.output}")
    #     sys.exit(-1)

    log.info(f"saving results to : {args.output}")

    with open(args.output, "w", newline="") as output_file:
        optimize(
            experiments[experiment_name],
            args.min_speed,
            args.vertical_speed,
            output_file,
        )


if __name__ == "__main__":
    main()
