#include <iostream>

using namespace std;

int rem = 0;
int ind = 0;
int i = 0;
   
int foodAvailability(int FP[], int P[], int n) {
    
    // Getting the first occurence
    for(i = 0; i < n; i++) {
        if(FP[i] > P[i]) {
            ind = i;
            break;
        }    
    }

    // Traversing through array
    if(ind != 0) {
        for (i = ind; i < n + ind; i++) {
            rem = abs(FP[(i%n)] - P[(i%n)]);
            FP[((i+1)%n)] += rem;
        }
        if(rem == 0) {
            return ind;
        } else {
            return -1;
        }
    } 
    
    return -1;
}
   

int main()
{
    int FP[] = {1, 2, 3, 4, 5};
    int P[] = {3, 4, 5, 1, 2};
	int n = sizeof(FP) / sizeof(FP[0]);
    int res = foodAvailability(FP, P, n);
    cout<<res;
    return 0;
}
