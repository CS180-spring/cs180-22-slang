#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include "CSV.h"

using namespace std;

void csv::split(const string&s, char c, vector<string>&v){
   int i = 0;
   int j = s.find(c);
   string sCopy = s;

   while(j >= 0){
      v.push_back(sCopy.substr(0, j-i));
      sCopy = sCopy.substr(j+1, sCopy.length());
      j = sCopy.find(c);

      if(j < 0){
         v.push_back(sCopy.substr(i, sCopy.length()));
      }
   }
}

void csv::loadCSV(istream& in, vector<vector<string>*>& data){
   vector<string>* p = NULL;
   string temp;

   while(!in.eof()){
      getline(in, temp, '\n');

      p = new vector<string>();
      split(temp, ',', *p);
      data.push_back(p);

      temp.clear();
   }
}

vector<vector<string>*> csv::read(){
   string doc;

   cout << "Please enter the csv to read: ";
   cin >> doc;
   cout << endl;

   ifstream in(doc);
   vector<vector<string>*> data;

   loadCSV(in, data);

   return data;
}

vector<double> csv::alter(vector<string>* data){
   vector<double> doubles;
   for(int i = 1; i < (*data).size(); i++){
      doubles.push_back(std::stod((*data).at(i)));
   }

   return doubles;
}

void csv::clear(vector<vector<string>*> data){
    for(vector<vector<string>*>::iterator p = data.begin();p != data.end(); ++p) {
      delete *p;
   }   
}

void csv::makeCSV(){
    int result = std::system("python3 API.py");
    if(result != 0){
        std::cerr << "Error: Unable to run script" << std::endl;
    }
}