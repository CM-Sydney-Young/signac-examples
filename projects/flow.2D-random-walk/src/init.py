#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories.
"""
import logging

import numpy as np
import signac

logger = logging.getLogger()
# Decrease logging level to WARN or lower for output
logger.setLevel(logging.ERROR)

# The different standard deviations to use for generating moves in the random
# walk
STANDARD_DEVIATIONS = np.linspace(start=0.1, stop=1, num=20)
NUMBER_REPLICAS = 100
RUN_STEPS = 5_000
MAX_SEED = 2 ** 32 - 1


def main():
    """Initialize signac project."""
    project = signac.init_project("2D Gaussian Random Walk")
    for replica in range(NUMBER_REPLICAS):
        for std in STANDARD_DEVIATIONS:
            seed = np.random.randint(MAX_SEED)
            statepoint = {
                "mean": 0,
                "standard_deviation": std,
                "replica": replica,
                "seed": seed,
            }

            job = project.open_job(statepoint)
            job.doc.run_steps = RUN_STEPS

            logger.warn(f"Initializing job with state point: {statepoint}.")
            job.init()


if __name__ == "__main__":
    main()
