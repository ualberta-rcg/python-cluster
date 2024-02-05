---
title: "Arrays"
teaching: 30
exercises: 10
questions:
- "How do I submit many similar jobs?"
objectives:
- "Be able to submit and run array jobs that run python code"
keypoints:
- "Array jobs allow you to run several jobs with a single job script"
---

## Many similar jobs

Writing job scripts isn't exactly the most rewarding experience.
This is particularly true when you are writing many almost identical job scripts.

Luckily Slurm has a solution for this: **job arrays**.

How it works:
* You specify in your script an array of integer indices that you want to use to parameterize some
sub-jobs.
  Some examples:
  ~~~
  #SBATCH --array=0-7
  #SBATCH --array=1,3,5,7
  #SBATCH --array=1-7:2
  #SBATCH --array=1-100%10
  ~~~
  {: .language-bash}
  The second and third examples are the same (the `:2` means "every second number").
  
  The last example means "run at most 10 of them at a given time"
* Your script will run **one time for each index specified**. Each time it runs, the script will have
  access to the environment variable **`$SLURM_ARRAY_TASK_ID`**, which will have the value of the
  index for this specific run.
  
  In the second example above, four sub-jobs are submitted into the
  queue, one will run with `$SLURM_ARRAY_TASK_ID` equal to `1`, another with `$SLURM_ARRAY_TASK_ID`
  equal to `3`, and so on.
* Each sub-job will appear separately in the queue, each with a separate log file.

Job arrays are an excellent way to exploit a kind of parallelism without having to
make your serial program parallel: since multiple jobs can run at the same time, the
net effect is that your multiple serial jobs are running in parallel.

Here is a very basic example of how arrays work, try submitting it:

**`array-basic.sh`**

~~~
#SBATCH --array=1,4,7
#SBATCH --time=00:10:00

echo "I am the job with array task ID $SLURM_ARRAY_TASK_ID"
sleep 60
~~~
{: .language-bash}

## How do I use `$SLURM_ARRAY_TASK_ID` with my python program?

There are a number of ways.

* **Read the `$SLURM_ARRAY_TASK_ID` from the environment.**
  
  The python os module will help with this:
  
  **`array-env.py`**
  ~~~
  import os

  my_array_id = os.environ['SLURM_ARRAY_TASK_ID']

  print('My array task id is', my_array_id, "from the environment")
  ~~~
  {: .language-python}

  **`array-env.sh`**
  ~~~
  #!/bin/bash
  #SBATCH --array=1,4,7
  #SBATCH --time=00:10:00

  module load python/3.11

  python array-env.py
  ~~~
  {: .language-bash}

  Then run: **`sbatch array-env.sh`**

  The drawback here is that now your python script can't be used outside of a job.

* **Pass the `$SLURM_ARRAY_TASK_ID` as a commandline argument to the program.**
  
  Elegent command line argument parsing can be done with the Python `argparse` module,
  but here we will just use the more simple `sys.argv`:

  **`array-arg.py`**
  ~~~
  import sys

  my_array_id = sys.argv[1]

  print('My array task id is', my_array_id, "from an argument")
  ~~~
  {: .language-python}

  **`array-arg.sh`**
  ~~~
  #!/bin/bash
  #SBATCH --array=1,4,7
  #SBATCH --time=00:10:00

  module load python/3.11

  python array-arg.py $SLURM_ARRAY_TASK_ID
  ~~~
  {: .language-bash}

  Then run: **`sbatch array-arg.sh`**

  Now this python script can be used outside of a job.

* **If you don't actually want numbers, you might consider a bash array**

  The python script is the same as previously, but now we can do for the submission
  script

  **`array-bash-array.sh`**
  ~~~
  #!/bin/bash
  #SBATCH --array=0-2
  #SBATCH --time=00:10:00

  module load python/3.11

  things=('dogs' 'cats' 'other things')

  thing=${things[$SLURM_ARRAY_TASK_ID]}

  python array-arg.py "$thing"
  ~~~
  {: .language-bash}

  (Watch the quotes above around the argument!)

  Then run: **`sbatch array-bash-array.sh`**

* **There are many other examples of ways to translate array task ids to meaningful inputs**

   Check out the job array wiki page: <https://docs.alliancecan.ca/wiki/Job_arrays>

> ## Putting it together ...
> Let's write a job script for an array job that does some machine learning, using
> different models on the classic [Titanic data set](https://www.kaggle.com/competitions/titanic)
>
> First we download a script and some data:
>
> ~~~
> wget https://raw.githubusercontent.com/ualberta-rcg/python-cluster/gh-pages/files/titanic.py
> wget https://raw.githubusercontent.com/ualberta-rcg/python-cluster/gh-pages/files/titanic-train.csv
> ~~~
> {: .language-bash}
>
> The `titanic.py` gives an example of using `argparse` for working with commandline arguments.
> In particular, it has a required parameter `--model` to select the model to use. The available options
> are `decision_tree`, `random_forest` and `state_vector_machine`., So for example, we might chose to
> run the program with:
>
> ~~~
> python titanic.py --model random_forest
> ~~~
> {: .language-bash}
>
> This will train a model with the data (reserving 1/3 of the data for testing), and report on the
> accuracy, precision and recall of the model.
>
> Your task is to write an array job that will run all three different models. It should include
> * Loading a python module
> * Create (and activate!) a virtual environment on local disk (`$SLURM_TMPDIR`)
> * Upgrade `pip` and use it to install `pandas`, `numpy`, and `scikit-learn`.
> * Add an `#SBATCH` directive for using a job array
> * use a bash array to translate numbers to model names.
> * run the python script: `python titanic.py ...`
>
> (Tip: copy/paste from the previous example, and the one in the 'jobs' section of this workshop.)
> 
> The jobs run pretty quick, but you might be able to catch them in `squeue`.
> Use `seff` to check out the job performance of each sub-job in the array.
> > ## Solution
> >
> > **`submit-titanic.sh`**
> >
> > ~~~
> > #!/bin/bash
> > #SBATCH --array=0-2
> > #SBATCH --time=00:10:00
> > 
> > module load python/3.11
> > 
> > models=('decision_tree' 'random_forest' 'state_vector_machine')
> > 
> > virtualenv --no-download $SLURM_TMPDIR/venv
> > source $SLURM_TMPDIR/venv/bin/activate
> > pip install --no-index pandas numpy scikit-learn
> > 
> > model=${models[$SLURM_ARRAY_TASK_ID]}
> > 
> > python titanic.py --model "$model"
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

{% include links.md %}
