.PHONY: std primes test coverage-unit coverage-e2e

test:
	python3.8 -B -m unittest -v

coverage-unit:
	python3.8 -m coverage run tests.py && \
	coverage report && \
	coverage html && \
	firefox htmlcov/index.html

coverage-e2e:
	python3.8 -m coverage run main.py ../examples/*.sil >/dev/null && \
	coverage report && \
	coverage html && \
	firefox htmlcov/index.html

std:
	# NOTE: this contains debugging flags
	nasm -f elf64 -g -o std.o std.asm -l std.lst
	ld -g -o std std.o

primes:
	nasm -f elf64 -o prime.o primes.asm \
	&& ld -o prime prime.o \
        && rm prime.o

## Examples for eventual use

hello:
	nasm -f elf64 -o hello.o hello5.asm
        # gcc will include libc by default, by the initial section must be 
        # called main
	gcc -Wall -Wextra -Werror -o hello hello.o
        # ld -o hello hello.o -lc -I /lib/x86_64-linux-gnu/libc.so.6

dynamic:
	nasm -f elf64 -o hello.o hello5.asm
	ld -o hello hello.o -lc --dynamic-linker\
	 /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 
