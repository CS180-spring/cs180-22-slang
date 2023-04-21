#include </usr/local/opt/libomp/include/omp.h> //do we need include path?
#include <algorithm>
#include <cmath>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <vector>
#include "CSV.h"
#include "kmeans.h"

using namespace std;

Song::Song(string songName, vector<double> coords){
    name = songName;
    cluster = 0; //initially doesn't belong to any closter
    coordinates = coords;
    dimensions = coordinates.size();
}
        
Cluster::Cluster(int num, Song cent){
    clusterNumber = num;
    center = cent.getCoords();

    //we want to add the center to the cluster so we know where the center is for the
    //next round of calculations
    this->addSong(cent);
}
void Cluster::addSong(Song newSong){
    newSong.setCluster(this->clusterNumber);
    songs.push_back(newSong);
}
bool Cluster::removeSong(string songName){
    for(int i = 0; i < songs.size(); i++){
        if(songs.at(i).getName() == songName){
            songs.erase(songs.begin() + i);
            return true;
        }
    }
    return false;
}

kMeans::kMeans(int K, int numOfIterations, string outputLoc){
    k = K;
    iterations = numOfIterations;
    outputFile = outputLoc;
}
void kMeans::classify(vector<Song> &allSongs){
    totalSongs = allSongs.size();
    dimensions = allSongs.at(0).getDimensions();

    vector<string> usedSongs;

    //make k clusters and pick a random song to put in each. These random songs
    //will act as the cluster centers for now
    for(int i = 1; i < k+1; i++){
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
    while(true){

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

int Combine::run(){
    string output = "output/outputFile.txt";
    int clusterNumber;
    int iterationNumber = 100; //we can make this user specified
    csv songList;
    vector<Song> songs;

    songList.makeCSV2(); //makes the second csv for the playlist the user wants to merge with
    
    vector<vector<string>*> returnData = songList.makeCombined(); //combines both csv data

    //builds songs out of each vector of strings and adds them to allSongs
    for(int i = 0; i < returnData.size(); i++){
       vector<string> *temp = returnData.at(i);
       string tempName = (*temp).at(2);
       vector<double> allDoubles = songList.alter(temp);
       Song newSong(tempName, allDoubles);
       songs.push_back(newSong);
    }

    cout << "Specify the number of clusters you want: ";
    cin >> clusterNumber;
    if(songs.size() < clusterNumber){
        cout << "Error: more clusters than songs in playlists" << endl;
        return 0;
    }

    kMeans combination(clusterNumber, iterationNumber, output);
    combination.classify(songs);

    return 0;
}