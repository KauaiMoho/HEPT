#!/bin/sh
#SBATCH --job-name=TRAIN_TRACKING_ODD #Job name
#SBATCH --mail-type=FAIL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=kluitel@purdue.edu # Where to send mail	
#SBATCH --account=cms
#SBATCH --output=/home/kluitel/HEPT/src/slurm_output/train_tracking_odd-%A.out	# Name output file 

#SBATCH -N 1
#SBATCH -n 20
#SBATCH --time=04:00:00

module load anaconda

echo "Running on $(hostname)"
echo "Working dir: $(pwd)"
date

mydir=/home/kluitel/HEPT/src/
cd $mydir
conda run -n HEPT_env python tracking_trainer.py --model odd