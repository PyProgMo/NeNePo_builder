#!/bin/bash

sbatch --array=0-39%40 zekecalc.sub
mkdir collectslurm
