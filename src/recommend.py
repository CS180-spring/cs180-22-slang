import pandas as pd

def generalize(input_df):
    generalized = input_df.copy()
    danceability_avg = input_df["danceability"].mean()
    energy_avg = input_df["energy"].mean()
    loudness_avg = input_df["loudness"].mean()
    speechiness_avg = input_df["speechiness"].mean()
    instrumentalness_avg = input_df["instrumentalness"].mean()
    liveness_avg = input_df["liveness"].mean()
    average = pd.concat([danceability_avg, energy_avg, loudness_avg, speechiness_avg, instrumentalness_avg, liveness_avg], join ='outer', axis = 1)
    return average
def recommend(generalized):
    general = generalized.copy()