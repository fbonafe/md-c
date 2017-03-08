.PHONY: default help object sharedlib all clean
CC = gcc

CC_FLAGS = -g -std=gnu99 -O3 -fopenmp -ffast-math -mavx2 -fno-inline -fPIC
LD_FLAGS = -shared -lm -fopenmp

LD = $(CC)

SOURCE_C = $(wildcard *.c)
OBJECTS_C = $(patsubst %.c, %.o, $(SOURCE_C))

SHAREDLIB = libmd.so

default: all

objects: $(OBJECTS_C)

sharedlib: $(SHAREDLIB)

all: objects sharedlib

%.o: %.c
	$(CC) $(CC_FLAGS) -c $^

%.so: $(OBJECTS_C)
	$(LD) $(LD_FLAGS) $^ -o $@

clean:
	rm -rfv $(OBJECTS_C) $(SHAREDLIB)
