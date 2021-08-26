#!/usr/bin/env python3
"""
FDM Experiments Optimizer


This script tries to find optimal parameter assignments for FDM experiments
(i.e.) for designs for which we already we have a trained/fitted CAD
approximator.
"""
import argparse
import csv
import logging
import sys
from csv import DictWriter
from itertools import product
from math import exp
from multiprocessing import Pool

import numpy as np

from symbench_athens_client.fdm_experiments import (
    get_experiment_by_name,
    get_experiments,
)

# There's a get_logger function in symbench_athens_client.utils (If so desired)
log = logging.getLogger("fdm_optimizer")


# Question>> Instead of hopelessly searching for the whole range, why don't we start from the point
# that gives us the best score so far and slide left and right based the baseline base result?

param_sweeps = {
    "arm_length": np.linspace(300, 600, 10),
    "support_length": np.linspace(1, 30, 5),
    "batt_mount_x_offset": [0],
    "batt_mount_z_offset": np.linspace(10, 50, 10),
    "q_position": [1.0],
    "q_angles": [1.0],
    "q_velocity": [1.0],
    "q_angular_velocity": [1.0],
    "r": np.geomspace(10.0, 1000.0, 10),
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
    score = 0.0

    while reqs[req_lateral_speed] <= max_lateral_speed:
        result = experiment.run_for(
            params, reqs, change_dir=True, write_to_output_csv=False
        )
        max_lateral_speed = result["Max_Speed"]  # shorten this loop
        score = result["TotalPathScore"]
        if score > best_score:
            best_score = score
            best_reqs = reqs.copy()
        reqs[req_lateral_speed] += 1

        # These file operations seem too expensive, we might have to consider an
        # alternative (Maybe generate output.csv later)
        # should_write_header = False
        # if not (experiment.results_dir / "output.csv").exists():
        #     should_write_header = True
        #
        # with open(experiment.results_dir / "output.csv", "a", newline="") as csv_file:
        #     op_writer = csv.DictWriter(csv_file, fieldnames=result.keys())
        #     if should_write_header:
        #         op_writer.writeheader()
        #     op_writer.writerow(result)

    return score, best_reqs


def results_logger(params, writer, output_file):
    def write_and_log(results):
        nonlocal params
        nonlocal writer
        nonlocal output_file

        best_score, best_reqs = results

        log.info(f"best score for {params}: {best_score} at {best_reqs}")
        writer.writerow({"score": best_score, **params, **best_reqs})
        output_file.flush()

    return write_and_log


def error_logger(error):
    log.error(error)


def optimize(
    experiment, min_lateral_speed, vertical_speed, output_file, num_processes=1
):
    """Find the best parameters for the given experiment"""
    assert req_lateral_speed in experiment.valid_requirements
    assert req_vertical_speed in experiment.valid_requirements

    param_names = list(set(param_sweeps.keys()) & set(experiment.valid_parameters))

    writer = DictWriter(
        output_file,
        ["score"] + param_names + [req_lateral_speed, req_vertical_speed],
    )
    writer.writeheader()
    if num_processes == 1:
        for param_values in product(*[param_sweeps[p] for p in param_names]):
            params = dict(zip(param_names, param_values))
            best_score, best_reqs = get_best_score(
                experiment, params, min_lateral_speed, vertical_speed
            )
            log_func = results_logger(params, writer, output_file)
            log_func((best_score, best_reqs))
    else:
        pool = Pool(num_processes)

        count = 0
        for param_values in product(*[param_sweeps[p] for p in param_names]):
            params = dict(zip(param_names, param_values))
            log.debug(
                f"Started for {params}, 'lateral_speed': {min_lateral_speed}, 'vertical_speed': {vertical_speed}"
            )

            pool.apply_async(
                get_best_score,
                kwds={
                    "experiment": experiment,
                    "params": params,
                    "min_lateral_speed": min_lateral_speed,
                    "vertical_speed": vertical_speed,
                },
                callback=results_logger(params, writer, output_file),
                error_callback=error_logger,
            )

            # ToDo: Remove test code
            count += 1
            if count == 1000:
                break

        pool.close()
        pool.join()


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
    parser.add_argument(
        "-n",
        "--num-processes",
        help="The number of process pools to use. Default is 1 or don't use.",
        type=int,
        default=1,
    )
    args = parser.parse_args()

    if args.list:
        print("\n".join(get_experiments()))
        sys.exit(0)

    if args.verbose:
        log.setLevel(logging.DEBUG)

    experiment_names = get_experiments()
    if args.experiment:
        if args.experiment not in experiment_names:
            log.error(f"experiment {args.experiment} is not available")
            sys.exit(-1)
        experiment_name = args.experiment
    else:
        experiment_name = experiment_names[0]

    experiment = get_experiment_by_name(experiment_name)
    experiment.start_new_session()

    if args.output is None:
        args.output = f"{experiment.results_dir}/{experiment_name}_best_results.csv"

    # if Path(args.output).exists():
    #     # better not to automatically overwrite these valuable files
    #     log.error(f"output file already exists: {args.output}")
    #     sys.exit(-1)

    log.info(f"saving results to : {args.output}")

    with open(args.output, "w", newline="") as output_file:
        optimize(
            experiment,
            args.min_speed,
            args.vertical_speed,
            output_file,
            num_processes=args.num_processes,
        )


if __name__ == "__main__":
    main()
