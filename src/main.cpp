#include <iostream>
#include <cstdlib>
#include <iostream>
#include "CSV.h"
#include "kmeans.h"

int main(){
    csv playlist1;
    playlist1.makeCSV();

    string answer;
    cout << "Would you like to merge your playlist with another user's? Y/N: ";
    cin >> answer;

    if(answer == "Y" || answer == "y"){
        Combine merge;
        merge.run();
    }

    return 0;
}
