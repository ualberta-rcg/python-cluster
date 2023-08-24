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

```
import subprocess
print("Hello from ...")
subprocess.run("hostname")
```

```
#!/bin/bash                                                                     

module load python/3.11

python hello.py
```

## You really shouldn't do that ...

The defaults are pretty wimpy, and it's ofter better to tell
the scheduler exactly what you want.

```
#!/bin/bash                                                                     

#SBATCH --nodes=1                                                               
#SBATCH --tasks-per-node=1                                                      
#SBATCH --cpus-per-task=1                                                       
#SBATCH --mem-per-cpu=4000M                                                     
#SBATCH --time=00:10:00                                                         

module load python/3.11

python hello.py
```
