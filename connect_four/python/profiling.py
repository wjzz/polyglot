import solve

import cProfile
import pstats # TODO: check the usage of this module (you need to save the profile to a file)

profile = cProfile.Profile()
profile.runcall(solve.main)
profile.print_stats()

# Jupyter
# %prun function()
# %prun?  == help

# python -m cProfile -o pi.stats simple_pi.py
# snakeviz pi.stats

# line by line profiling - 1:30:00 mark in the video
# kernprof -v -l input_file.py        # use the @profile decorator