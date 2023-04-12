//inspired by https://www.oreilly.com/library/view/c-cookbook/0596007612/ch04s24.html

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

void split(const string& s, char c, vector<string>& v) {
   int i = 0;
   int j = s.find(c);

   while (j >= 0) {
      v.push_back(s.substr(i, j-i));
      i = ++j;
      j = s.find(c, j);

      if (j < 0) {
         v.push_back(s.substr(i, s.length()));
      }
   }
}

void loadCSV(istream& in, vector<vector<string>*>& data) {

   vector<string>* p = NULL;
   string tmp;

   while (!in.eof()) {
      getline(in, tmp, '\n');

      p = new vector<string>();
      split(tmp, ',', *p); 
      data.push_back(p);

      cout << tmp << '\n';
      tmp.clear();
   }
}

vector<vector<string>*> read(){
    string doc;

    cout << "Please enter csv to read: ";
    cin >> doc;
    cout << endl;

   ifstream in(doc);

   vector<vector<string>*> data;

   loadCSV(in, data);

   return data;
}

void clear(vector<vector<string>*> data){
    for(vector<vector<string>*>::iterator p = data.begin();p != data.end(); ++p) {
      delete *p;
   }   
}