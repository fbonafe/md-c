#ifndef FORCE_H
#define FORCE_H
#include <omp.h>
#include <stdio.h>
#include "system.h"
#include "cell.h"

void newton(System *sys, CellList *clist, double sigma, double epsilon, double mass);
void minimum_images(System *sys, double *dr);
double calculate_force(System *sys, int i, int j, double *dr, int tid, double sigma, double epsilon, double mass);
void kinetic(System *sys);
void tally_force(System *sys);
#endif
