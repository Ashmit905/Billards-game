CC = clang
CFLAGS = -Wall -std=c99 -pedantic -g
PYTHON = python3.10

all: _phylib.so

clean:
	rm -f *.o *.so

phylib_wrap.c phylib.py: phylib.i
	swig -python -py3 phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -o phylib_wrap.o -I /usr/include/$(PYTHON)

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) phylib_wrap.o -L. -L /usr/lib/$(PYTHON) -lphylib -l$(PYTHON) -shared -o _phylib.so

libphylib.so: phylib.o
	$(CC) $(CFLAGS) phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o -fPIC



	

	
