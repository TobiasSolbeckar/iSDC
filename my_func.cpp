#include <iostream>
#include <vector>
#include <cmath>
#include "my_func.h"

using namespace std;

/*
def generateNormDistr(x_val,mu,sigma):
# pdf = 1/sqrt(2*pi*sigma^2) * exp(-(x-mu)^2/2*sigma^2)
	norm_dist_val = []
	C = 1 / np.sqrt(2*np.pi*np.square(sigma))
	if isinstance(x_val,list):
		for x in x_val:
			norm_dist_val.append(C*np.exp((-0.5*np.square(x-mu))/(np.square(sigma))))
	else:
			norm_dist_val = C*np.exp((-0.5*np.square(x_val-mu))/(np.square(sigma)))
	return norm_dist_val
*/

float evaluate_gaussian(float mu, float sigma2, float x_val){
	float pi = 3.1415;
	float C = 1 / sqrt(2*pi*sigma2);
	return C*exp(-0.5*pow((x_val-mu),2)/sigma2);
}

vector<float> create_gaussian(float mu, float sigma2, vector<float> X){
	float pi = 3.1415;
	vector<float> gaussian_dist(X.size());
	float C = 1 / sqrt(2*pi*sigma2);
	for(int i = 0;i < X.size();i++){
		float x = X[i];
		gaussian_dist[i] = C*exp(-0.5*pow((x-mu),2)/sigma2);
	}
}

int distance(int velocity, int dt){
	return (velocity * dt);
}

void print_matrix(vector < vector <float> > matrix){
	for(int i=0;i<matrix.size();i++){
		for(int j=0;j<matrix[0].size();j++){
			cout << matrix[i][j] << " ";
		}
		cout << endl;
	}
}

vector < vector <int> > matrix_add(vector < vector <int> > A, vector < vector <int> > B){
	// Returns C, where C = A + B. A and B must be the same size.
	if (A.size() != B.size()){
		// TODO: Learn how to raise an error
		cout << "This should raise an error!" << endl;
	}
	else if (A[0].size() != B[0].size()){
		cout << "This should raise an error!" << endl;	
	}
	else
	{
		//This is the good case
		vector < vector <int> > C(A.size(),vector<int>(A[0].size(),0));
		for(int i=0;i<C.size();i++){
			for(int j=0;j<C[0].size();j++){
				C[i][j] = A[i][j] + B[i][j];
			}
		}
		return C;
	}
}

vector < vector <int> > matrix_sub(vector < vector <int> > A, vector < vector <int> > B){
	// Returns C, where C = A + B. A and B must be the same size.
	if (A.size() != B.size()){
		// TODO: Learn how to raise an error
		cout << "This should raise an error!" << endl;
	}
	else if (A[0].size() != B[0].size()){
		cout << "This should raise an error!" << endl;	
	}
	else
	{
		//This is the good case
		vector < vector <int> > C(A.size(),vector<int>(A[0].size(),0));
		for(int i=0;i<C.size();i++){
			for(int j=0;j<C[0].size();j++){
				C[i][j] = A[i][j] - B[i][j];
			}
		}
		return C;
	}
}

vector < vector <float> > matrix_mul(vector < vector <float> > A, vector < vector <float> > B){
	if (A[0].size() != B.size()){
		// TODO: Learn how to raise an error
		cout << "Number of columns in A: " << A[0].size() << endl;
		cout << "Number of rows in B:    " << B.size() << endl;
		cout << "This should raise an error!" << endl;
	}
	float cell_data;
	// For readability;
	int m = A.size();
	int n = A[0].size();
	int p = B[0].size();
	// Create a matrix with dimensions (m x p)
	vector < vector <float> > C(m,vector<float>(p,0));
	for(int i = 0;i<m;i++){
		for(int j = 0;j<p;j++){
			cell_data = 0;
			for(int k = 0;k<n;k++){
				cell_data += A[i][k] * B[k][j];
			}
			C[i][j] = cell_data;
		}
	}
	return C;
}

void print_vector(vector<float> v){
	for (int i=0;i<v.size();i++){
		cout << v[i] << " ";
	}
	cout << endl;
}


float vector_sum(vector<float> v){
	float sum = 0;
	for (int i=0;i<v.size();i++){
		sum += v[i];
	}
	return sum;
}

vector<float> sense(vector<float> p, char Z, vector<char> world, float pHit, float pMiss){
	// Z is the current measurement ('r' or 'g')
	vector<float> q(p.size(),0);
	int hit;
	float sum;

	for(int i=0;i<q.size();i++){
		hit = 0;
		if(Z == world[i]){
			hit = 1;
		}
		q[i] = p[i] * (hit*pHit + (1-hit)*pMiss);
	}
	sum = vector_sum(q);
	for(int i=0;i<q.size();i++){
		q[i] = q[i]/sum;
	}
	return q;
}

vector<float> move(vector<float> p, int U, float pExact, float pOvershoot, float pUndershoot){
	// U is the current motion
	vector<float> q(p.size(),0);
	float s;
	for(int i=0;i<q.size();i++){
		s = pExact * p[(i-U) % p.size()];
		s += pOvershoot * p[(i-U-1) % p.size()];
		s += pUndershoot * p[(i-U+1) % p.size()];
		q[i] = s;
	}
	return q;
}
