#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include "my_func.h"

using namespace std;

// declare a function
int some_func(int x);
int some_other_func(int x);

int main(){
	// Proper declaration of a 5x3 matrix, with values 2: 
	// vector < vector <int> > my_matrix (5, vector <int> (3, 2));
	int s = 0;
	int loops = 1000000000;
	clock_t t0;
	
	t0 = clock();
	for(int i=0;i<loops;i++){
		some_func(3);
	}
	cout << "1. Looptime is " << 1000.0*(clock()-t0)/CLOCKS_PER_SEC << " ms." << endl;

	t0 = clock();
	for(int i=0;i<loops;i++){
		some_other_func(3);
	}
	cout << "2. Looptime is " << 1000.0*(clock()-t0)/CLOCKS_PER_SEC << " ms." << endl;

	return 0;
}


int some_func(int x){
	static int y = 5 + x;
	return y;
}

int some_other_func(int x){
	int y = 5 + x;
	return y;
}