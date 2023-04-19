#ifndef CSV
#define CSV

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>

using namespace std;

class csv{
    public:
    void split(const string &, char, vector<string>&);
    void loadCSV(istream&, vector<vector<string>*>&);
    vector<vector<string>*> read();
    vector<double> alter(vector<string>*);
    void clear(vector<vector<string>*>);
    void makeCSV();
};

#endif