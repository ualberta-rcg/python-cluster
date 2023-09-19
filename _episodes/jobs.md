---
title: "Running jobs"
teaching: 30
exercises: 10
questions:
- "How do I submit jobs that run python code?"
- "How do I ensure that my python job has the packages it needs?"
- "How do I get better input/output performance?"
- "How do I use a GPU with my code?"
objectives:
- "Be able to submit and run jobs that run python code"
- "Be able to create virtual environments to install packages in a job"
- "Create a virtual environment on local disk"
- "Run a code on a GPU"
keypoints:
- "Submit jobs to run long-running or computationally intensive Python code"
- "Create virtual environments and install packages from the Alliance wheelhouse"
- "Working with local disk in a job can provide performance benefits"
- "You can use the scheduler to ask for a GPU to run code on"
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

Now it turns out that you could also submit this script as a batch job to Slurm:

```
sbatch hello.sh
```

## The queue

You can check your jobs that are in the queue with:

```
squeue -u $USER
```

On the regular Alliance clusters, there is a shorthand command:

```
sq
```

Only queued (pending) and running jobs will be shown, so if your job has finished running you
won't see it in the queue

To see all of the jobs in the queue, you can run `squeue`.

## Output

Check out the output file (something that looks something like `slurm-57.out`) to see what
happened with your job. Hopefully such a file exists and it has a hostname in the output.

## But you really shouldn't submit jobs this way ...

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
this is often a good way to scale up a program for later. The `M` stands for Megabytes.

## Why so many Megabytes? (When Gigabytes exist as a thing)

The scheduler often reserves some memory for each core for use by the operating system when
it schedules jobs. If you ask for all of the memory for a core, the scheduler needs a little
bit of memory from somewhere else (another core), and as a result your priority will be impacted
as if you used an additional core.
So if you know that a system has 4 Gigabytes of RAM per core,
then it's better to ask the scheduler for 4000M (Megabytes) than for 4G (Gigabytes).
A Gigabyte is actually 1024 Megabytes, and the difference in memory can be used by Slurm to
service operating requests.

We can submit this job again with `sbatch hello.sh`. The output won't change in our case, but
being specific with your resource requirements is important for jobs that do serious work.

## Accounting ...

We have glossed over the fact that there is an "account" being used for deciding the priority of
your job. In the case of the training cluster, everybody has one account `def-sponsor00`.

In real life situtations, it's quite possible that you might have access to more than one account
on a cluster (e.g., `def-sponsor00` and `rrg-sponsor00`). In which case you'll need to specify
which account to use either in the script, or on the commandline. (I often prefer the later method).

In the script, add the line:

```
#SBATCH --account=def=sponsor00
```

On the commandline, submit with the following command:

```
sbatch --account=def-sponsor00 hello.sh
```

## The speed of storage matters

Most cluster users will know the three main filesystems on a cluster:

* `home`
* `scratch`
* `project`

Each of these filesystems are on disk that is connected to the computers you are using
over a network. In general, networked disk is slower than local disk (when the disk is connected
to the computer you are using), but in order for all of the computers in the cluster to access
these filesystems, a network needs to be involved.

The situation is worse than this. Unlike the disk in your laptop, on the cluster there might
be hundreds of users all using the same filesystem at the same time. This makes the disk
performance issue even worse.

Performance issues are particularly noticable in situations where many files are read/written to.
It is better to do a few big writes to a few files than it is to do many little writes to a
lot of files.

The Alliance clusters have a solution for this: reserving a piece of local disk on each cluster
compute node for fast Input/Output operations. When using the Slurm scheduler, this disk can
be accessed through an environment variable called `$SLURM_TMPDIR`.

**The good:**

* Using `$SLURM_TMPDIR` can greatly speed up your calculations that involve a lot of reading/writing
to disk.
* While `$SLURM_TMPDIR` is physically restricted in size, it is often large enough for most
purposes, and there are no quotas involved (for example, on the shared filesystems there are
quotas that restrict the number of files that can be created).

