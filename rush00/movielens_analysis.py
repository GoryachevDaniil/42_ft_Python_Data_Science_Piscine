import os
import sys
import datetime as dt
import functools
import collections
from collections import Counter
# from bs4 import BeautifulSoup
import urllib
import json
# import requests
import re
# import pytest

class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file: str):
        self.filename = path_to_the_file
        # self.movies_csv_headers = ('movieId','title','genres')
        # self.movies_csv_types = (int, str, str)

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the 
        keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by 
        counts descendingly.
        """
        all_lines = self.read_file()
        del all_lines[0]        
        
        tmp = [el[1][-5:].rstrip(')') for el in all_lines]
        
        result = Counter()

        for el in tmp:
            try:
                int(el)
                if el in result:
                    result[el] += 1
                else:
                    result[el] = 1
            except:
                if 'Null' in result:
                    result['Null'] += 1
                else:
                    result['Null'] = 1

        return dict(result.most_common())
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys 
        are genres and the values are counts.
        Sort it by counts descendingly.
        """
        all_lines = self.read_file()
        del all_lines[0]

        tmp = [el[2].split('|') for el in all_lines]

        result = Counter()
        
        for elem in tmp:
            for el in elem:
                if el:
                    result[el] += 1

        return dict(result.most_common())
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies 
        where the keys are movie titles and 
        the values are the number of genres of the 
        movie. Sort it by numbers descendingly.
        """
        all_lines = self.read_file()
        del all_lines[0]

        result = dict()

        for elem in all_lines:
            result[elem[1]] = len(elem[2].split('|'))

        return dict(sorted(result.items(), \
                        key=lambda x: x[1], reverse=True)[:n])

    def read_file(self):
        with open(self.filename, "r", encoding='utf-8') as f:
            line = f.readlines()
            all_lines = []
            for i in range(len(line)):
                tmp_line = line[i].replace('\n', '')

                if tmp_line.find('"') != -1:
                    splitted = re.split(r',\"|\",', tmp_line)
                else:
                    splitted = tmp_line.split(',')
                all_lines.append(splitted)

        return all_lines

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    # ratings_headers = ('userId','movieId','rating','timestamp')
    # ratings_separator = ','
    # ratings_types = (int, int, float, int)

    def __init__(self, path_to_the_file: str):
        """
        Put here any fields that you think you will need.
        """
        self.filename = path_to_the_file


    def read_file(self):
        with open(self.filename, "r", encoding='utf-8') as f:
            line = f.readlines()
            all_lines = []

            for i in range(len(line)):
                tmp_line = line[i].replace('\n', '')
                all_lines.append(tmp_line.split(','))

        return all_lines

    class Movies:    
        def __init__(self, ratings_cls, movies_cls: Movies):
            if not isinstance(ratings_cls, Ratings) or not isinstance(movies_cls, Movies):
                raise ValueError('invalid Movies class object')
            self.ratings = ratings_cls
            self.movies_cls = movies_cls

        def dist_by_year(self):
            """
            The method returns a dict where the keys 
            are years and the values are counts. 
            Sort it by years ascendingly. You need 
            to extract years from timestamps.
            """
            result = Counter()
            tmp = self.ratings.read_file()
            for i in range(1, len(tmp)):
                year = dt.datetime.fromtimestamp(int(tmp[i][3])).year
                result[year] += 1

            return dict(sorted(result.items()))


        # def NEXT_METHOD():      <---



class TestRatings:
    """Tests for Ratings class
    """
    @classmethod
    def setup_class(cls):
        cls.ratings = Ratings('data/ratings.csv')
        cls.mov = Movies('data/movies.csv')
        cls.ratings_movies = Ratings.Movies(cls.ratings, cls.mov)
        # cls.ratings_users = Ratings.Users(cls.ratings, cls.mov) ## make Users

    def test__movies__dist_by_years__types(self):
        """Test are dist_by_years method result types correct
        # """
        result = self.ratings_movies.dist_by_year()
        print(result)


def main():
    mov = Movies('data/movies.csv')
    rat = Ratings('data/ratings.csv')

    testRat = TestRatings()
    testRat.setup_class()
    testRat.test__movies__dist_by_years__types()

if __name__ == '__main__':
    main()




#############################################
############### CHERNOVIK ###################
#############################################

# def main():
#     mov = Movies('data/movies.csv')
    
#     test_1 = mov.dist_by_release()
#     # print(test_1)

#     test_2 = mov.dist_by_genres()
#     # print(test_2)

#     test_3 = mov.most_genres(10)
#     # print(test_3)

#     rats = Ratings('data/movies.csv')
#     # mov = Movies('data/movies.csv')
#     rats_movies = Ratings.Movies(rats, mov)
#     # rats_users = Ratings.Users(rats, mov)


#     rats_movies.dist_by_year(rats, mov)

#     # rat = Ratings('data/ratings.csv')
#     # tmp = rat.read_file()
#     # print(tmp[1])



#     test_4 = rat.dist_by_year(rat, mov)
#     print(test_4)




# if __name__ == '__main__':
#     main()
