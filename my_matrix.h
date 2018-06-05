#ifndef MY_MATRIX.H
#define MY_MATRIX.H

#include <iostream>
#include <vector>

/*
class Classname
{
    private:
        declare private variables;
        declare private functions;

    public:
        declare public variables;
        declare public functions;
};
*/

class Matrix
{
	private:
		vector < vector <float> > grid;
		vector<float>::size_type rows;
		vector<float>::size_type cols;

}
/// Vector / Matrix functions
void print_matrix(vector < vector <float> > matrix);
void print_vector(vector<float> v);
vector < vector <int> > matrix_add(vector < vector <int> > A, vector < vector <int> > B);
vector < vector <int> > matrix_sub(vector < vector <int> > A, vector < vector <int> > B);
vector < vector <float> > matrix_mul(vector < vector <float> > A, vector < vector <float> > B);
vector<float> sense(vector<float> p, char Z, vector<char> world, float pHit, float pMiss);
vector<float> move(vector<float> p, int U, float pExact, float pOvershoot, float pUndershoot);

#endif // MY_MATRIX.H