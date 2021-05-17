from flow import FlowProject, aggregator, directives


class Project(FlowProject):
    pass


RANKS_PER_JOB = 2
JOBS_PER_AGGREGATE = 8


@Project.operation
@directives(nranks=lambda *jobs: RANKS_PER_JOB * len(jobs))
@aggregator.groupsof(JOBS_PER_AGGREGATE)
def do_mpi_task(*jobs):
    from mpi4py import MPI

    world_comm = MPI.COMM_WORLD
    world_rank = world_comm.Get_rank()
    world_size = world_comm.Get_size()
    num_jobs = len(jobs)
    if world_rank == 0:
        print(
            f"Launching MPI tasks for {len(jobs)} jobs. Rank {world_rank} of {world_size}."
        )

    # Use MPI splitting to make new communicators
    communicator_size = world_size // num_jobs
    color = world_rank // communicator_size
    key = world_rank % communicator_size
    print(f"{world_rank=}, {color=}, {key=}")

    split_comm = world_comm.Split(color, key)
    split_rank = split_comm.Get_rank()
    split_size = split_comm.Get_size()

    # Select the job from the aggregate to run in the split communicator.
    job = jobs[color]

    print(f"{world_rank=}, {split_rank=}, {split_size=}, {job=}")

    # Now you can use the split communicator with your application!
    # Call your function with job, split_comm


if __name__ == "__main__":
    Project().main()
