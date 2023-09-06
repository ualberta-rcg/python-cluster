---
title: "Running jobs"
teaching: 0
exercises: 0
questions:
- "How do I submit jobs that run python code?"
objectives:
- "Be able to submit and run jobs that run python code"
keypoints:
- "Submit jobs to run long-running or computationally intensive Python code"
---

# Hello world job

Let's write a short program `hello.sh` that says "Hello" from the computer it is run on.


```
import subprocess
print("Hello from ...")
subprocess.run("hostname")
```

We can write a bash script `hello.sh` that runs this program:

```
#!/bin/bash                                                                     

module load python/3.11

python hello.py
```
You can give it a try on the command line:

```
bash hello.sh
```

How it turns out that you could also submit this script as a batch job to Slurm:

```
sbatch hello.sh
```

You can check `squeue` to see if your job is waiting or running (but if it ran and finished, your job
will not appear in the queue).

Check out the output file (something that looks something like `slurm-57.out` to see what happened.

## But ... you really shouldn't do that ...

When you submit a job that way, the scheduler gives your job some default computational resources.
The defaults are pretty wimpy however, and it's ofter better to tell the scheduler exactly what you want.
Common defaults are 1 hour for run time, and 256MB for each CPU core.

We can modify our script to put in some comments, but these comments (all starting with `#SBATCH`)
instruct the scheduler what resources we want for our job:

```
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1000M
#SBATCH --time=00:10:00

module load python/3.11

python hello.py
```

Of note, the memory is requested by core (we only ask for one core though), since
the is often a good way to scale up a program for later. The `M` stands for Megabytes.

## Why so many Megabytes? (When Gigabytes exist as a thing)

The scheduler often reserves some memory for use by the operating system when it
schedules jobs. So if you know that a system has 4 Gigabytes of RAM per core,
then it's better to ask the scheduler for 4000M (Megabytes) than for 4G (Gigabytes).
A Gigabyte is actually 1024 Megabytes.


We can submit this job again with `sbatch hello.sh`. The output won't change in our case, but
being specific with your resource requirements is important for jobs that do serious work.
