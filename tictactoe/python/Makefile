PYTHON=python3.7
PYPY=pypy3

BENCH=bench.py

ARGS=immutable
ARGS2=mutable
TIME=time -f "user %U"

STATS=stats.py

all:
	$(PYTHON) $(BENCH) $(ARGS)

bench:
	$(TIME) $(PYTHON) $(BENCH) $(ARGS)
	$(TIME) $(PYPY) $(BENCH) $(ARGS)
	$(TIME) $(PYTHON) $(BENCH) $(ARGS2)
	$(TIME) $(PYPY) $(BENCH) $(ARGS2)

save:
	make bench 2>&1 | cat >>logs/BENCHMARKS

stats:
	$(PYTHON) $(STATS) results_memo
