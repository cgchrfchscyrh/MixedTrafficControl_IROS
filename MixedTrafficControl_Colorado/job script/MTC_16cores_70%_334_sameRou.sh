#!/bin/bash
#SBATCH --job-name=86_334_70%_sameRoute    # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liusongyang@ufl.edu   # Where to send mail	
#SBATCH --nodes=1                     # Use one node
#SBATCH --ntasks=1                    # Run a single task
#SBATCH --cpus-per-task=16             # Use 1 core
#SBATCH --mem=100gb              # Memory limit
#SBATCH --partition=hpg-default
#SBATCH --time=40:00:00               # Time limit hrs:min:sec
#SBATCH --output=out/86_334_70%_sameRoute_%j.out   # Standard output and error log
pwd; hostname; date

module load sumo/1.13.0
env_path=/blue/du.j/liusongyang/.conda/envs/MTC3.9/bin
export PATH=$env_path:$PATH

python DQN_run_medium_334_8control_sameRou.py --rv-rate 0.7 --stop-iters 1000 --framework torch --num-cpu $SLURM_CPUS_PER_TASK

date