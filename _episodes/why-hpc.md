---
title: "Why run Python on a cluster?"
teaching: 5
exercises: 0
questions:
- "When would I run on a cluster?"
objectives:
- "Understand when running on a cluster is worth it, and when it isn't"
keypoints:
- "Make sure the effort needed to run on a cluster isn't too high"
---

## Some ways to run Python

* You can use cloud-based Jupyter notebooks
* You can run Python on your own machine and either run scripts or Jupyter notebooks
* You could run Python on an HPC cluster

## When shouldn't you run on a cluster?

* When you are interested in running very few, fairly short jobs. The overhead
  and effort of running on a cluster may not be work it if these jobs require modest
  computational resources
* When you don't feel comfortable using (or learning) Linux based tools (although stick around:
  because many HPC clusters provide access to a JupyterHub for interactive work).

## Times when running on a cluster makes sense

* When you have a program that takes a really long time to complete (e.g., days)
* When you need to run the same program dozens or hundreds of times, with different parameters
  (e.g., a parameter sweep)
* You are reaching the limit of what either your laptop or cloud-based tools will allow in
  terms of computational power, e.g., maybe your program can use multiple CPUs, or can
  be accellerated with an expensive GPU, or maybe it needs more memory that what you currently
  have access to.
* You need access to more storage than is available to you on your laptop or cloud-based
  solutions.

{% include links.md %}
