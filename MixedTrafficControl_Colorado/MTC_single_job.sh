#!/bin/sh
#SBATCH --job-name=MTC_test    # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liusongyang@ufl.edu   # Where to send mail	
#SBATCH --nodes=1                     # Use one node
#SBATCH --ntasks=1                    # Run a single task
#SBATCH --cpus-per-task=64             # Use 1 core
#SBATCH --mem=10gb                   # Memory limit
#SBATCH --time=30:00:00               # Time limit hrs:min:sec
#SBATCH --output=MTC_test_%j.out   # Standard output and error log

pwd; hostname; date

module load python

module load conda

module load sumo/1.20.0

conda activate MTC3.9

echo "Running MTC test script"

python DQN_run_medium.py --rv-rate 1.0 --stop-iters 1000 --framework torch --num-cpu $SLURM_CPUS_PER_TASK

date
