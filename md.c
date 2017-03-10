#include "md.h"

float timedifference_msec(struct timeval t0, struct timeval t1)
{
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_usec - t0.tv_usec) / 1000000.0f;
}

void onestep(System *sys, CellList *clist, Integrator *integ) {
    first_step(integ, sys);
    update_cells(clist, sys);
    newton(sys, clist);
    last_step(integ, sys);
    kinetic(sys);
}


int simpleloop(int nsteps, System *sys, CellList *clist, Integrator *integ) {
  for (int i = 0; i < nsteps; i++) {
    onestep(sys, clist, integ);
  }
  return 0;
}

int get_num_threads() {
  int nthreads;
#pragma omp parallel
  nthreads = omp_get_num_threads();
  return nthreads;
}

int init_vars(System *sys, CellList *clist, Integrator *integ) {
  fill_cells(clist, sys);
  integ->timestep = sys->timestep;

  printf("%d threads\n", sys->nthreads);
  update_cells(clist, sys);
  newton(sys, clist);
  kinetic(sys);
  return 0;
}


int mainloop(System *sys, CellList *clist, Integrator *integ, FILE *file_energy, FILE *file_time, struct timeval start, struct timeval now) {
  for (int i = 0; i < sys->n_steps; i++) {
    onestep(sys, clist, integ);
    fprintf(file_energy, "%g, %g, %g\n", sys->potential, sys->kinetic, sys->potential+sys->kinetic);
    gettimeofday(&now, NULL);
    double elapsed = timedifference_msec(start, now);
    fprintf(file_time, "%i, %g\n", i, elapsed);
    printf("%i,  %g\n", i, elapsed);
  }
  return 0;
}


int main(int argc, char** argv) {
  FILE *file_time, *file_energy;
  struct timeval start, now;
  file_time = fopen("time.dat", "w");
  file_energy = fopen("energy.dat", "w");
  fprintf(file_energy, "#Potential, Kinetic, Total\n");

  System *sys = (System *) malloc(sizeof(System));

  sys->nthreads = get_num_threads();
  printf("%d threads\n", sys->nthreads);

  if (argc != 3) {
    fprintf(stderr, "usage: %s n_steps n_particles\n", argv[0]);
    exit(1);
  }
  sys->n_particles = atoi(argv[2]);
  sys->n_steps = atoi(argv[1]);
  sys->size = cbrt(sys->n_particles/0.45);
  sys->rcut = 2.5;
  sys->phicut = 4.0*(pow(2.5, -12) - pow (2.5, -6));
  init_system(sys);
  
  CellList *clist = (CellList *) malloc(sizeof(CellList));
  init_cells(clist, sys, 2.5);
  Integrator *integ = (Integrator *) malloc(sizeof(Integrator));
  integ->timestep = 0.0005;
  update_cells(clist, sys);
  newton(sys, clist);
  kinetic(sys);

  gettimeofday(&start, NULL);
  mainloop(sys, clist, integ, file_energy, file_time, start, now);
  gettimeofday(&now, NULL);
  
  double elapsed = timedifference_msec(start, now);
  printf("Steps: %d, Part: %d, Time: %f\n", sys->n_steps, sys->n_particles, elapsed);
  return 0;
}
