#include <iostream>
#include <vector>

using namespace std;

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


/// Misc.
int distance(int velocity, int dt);

/// Gaussian
float evaluate_gaussian(float mu, float sigma2, float x_val);
vector<float> create_gaussian(float mu, float sigma2, vector<float> X);

/// Vector / Matrix functions
void print_matrix(vector < vector <float> > matrix);
void print_vector(vector<float> v);
vector < vector <int> > matrix_add(vector < vector <int> > A, vector < vector <int> > B);
vector < vector <int> > matrix_sub(vector < vector <int> > A, vector < vector <int> > B);
vector < vector <float> > matrix_mul(vector < vector <float> > A, vector < vector <float> > B);
vector<float> sense(vector<float> p, char Z, vector<char> world, float pHit, float pMiss);
vector<float> move(vector<float> p, int U, float pExact, float pOvershoot, float pUndershoot);