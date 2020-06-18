#!/bin/bash
#SBATCH --job-name=python-explorations-rerun-CP
#SBATCH --mail-type=ALL
#SBATCH --time=2-12:00
#SBATCH --mail-user=r.j.scheedler@student.rug.nl
#SBATCH --output=job-%j.log
#SBATCH --partition=regular
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128000

module load Python/3.6.4-foss-2018a
# Imports
pip install gitpython --user
pip install matplotlib --user
pip install pandas --user
pip install scipy --user
pip install mlxtend --user
pip install dtw-python --user
pip install PyGithub --user
pip install matplotlib-venn --user
pip install seaborn --user

srun /data/s2550709/CoChangeAnalysis/execution_scripts/job.sh