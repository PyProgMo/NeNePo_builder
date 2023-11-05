#!/bin/bash

sbatch --array=0-49%50 zekecalc.sub
mkdir collectslurm
