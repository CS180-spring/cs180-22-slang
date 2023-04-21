#ifndef KMEANS
#define KMEANS

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
        Song(string, vector<double>);
        int getDimensions(){ 
            return dimensions;
        }
        int getCluster(){
            return cluster; 
        }
        void setCluster(int val){
            cluster = val; 
        }
        vector<double> getCoords(){ //returns entire coordinate
            return coordinates;
        }
        double getCoord(int index){ //gets specific term in coordinate
            return coordinates.at(index); 
        }
        string getName(){
            return name;
        }
};

class Cluster{
    private:
        int clusterNumber;
        vector<Song> songs; //songs in cluster
        vector<double> center; //the center of the cluster (for math purposes)

    public:
        Cluster(int, Song);
        void addSong(Song);
        bool removeSong(string);
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
        int k, dimensions, totalSongs, iterations;
        vector<Cluster> clusters;
        string outputFile;

        void clearClusters(){
            for(int i = 0; i < k; i++){
                clusters.at(i).removeAllPoints();
            }
        }

        int getNearestCluster(Song inputSong){
            double sum, shortestPath;
            int nearest;
            sum = 0.00;

            if(dimensions == 1){ //if we only have one song feature to analyze
                shortestPath = abs(clusters.at(0).getCenterCoord(0) - inputSong.getCoord(0));
            }
            else{ //calculating euclidean distance
                for(int i = 0; i < dimensions; i++){
                    sum += pow(clusters.at(0).getCenterCoord(i) - inputSong.getCoord(i), 2);
                }
                shortestPath = sqrt(sum);
            }
            nearest = clusters.at(0).getClusterNum();

            //above we got the distance for the first cluster so we have something to compare to
            //now we'll go through the rest of the clusters and see if we can find one closer
            //to our current song

            for(int i = 1; i < k; i++){
                double distance;
                sum = 0.00; //clear from last use

                if(dimensions == 1){
                    distance = abs(clusters.at(i).getCenterCoord(0) - inputSong.getCoord(0));
                }
                else{
                    for(int j = 0; j < dimensions; j++){
                        sum += pow(clusters.at(i).getCenterCoord(j) - inputSong.getCoord(j), 2);
                    }
                    distance = sqrt(sum);
                }

                if(distance < shortestPath){
                    shortestPath = distance;
                    nearest = clusters.at(i).getClusterNum();
                }
            }

            return nearest;
        }

    public:
        kMeans(int, int, string);
        void classify(vector<Song> &);
};

class Combine{
    public:
        int run();
};

#endif