**The bad:**

* `$SLURM_TMPDIR` only exists while you are running a job. It disappears after the job is done and
all of the files are deleted. It is thus very important that you copy in and copy out any files
you need or create during the running of the job before the job ends. This includes the situation
when you have an error that kills your job: your files on `$SLURM_TMPDIR` will vanish, which makes it
difficult to debug things.
* `$SLURM_TMPDIR` is only on the computer you are running on, and there isn't access to it over the
network. So if your job involves multiple computers, it's likely that `$SLURM_TMPDIR` won't be a good
fit (there are cases where you can make things work though).

## Virtual environments are a collection of many files ...

When you assemble a virtual environment, you are usually creating a large colletion of Python files.

**Because of this, it is highly recommended that you create your virtual environments on local disk**

This is what it looks like:

```
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1000M
#SBATCH --time=00:10:00

module load python/3.11

virtualenv --no-download $SLURM_TMPDIR/venv
source $SLURM_TMPDIR/venv/bin/activate
pip install --no-index pandas
# Install any other packages you need here

python hello.py
```

Note that compute nodes don't have access to the internet to grab
packages from PyPI, so it's really important to add the `--no-index`
flag to pip.

## An exercise using GPUs

GPUs (Graphical Processing Units) can speed up a number of different kinds of codes in a
number of different domains (Machine Learning being a hot example right now).

Your code must be especially written to use the GPU, usually using a library that
does most of the low-level work.

Most programs and libraries that use one or more GPUs on the Alliance clusters use a special
library called CUDA (written by NVIDIA) to interface with the GPU card.

There is a Python package called Numba (rhymes with "rhumba", sounds kinda like "number")
that can use a GPU card.

To run a GPU job, you basically need three things:

1. **You need to request a GPU from the scheduler.**
   
   You may want to request a specific type of
   GPU, but the most generic way to make such a request is to add a line to your batch script
   that looks like:
   
   ```#SBATCH --gres=gpu:1```
   
   This tells the scheduler "give me one GPU, I don't care what kind".
   If the type of GPU is of concern to you, check out the options on the Alliance GPU page:
   <https://docs.alliancecan.ca/wiki/Using_GPUs_with_Slurm>

2. **You need to load the CUDA modules.**
   
   Just like with loading the Python module, we can load CUDA with:

   ```module load cuda```
   
   This will allow your software to find the CUDA libraries. You can run
   `module spider cuda` to find out what versions of CUDA are available.

3. **You need to load a package in your virtual environment that uses the GPU.**

   In this case, we will use `pip` to install `numba` in our virtual environment.

4. **Your Python script must be written to use such a library.**
   
   Writing code for the GPU is beyond the scope of this course so we will download
   one. You can get the script by running:

   ~~~
   wget ...
   ~~~

   The script `primes.py` we've downloaded computes all of the prime numbers that are less than
   5,000,000.

> ## Putting it together ...
> Let's put things together to write a job script that runs this GPU code. Some features of this
> script:
> * Ask Slurm for a GPU (above)
> * Load both the `python` and `cuda` modules.
> * Create a virtual environment on local disk of the node you are running on,
>   activate it, upgrade `pip`, and use `pip` to install `numba`
> * Run the python script
>
> When the job is done, check the output file, and run `seff [jobid]` to see
> some performance information.
> > ## Solution
> > ~~~
> > #!/bin/bash
> >
> > #SBATCH --nodes=1
> > #SBATCH --tasks-per-node=1
> > #SBATCH --cpus-per-task=1
> > #SBATCH --mem-per-cpu=1000M
> > #SBATCH --time=00:10:00
> > #SBATCH --gres=gpu:1
> >
> > module load python/3.11 cuda
> >
> > virtualenv --no-download $SLURM_TMPDIR/venv
> > source $SLURM_TMPDIR/venv/bin/activate
> >
> > pip install --no-index --upgrade pip
> > pip install --no-index numba
> >
> > python primes.py
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

{% include links.md %}
