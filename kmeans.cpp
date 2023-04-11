#include </usr/local/opt/libomp/include/omp.h> //do we need include path?
#include <algorithm>
#include <cmath>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <vector>

using namespace std;

class Song{
    private:
        string name; //song name
        int cluster; //which cluster the song belongs to
        int dimensions; //number of features being analyzed
        vector<double> coordinates; //coordinates on graph 

    public:
        Song(string songName, string coords){
            name = songName;
            cluster = 0; //initially doesn't belong to any closter

            //turns string of coordinates into a vector
            //unsure if this works with negative numbers as of rn
            stringstream iss(coords);
            double number;
            while(iss >> number){
                coordinates.push_back(number);
            }

            dimensions = coordinates.size();
        }
        int getDimensions(){ 
            return dimensions;
        }
        int getCluster(){
            return cluster; 
        }
        string getName(){
            return name;
        }
        vector<double> getCoords(){
            return coordinates;
        }
        void setCluster(int val){
            cluster = val; 
        }
        double getCoord(int index){ 
            return coordinates.at(index); 
        }
};

class Cluster{
    private:
        int clusterNumber;
        vector<Song> songs; //songs in cluster
        vector<double> center; //the center of the cluster (for math purposes)

    public:
        Cluster(int num, Song cent){
            clusterNumber = num;
            center = cent.getCoords();

            //we want to add the center to the cluster so we know where the center is for the
            //next round of calculations
            this->addSong(cent);
        }
        void addSong(Song newSong){
            newSong.setCluster(this->clusterNumber);
            songs.push_back(newSong);
        }
        bool removeSong(string songName){
            for(int i = 0; i < songs.size(); i++){
                if(songs.at(i).getName() == songName){
                    songs.erase(songs.begin() + i);
                    return true;
                }
            }
            return false;
        }
        void removeAllPoints(){
            songs.clear();
        }
        int getClusterNum(){
            return clusterNumber;
        }
        Song getSong(int index){
            return songs.at(index);
        }
        int getSize(){ 
            return songs.size();
        }
        double getCenterCoord(int index){
            return center.at(index);
        }
        void setCenter(int coord, double newCenterCoord){
            this->center.at(coord) = newCenterCoord; 
        }
};

class kMeans{
    private:

    public:
};

int main(int argc, char **argv){

    return 0;
}