#!/bin/bash
#SBATCH --job-name=MTC    # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=liusongyang@ufl.edu   # Where to send mail	
#SBATCH --nodes=1                     # Use one node
#SBATCH --ntasks=1                    # Run a single task
#SBATCH --cpus-per-task=64             # Use 1 core
#SBATCH --mem=400gb              # Memory limit
#SBATCH --partition=gpu
#SBATCH --gpus=a100:1
#SBATCH --time=40:00:00               # Time limit hrs:min:sec
#SBATCH --output=out/MTC_%j.out   # Standard output and error log
pwd; hostname; date

module load sumo/1.13.0
env_path=/blue/du.j/liusongyang/.conda/envs/MTC3.9/bin
export PATH=$env_path:$PATH

python DQN_run_medium_2control.py --rv-rate 0.8 --stop-iters 1000 --framework torch --num-cpu $SLURM_CPUS_PER_TASK

# python DQN_eval_100_medium_8control.py --rv-rate 1.0 --model-dir checkpoints/medium_8control_100%_checkpoint_001000 --save-dir evaluation_results --stop-timesteps 1000

date