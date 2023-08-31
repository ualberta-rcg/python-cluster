---
title: "Virtual environments"
teaching: 0
exercises: 0
questions:
- "How do I install python packages?"
objectives:
- "Be able to create and activate virtual environments"
- "Be able to install packages in a virtual environment"
keypoints:
- "Virtual environments store a version of python and somepackages"
---

## Loading Python

When you first log into an HPC cluster, you will have python available to you, but it's rarely the version
you will want.

```
$ python --version
Python 3.7.7
```

Unlike your home computer, the Alliance clusters use a modular software stack that allows you to
choose what version of python you would like to use. To use this stack, most actions are initiated
by the `module` command. The `module load` command, followed by the name of the software you want
(and possibly the version) gives you access to that software. For example, we can load Python 3.11
with:

```
module load python/3.11
```

To find out the available version of python:

```
module spider python
```

Note: the module load command doesn't do any permanent changes to your
account, and the next time you log in things will be the same as before.
You will need to load the python module again if you want to use it.

Once python is loaded, you can create a virtual environment, which will give you access to packages
you've downloaded with pip.

You create a virtualenvironment with:

```
virtualenv --no-download venv
```
(Here `venv` is a name for the virtual environment, and will be created on disk as a folder.)

To use a virtual environment, you need to activate it. This is done with

```
source venv/bin/activate
```

We can now use pip to start downloading packages. The first thing we should do is to upgrade pip.

```
pip install --upgrade pip
```

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

To see all of the wheels that are in the Alliance wheelhouse, visit this page:
https://docs.alliancecan.ca/wiki/Available_Python_wheels

## A warning

If you don't have a virtual environment enabled, `pip` will attempt to install packages so they
are available to your entire account. This almost always leads to problems, so it is recommended that
you always have a virtual environment activated when you install packages with `pip`.

## Deactivating a virtual environment

When you are done using a virtual environment, or you want to activate a different one, run

```
deactivate
```

Note: you can't have more than one virtual environment active at a time.

## Unloading a module

One you've deactivated a virtual environment, you might decide you want to work with a different
version of Python. You can unload the Python module with:

```
module unload python/3.11
```

Note that the following also works:

```
module unload python
```

Sometimes you realize that you want to reset all of the software modules back to the defaults.
One way to do this is to log out and back into the cluster. More efficient though:

```
module reset
```
