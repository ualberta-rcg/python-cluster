---
title: "Running a notebook in a JupyterHub"
teaching: 20
exercises: 0
questions:
- "How do I run a notebook in a JupyterHub?"
- "How do I load specific software in a JupyterHub notebook"
objectives:
- "Be able to run a notebook in a JupyterHub"
keypoints:
- "Most Alliance clusters have a JupyterHub"
---

# Jupyter Notebooks

It's quite likely that you have used Jupyter notebooks in the past.
They can be a convenient way to test ideas and construct new code.
While Jupyter notebooks aren't the preferred choice for executing
long-running code on a cluster (mostly because they are interactive
in nature), they can be an important part of your development pipeline.

# JupyterHub

A JupyterHub is a way to allow multiple users to access Jupyter notebooks (and other applications)
in a way so that each user gets their own isolated environment. This has some similarity to
Google's cloud-based Colab service.

Your instructor will give you the URL for the JupyterHub login page (usually putting the address of the
training cluster into the URL bar of your browser will get you there).

Production Alliance clusters will have 'jupyterhub' in the front of the cluster name, e.g.,

* <https://jupyterhub.cedar.computecanada.ca>
* <https://jupyterhub.narval.computecanada.ca>
* <https://jupyterhub.beluga.computecanada.ca>
* <https://jupyterhub.graham.computecanada.ca>

Once you have arrived at the JupyterHub page, you can log in with the same username
and password used to log into the cluster via SSH.

![Jupyter server options page]({{ page.root }}/fig/jupyterhub-sign-in.png){: width="200" }

You are now given a page with some options to select some resources, much like a
Slurm submission script.

![Jupyter server options page]({{ page.root }}/fig/jupyterhub-server-options.png){: width="400" }

For the most part, we can keep the defaults to get a single core and some memory
for an hour. Of particular note is the "JupyterLab" user interface option: Jupyter is
a powerful way to run one-or-more notebooks or other applications.

Press "Start". It may take a few moments for an interface to show up.

![JupyterLab]({{ page.root }}/fig/jupyterhub-jupyterlab.png){: width="400" }

On the left side, there is a vertical stack of icons for some general activities:

* File browser (filefolder)
* Running Terminals and Kernels (circle square)
* GPU dashboard
* Table of Contents
* Software
* Extension Manager

## You can start a new launcher with the `+` tab button

Most operations make the launcher disappear, but you can open a new one with the `+` button

## You can start a terminal ...

This gives you a terminal session, just like as if you used SSH to access to cluster.
The drawback here is that you are doing this through the scheduler, and this way
will deplete your priority for running jobs (using SSH to access the cluster will
**never** deplete your priority.

## Picking a specific Python version

Select `Python 3 (ipykernel)` from a launcher.

In the notebook, you can find the current python version a couple of ways:

~~~
import sys
sys.version_info
~~~
{: .language-python}

or

~~~
!python --version
~~~
{: .language-python}

You can use a specific python version by visiting the software screen (hexagon icon) and
loading the module `ipython-kernel/3.11` (for example).

Now on the launcher, the notebook icon says `Python 3.11`.

In your running notebook, you can now switch python versions through the `Kernel`
menu (`Change Kernel`). This will wipe clean any program you are currently running
in the notebook.

Rerun the version code again.

## Python scripts as modules

We can load (and run) our prime calculating code ...

~~~
import primes_cpu
primes_cpu.main()
~~~
{: .language-python}

Another example:

~~~
!pip install --no-index pandas scikit-learn numpy
~~~
{: .language-python}

(You may need to restart the kernel first ... You may also need to change directories with `cd`).

~~~
import titanic
titanic.main('random_forest')
~~~
{: .language-python}

## Some other programs you can access

Some of these don't work great on our test cluster, but you have access
to some programs by loading other software modules ...
After loading the module, press the `+` on the tab bar to get a new launcher,
you will new icons.

* RStudio: e.g., `rstudio-server/4.3`
* OpenRefine: e.g., `openrefine/3.4.1`
* MS Code Server: `code-server/3.12.0`

## Quit

Go to `File` menu and select `Logout`.