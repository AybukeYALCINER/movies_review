# movies_review
Movie reviews are a fairly commonly used tool used by consumers to understand if a movie is worth the price and time. There are different methods to create reviews about movies. One of them is rating the movies by different users. GroupLens Research has collected and made available  rating datasets from the MovieLens web site (http://movielens.org). We used extra information about movies, Dennis Schwartz’s reviews.  

We implemented a python program that analyzes GroupLens’ data and compares them with Dennis Schwartz’s reviews. This program will create html files for movies which are both in Dennis Schwartz’s reviews and in GroupLens’ data and try to guess genres of movies based on the data which obtained from movies. 
## Stage 1
# Step 1: Understand the GroupLens’ data 

The last 19 fields are the genres, a 1 indicates the movie is of that genre, a 0 indicates it is not; movies can be in several genres at once.  

The movie ids are the ones used in the u.data.

> u.genre 
This file contains a list of the genres.  
 
We used this file to format genre field which are taken from u.item. 


> u.user 

 This file contains demographic information about the users; (The user ids are the ones used in the u.data data set.)
 
 > u.occupation 
This file consists of list of the occupations. (The occupation ids are the ones used in the u.user data )

> u.data 
The full data set, 100000 ratings by 943 users on 1682 items comprised of this file. 

# Step 2: Understand the Dennis Schwartz’s data 
Dennis Schwartz’ review data is taken from (https://www.cs.cornell.edu/people/pabo/moviereview-data/  You can look here to get information about Dennis Schwartz). This data consists of different txt files.
Each of files is about only a movie review. These files are supposed to be in a folder which is named film. We read these files one by one from the folder. 

# Step 3: Combine the GroupLens’ data and Dennis Schwartz’s data 

In order to create html files for movies, we combine the datasets. We create html files for the movies which are in film folder. In this step, we expected to use list comprehensions. 
Firstly, we compare the both dataset (movies in film folder and u.item) and select the movies which are in both  datasets. We will create review.txt file to write messages for movies which are in u.item but not in film folder and movies which are found in folder. Use user-defined exception to take messages. 

After selecting movies, We find user ids who rate them from u.data and get detail information about these users from u.user. 

# Step 4: Write review to html file 

When we extract information from given data for movies, we use this data to create html files which are located in filmList folder. 
