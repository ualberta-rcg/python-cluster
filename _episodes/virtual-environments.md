---
title: "Loading Python and Virtual Environments"
teaching: 30
exercises: 10
questions:
- "How do I run python on the cluster?"
- "How do I install python packages?"
objectives:
- "Be able to load a specific version of Python"
- "Be able to create and activate virtual environments"
- "Be able to install packages in a virtual environment"
keypoints:
- "Python is loaded on the cluster through modules"
- "Virtual environments store a version of python and some packages"
- "Package requirements ensure consistency for versions"
---

If you've learned python using Jupyter notebooks, you may have never run python on the
command line or seen a virtual environment before. Quite ofter packages like `pandas` and
`numpy` are "just there" when we use online notebook services like Colab.

On a cluster, we have many options for how we want to run Python. We have a system called
"modules" (or "environment modules", or it's proper name "lmod") that help us choose
which Python version we want to use.
On a cluster, it's our responsibility to ensure that we have the packages we need to
run our Python code.

This is what we will cover in this section.

## Loading Python

When you first log into an HPC cluster, you will have python available to you, but it's rarely the version
you will want.

```
$ python --version
Python 3.7.7
```
{: .language-bash}

Unlike your home computer, the Alliance clusters use a modular software stack that allows you to
choose what version of python you would like to use. To use this stack, most actions are initiated
by the `module` command. The `module load` command, followed by the name of the software you want
(and possibly the version) gives you access to that software. For example, we can load Python 3.11
with:

```
module load python/3.11
```
{: .language-bash}

To find out the available version of python:

```
module spider python
```
{: .language-bash}

Note: the module load command doesn't do any permanent changes to your
account, and the next time you log in things will be the same as before.
You will need to load the python module again if you want to use it.

## Python Packages

Once python is loaded, we need to ensure that we have the packages we need to
run our python code.

We can see if we have the `pandas` package installed by starting up the
Python console:

```
python
```
{: .language-bash}

Now try to import `pandas`:

```
import pandas
```
{: .language-python}

You likely got an error saying that `pandas` couldn't be found
(`Ctrl-D` to exit the console). It's our responsibility to get it.

Virtual environments provide a nice solution to keeping the packages you
need for any particular program isolated from your account and the system
install of python. If you have two different projects that use different
Python versions and different dependencies, no problem: you can
create two different virtual environments that you can turn on of off as
needed. The  tool `pip` is used to install packages that don't come
with the main Python install (`pip` stands for "`pip` installs packages").

Note: on most clusters, the Anaconda distribution of Python is not supported
(nor does it work). If you would like to know why, check out this document:

<https://docs.alliancecan.ca/wiki/Anaconda/en#Do_not_install_Anaconda_on_our_clusters>

You create a virtualenvironment with:

```
virtualenv --no-download venv
```
{: .language-bash}

(Here `venv` is a name for the virtual environment, and will be created on disk as a folder.)

To use a virtual environment, you need to activate it. This is done with

```
source venv/bin/activate
```
{: .language-bash}

Notice how your command prompt now has the name of the virtual environment.
We can now use pip to start downloading packages. The first thing we should do is to upgrade pip.

```
pip install --upgrade pip
```
{: .language-bash}

Later versions of `pip` do a better job of handling package requirements and dependencies,
so this is why this step is important.

## Some important considerations

The above is fine for your own computer, but in general:

* python packages from PyPI aren't optimized for the cluster environment. They might be missing
  parallelization options, or may have been built without vectorization or other optimization
  flags.
* worker nodes on Alliance clusters almost never have access to the internet to reach PyPI.

For this reason, the Alliance has it's own wheelhouse that is accessible to all
cluster nodes and has mostly wheels that were built for clusters. To use this instead of
PyPI, we can use the `--no-index` flag for `pip`, e.g.,

```
pip install --no-index --upgrade pip
pip install --no-index pandas
```
{: .language-bash}

If you neglect to include `--no-index` when installing with `pip` you can run into
real problems where `pip` tries to access PyPI but can't due to lack of internet
access. Your install command might hang forever without completing.

Now start up the Python console and try `import pandas`. Did it work?

To see all of the wheels that are in the Alliance wheelhouse, visit this page:
<https://docs.alliancecan.ca/wiki/Available_Python_wheels>

## A warning

If you don't have a virtual environment enabled, `pip` will attempt to install packages so they
are available to your entire account. This almost always leads to problems, so it is recommended that
you always have a virtual environment activated when you install packages with `pip`.
If you do make the mistake and install in your account, not in a virtual environment,
you can usually find the software installed in the `.local` folder in your home.

There are some environment variables that you can use to prevent this (Google for
`PYTHONNOUSERSITE` or `PIP_REQUIRE_VIRTUALENV` if you are interested).

## pip and versions

You'll notice that when we ran `pip install --no-index pandas`,
we didn't specify a version.

If we want to install a specific version of a package we can do so
by using the package name, double equals signs, and the version number.
By sure to keep all of this inside of quotation marks (I prefer single quotes):

~~~
pip install --no-index 'flask==1.1.2'
~~~
<: .language-bash>

## Checking which packages are installed

This is done with the `pip freeze` command.

```
pip freeze
```
{: .language-bash}
~~~
numpy==1.25.2+computecanada
pandas==2.1.0+computecanada
python-dateutil==2.8.2+computecanada
pytz==2023.3.post1+computecanada
six==1.16.0+computecanada
tzdata==2023.3+computecanada
~~~
{: .output}

## Repeatability through requirements

Sometimes you want to ensure that you use the same versions of your packages each
time you run your python code, on whatever cluster we are running on.

We can use the output from `pip freeze` and send the output to a file
(the convention is to call this file `requirements.txt`, but the file could
be named anything you want):

```
pip freeze > requirements.txt
```
{: .language-bash}
 
Now the next time we create a virtual environment, we can use this file
to populate the packages with the `-r` flag to pip.


```
pip install --no-index -r requirements.txt
```
{: .language-bash}

## Deactivating a virtual environment

When you are done using a virtual environment, or you want to activate a different one, run

```
deactivate
```

Notice how your command prompt changes.

Note: you can't have more than one virtual environment active at a time.

## `requirements.txt` example

Let's create a second virtual environment called `venv2`:

```
module load python/3.11
virtualenv --no-download venv2
source venv2/bin/activate
pip install --upgrade --no-index pip
pip install --no-index -r requirements.txt

# check if it works

deactivate
```
{: .language-bash}

## `scipy-stack`: An alternative to a virtual environment

If you are using some common data science packages, there is a module in the Alliance
software stack that contains many of them: `scipy-stack`.

We can load the `scipy-stack` as follows:

```
module load python/3.11
module load scipy-stack
```
{: .language-bash}

As of this writing, the version of `scipy-stack` that gets loaded is `2023b`.
You can be explicit about this:

```
module load python/3.11
module load scipy-stack/2023b
```
{: .language-bash}

If you would like to know which packages are loaded, check out `module spider scipy-stack/2023b`
or do a `pip freeze` (although you will also see some packages that come with the `python` module).

## Unloading a module

One you've deactivated a virtual environment, you might decide you want to work with a different
version of Python. You can unload the Python module with:

```
module unload python/3.11
```
{: .language-bash}

Note that the following also works:

```
module unload python
```
{: .language-bash}

Sometimes you realize that you want to reset all of the software modules back to the defaults.
One way to do this is to log out and back into the cluster. More efficient though:

```
module reset
```
{: .language-bash}

## Your turn ...

> ## Creating virtual environments
> Now that we have a clean setup (virtual environments are deactivated and modules are reset), 
> try the following on your own:
> * Load Python 3.10
> * Create a virtual environment and activate it (careful to choose a new name or work in a new
>   directory, since we have already used `venv` and `venv2`)
> * Upgrade `pip`
> * Install the packages `dask` and `distributed` (version `1.28.1`).
> * Create a requirements file (e.g., `requirements2.txt`).
> * Deactivate your virtual environment.
> * Create a second virtual environment (and activate it!) and use your requirements file to populate it.
>
> Note: Each previous step should be done to do the next step:
> > ## Solution
> > ~~~
> > # First virtual environment
> > module load python/3.10
> > virtualenv --no-download venv3
> > pip install --no-index --upgrade pip
> > pip install --no-index dask 'distributed==1.28.1'
> > pip freeze > requirements2.txt
> > deactivate
> >
> > # Second virtual environment
> > module load python/3.10
> > virtualenv --no-download venv4
> > pip install --no-index --upgrade pip
> > pip install --no-index -r requirements2.txt
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

{% include links.md %}
