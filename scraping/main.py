from libraries import *
import functions as f


dataframe = pd.read_pickle("Data/users_and_followers_data.pkl")
dataframe
dataframe = pd.read_pickle("Data/users_tweets_data.pkl")
dataframe

dataframe.groupby("username").sum()

if __name__ == '__main__':
    
    
    queries = ['pokemon scarlet violet lang:en until:2022-09-10 since:2022-09-01 -filter:replies -filter:links' + "\n",     
               'pokemon scarlet violet lang:en until:2022-09-20 since:2022-09-11 -filter:replies -filter:links' + "\n", 
               'pokemon scarlet violet lang:en until:2022-09-30 since:2022-09-21 -filter:replies -filter:links' + "\n", 
               
               'pokemon scarlet violet lang:en until:2022-10-10 since:2022-10-01 -filter:replies -filter:links' + "\n",
               'pokemon scarlet violet lang:en until:2022-10-20 since:2022-10-11 -filter:replies -filter:links' + "\n",
               'pokemon scarlet violet lang:en until:2022-10-31 since:2022-10-21 -filter:replies -filter:links' + "\n",
               
               'pokemon scarlet violet lang:en until:2022-11-10 since:2022-11-01 -filter:replies -filter:links' + "\n",
               'pokemon scarlet violet lang:en until:2022-11-20 since:2022-11-11 -filter:replies -filter:links' + "\n",
               'pokemon scarlet violet lang:en until:2022-11-30 since:2022-11-21 -filter:replies -filter:links' + "\n",
               
               'pokemon scarlet violet lang:en until:2022-12-10 since:2022-12-01 -filter:replies -filter:links' + "\n"
               'pokemon scarlet violet lang:en until:2022-12-20 since:2022-12-11 -filter:replies -filter:links' + "\n"
               'pokemon scarlet violet lang:en until:2022-12-31 since:2022-12-21 -filter:replies -filter:links' + "\n"]
    

    f.get_usernames(queries)
    
    
    dataframe = pd.read_pickle("Data/users_and_followers_data.pkl")

    queries = ('pokemon scarlet violet (from:'+ dataframe["username"] +') lang:en since:2022-09-01 -filter:replies -filter:links' + "\n").array
    
    f.get_tweets(dataframe["username"].array, queries)
    