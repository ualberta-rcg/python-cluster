---
title: "Running interactive jobs"
teaching: 0
exercises: 0
questions:
- "How do I run jobs that allow me to interact with my python code?"
- "How do I debug code on an interactive node?"
objectives:
- "Be able to start interactive jobs and run python code"
keypoints:
- "Interactive jobs are a useful way to set up or solve issues with python code on a cluster"
---

## Batch jobs are great, but ...

Batch jobs are great, but you need to implement them correctly before they will work.

It's quite unsatisfying having to run a job just to find out if it will work or not.
This is particularly true if your jobs are experiencing long wait times in the
scheduler queue, just to have a job fail in a few seconds or minutes.

Interactive jobs let you have a better turnaround time while figuring your job out
-- the scheduler gives you the resources you want, and connects you to a terminal session
on the compute node to try things out.

They also give an opportunity to run monitoring tools to see how your program is faring.

## Use `salloc` instead of `sbatch`

Let's take the CPU prime example from an earlier lesson (the GPU example would be great to try,
but we don't have enough GPUs to ensure a reasonable waiting time for all students).

**`submit-cpu.sh`**
~~~
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1000M
#SBATCH --time=00:30:00

module load python/3.11

virtualenv --no-download $SLURM_TMPDIR/venv
source $SLURM_TMPDIR/venv/bin/activate

pip install --no-index --upgrade pip
pip install --no-index numba

python primes_cpu.py
~~~
{: .language-bash}

In this case we would like to get the exact some resources from the scheduler as we did
from the batch job, so we take the values from the "`#SBATCH`" lines and give them
to `salloc` instead:

~~~
salloc --nodes=1 --cpus-per-task=1 --mem-per-cpu=1000M --time=00:30:00
~~~
{: .language-bash}

Now we wait ... the command will appear to hang, but it's just waiting to get the resources
from the scheduler. We will eventually get a command prompt.

From here we can try out the first few lines from the SLURM script, one at a time:

~~~
module load python/3.11
virtualenv --no-download $SLURM_TMPDIR/venv
source $SLURM_TMPDIR/venv/bin/activate
pip install --no-index --upgrade pip
pip install --no-index numba
~~~
{: .language-bash}

Now we get to the part where the prime detection script is run, the one that does the work.
We will force this into the background using `&` at the end of the line:

~~~
python primes_cpu.py &
~~~
{: .language-bash}

(Be careful putting the `&` in your batch scripts: the scheduler often thinks your code
has finished running and the scheduler kills your job.)

We can "see" the program running by using the `jobs` command.

If we want to bring the program to the forefront, get the job id and: 'fg [job id]` (e.g., probably `fg 1`).

We can suspend the program by pressing `Ctrl-Z`. This stops the program from running, but doesn't kill it.

Check `jobs` again to see it and get the job id.

Finally `bg [job id]` (e.g., probably `bg 1`) runs the program in the background.

While the program is running in the background, run the `htop` command (and `htop -u`).

If trying with a GPU node, add `--gres=gpu:1` to you salloc, load the cuda module (`module load cuda`),
and check out what the gpu is doing with `nvidia-smi`.
