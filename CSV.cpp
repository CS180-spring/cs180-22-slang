#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include "CSV.h"

using namespace std;

//separates the values by commas
void csv::split(const string&s, char c, vector<string>&v){
   int i = 0;
   int j = s.find(c);
   string sCopy = s;

   while(j >= 0){
      top:
      int k = sCopy.find("\"");
      if(k == 0){
         sCopy = sCopy.substr(1, sCopy.length());
         k = sCopy.find("\"");
         string temp2 = sCopy.substr(0, k-1);
         v.push_back(temp2);
         sCopy = sCopy.substr(k+2, sCopy.length());
         j = sCopy.find(c);
         goto top;
      }

      v.push_back(sCopy.substr(0, j-i));
      sCopy = sCopy.substr(j+1, sCopy.length());
      j = sCopy.find(c);

      if(j < 0){
         v.push_back(sCopy.substr(i, sCopy.length()));
      }
   }
}

//reads the csv and returns a vector of vectors
//each internal vector contains the values of each line in the csv
//each comma separated value on a line is a value in an internal vector
void csv::loadCSV(istream& in, vector<vector<string>*>& data){
   vector<string>* p = NULL;
   string temp;

   while(!in.eof()){
      getline(in, temp, '\n');

      if(temp == ""){
         return;
      }

      p = new vector<string>();
      split(temp, ',', *p);
      data.push_back(p);

      temp.clear();
   }
}

//opens the user specideied csv and loads its contents into a vector 
//of vectors where each internal vector is a line in the csv
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

//reads Playlist.csv and Playlist2.csv and combines them into a 
//vector of vectors to return as the list of songs
vector<vector<string>*> csv::makeCombined(){

   string doc = "Playlist.csv";
   ifstream in(doc);
   vector<vector<string>*> data;

   loadCSV(in, data);

   doc = "Playlist2.csv";
   ifstream in2(doc);
   loadCSV(in2, data);

   return data;
}

//changes the contents of a line in the csv to doubles from strings
//this is for math purposes later on
vector<double> csv::alter(vector<string>* data){
   vector<double> doubles;
   for(int i = 4; i < (*data).size(); i++){
      doubles.push_back(std::stod((*data).at(i)));
   }

   return doubles;
}

//frees memory
void csv::clear(vector<vector<string>*> data){
    for(vector<vector<string>*>::iterator p = data.begin();p != data.end(); ++p) {
      delete *p;
   }   
}

//runs the python script in API.py
//returns a csv filled with song data from a user specified playlist
void csv::makeCSV(){
    int result = std::system("python3 API.py");
    if(result != 0){
        std::cerr << "Error: Unable to run script" << std::endl;
    }
}

//runs the python script in cluster.py
//ONLY RUN WHEN WE ALREADY HAVE THE FIRST USER'S PLAYLIST BUILT
//returns a lump csv with all songs from both the user and user's friend's
//playlists for analysis in kmeans.cpp
void csv::makeCSV2(){
   int result = std::system("python3 cluster.py");
    if(result != 0){
        std::cerr << "Error: Unable to run script" << std::endl;
    }
}