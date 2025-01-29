#!/bin/bash

module load python/3.10 cudatoolkit/12.1.1
source ~/scratch/naijavoices-env2/bin/activate

# 1.0.19
python -m pdb analysis4.py