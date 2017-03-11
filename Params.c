#include "Params.h"

void Params(double* params){
  int elem;

  printf ( "\n" );
  printf ( "  Choose the element for the simulation \n" );
  printf ( "  Ar(1)\t Kr(2)\t N2(3)\t Xe(4)\t CO2(5)\t CH4(6) \n" );
  scanf ( "%d", &elem );
  
  double sigma = 0.;
  double epsilon = 0.;
  double mass = 0.;
  /* Ar */
  if (elem == 1){
	  sigma = 0.34;
	  epsilon = 0.120;
	  mass = 26.982;
  }
  /* Kr*/
  if (elem == 2){
	  sigma = 0.38;
	  epsilon = 0.164;
	  mass = 83.798;
  }
  /* N2 */
  if (elem == 3){
	  sigma = 0.37;
	  epsilon = 0.95;
	  mass = 28.0;
  }
  /* Xe */
  if (elem == 4){
	  sigma = 0.45;
	  epsilon = 0.222;
	  mass = 131.293;
  }
  /* CO2 */
  if (elem == 5){
	  sigma = 0.43;
	  epsilon = 0.193;
	  mass = 44.009;
  }
  /* CH4 */
  if (elem == 6){
	  sigma = 0.38;
	  epsilon = 0.149;
	  mass = 16.043;
  }
  params[0] = sigma;
  params[1] = epsilon;
  params[2] = mass;
  /************************************/
  printf ("sigma = %lf\t epsilon = %lf\t mass = %lf\n", sigma, epsilon, mass);
  // printf ("p1 = %lf\t p2 = %lf\t p3 = %lf\n", params[0], params[1], params[2]);
  return;
}