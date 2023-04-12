#ifndef CSV
#define CSV

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

class csv{
    public:
    void split(const string &, char, vector<string>&);
    void loadCSV(istream&, vector<vector<string>*>&);
    vector<vector<string>*> read();
};

#endif CSV