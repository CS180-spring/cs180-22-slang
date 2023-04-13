#include </usr/local/opt/libomp/include/omp.h> //do we need include path?
#include <algorithm>
#include <cmath>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <vector>
#include "readCSV.h"

using namespace std;

class Song{
    private:
        string name; //song name
        int cluster; //which cluster the song belongs to
        int dimensions; //number of features being analyzed
        vector<double> coordinates; //coordinates on graph 

    public:
        Song(string songName, vector<double> coords){
            name = songName;
            cluster = 0; //initially doesn't belong to any closter
            coordinates = coords;
            dimensions = coordinates.size();
        }
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
        kMeans(int K, int numOfIterations, string outputLoc){
            k = K;
            iterations = numOfIterations;
            outputFile = outputLoc;
        }
        void classify(vector<Song> &allSongs){
            totalSongs = allSongs.size();
            dimensions = allSongs.at(0).getDimensions();

            vector<string> usedSongs;

            //make k clusters and pick a random song to put in each. These random songs
            //will act as the cluster centers for now
            for(int i = 1; i < k; i++){
                while(1){
                    int index = rand() % totalSongs;
                    string tempSong = allSongs.at(index).getName();
                    if(find(usedSongs.begin(), usedSongs.end(), tempSong) == usedSongs.end()){
                        usedSongs.push_back(allSongs.at(index).getName());
                        allSongs.at(index).setCluster(i);
                        Cluster newCluster(i, allSongs.at(index));
                        clusters.push_back(newCluster);
                        break;
                    }
                }
            }

            int itNum = 1;
            while(1){
                bool done = true;
                //we learned this command in 160. Speeds up clustering process since
                //we'll have many songs
                #pragma omp parallel for reduction(&&: done) num_threads(16)

                for(int i = 0; i < totalSongs; i ++){
                    int currCluster = allSongs.at(i).getCluster();
                    int nearestCluster = getNearestCluster(allSongs.at(i));
                    if(currCluster != nearestCluster){
                        allSongs.at(i).setCluster(nearestCluster);
                        done = false;
                    }
                }

                //clear the clusters and reassign based on what we found above
                clearClusters();
                for(int i = 0; i < totalSongs; i++){
                    clusters.at(allSongs.at(i).getCluster() - 1).addSong(allSongs.at(i));
                }

                //recalculate the cluster centers
                for(int i = 0; i < k; i++){
                    int size = clusters.at(i).getSize();
                    for(int j = 0; j < dimensions; j++){
                        double sum = 0;
                        if(size > 0){
                            #pragma omp parallel for reduction(+: sum) num_threads(16)
                            for(int l = 0; l < size; l++){
                                sum += clusters.at(i).getSong(l).getCoord(j);
                            }
                            clusters.at(i).setCenter(j, sum/size);
                        }
                    }
                }

                if(done || itNum >= iterations){
                    break;
                }
                itNum ++;
            }

            ofstream outFile;
            outFile.open(outputFile, ios::out);
            
            for(int i = 0; i < totalSongs; i++){
                outFile << allSongs.at(i).getName() << ": " << allSongs.at(i).getCluster() << endl;
            }
        }
};

int main(){
    string output = "";
    int clusterNumber;
    int iterationNumber = 100; //we can make this user specified
    csv songList;

    vector<Song> allSongs;
    
    vector<vector<string>*> returnData = songList.read();
    for(int i = 0; i < returnData.size(); i++){
       vector<string> *temp = returnData.at(i);
    //    string tempName = (*temp).at(0);
    //    cout << "before alter" << endl;
    //    vector<double> allDoubles = songList.alter(temp);
    //    cout << "finished alter" << endl;
    //    Song newSong(tempName, allDoubles);
    //    allSongs.push_back(newSong);

        for(int j = 0; j < (*temp).size(); j++){
            cout << i << ":" << (*temp).at(j) << endl;
        }
    }

    // cout << "Please enter the name of the output file: ";
    // cin >> output;
    // cout << endl;

    // cout << "Specify the number of clusters you want: ";
    // cin >> clusterNumber;
    // cout << endl;

    // ofstream outFile;
    // outFile.open("outputFile.txt", ios::out);

    // for(int i = 0; i < allSongs.size(); i++){
    //     outFile << allSongs.at(i).getName() << ": ";
    //     vector<double>coords = allSongs.at(i).getCoords();
    //     for(int j = 0; j < coords.size(); j++){
    //         outFile << coords.at(i) << ", " << endl;
    //     }
    // }

    return 0;
}