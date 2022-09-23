import os
import sys
import datetime as dt
# import functools
from functools import reduce
# import collections
from collections import Counter, defaultdict
import urllib
import json
import re

class Movies:
    def __init__(self, path_to_the_file: str):
        self.filename = path_to_the_file
        self.titles = {}
        for data in self.read_file():
            self.titles[data[0]] = data[1]

    def dist_by_release(self):
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
        all_lines = self.read_file()
        del all_lines[0]

        result = dict()

        for elem in all_lines:
            result[elem[1]] = len(elem[2].split('|'))

        return dict(sorted(result.items(), \
                        key=lambda x: x[1], reverse=True)[:n])
    
    def get_title(self, movie_id):
        return self.titles.get(movie_id)

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


class Statistics:
    @staticmethod
    def average(values: list):
        return sum(values) / len(values)


    @staticmethod
    def median(values: list):
        if len(values) == 0:
            raise ValueError('List is empty.')

        if len(values) == 1:
            return float(values[0])

        values = sorted(values)
        mid = int(len(values) / 2)
        
        if len(values) % 2:
            return float(values[mid])
        
        return (values[mid - 1] + values[mid]) / 2.0

    @classmethod
    def variance(cls, values: list):
        mean = cls.average(values)

        def reduce_func(prev, curr):
            diff = curr - mean
            return prev + diff * diff
        
        squares_sum = reduce(reduce_func, values)

        return squares_sum / len(values)


class Ratings:
    def __init__(self, path_to_the_file: str):
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
                raise ValueError('invalid class object')
            self.ratings = ratings_cls
            self.movies_cls = movies_cls

        def dist_by_year(self):
            result = Counter()
            tmp = self.ratings.read_file()
            for i in range(1, len(tmp)):
                year = dt.datetime.fromtimestamp(int(tmp[i][3])).year
                result[year] += 1

            ratings_by_year = dict(sorted(result.items()))

            return ratings_by_year

        def dist_by_rating(self):
            result = Counter()
            tmp = self.ratings.read_file()

            for i in range(1, len(tmp)):
                rat = tmp[i][2]
                result[rat] += 1

            ratings_distribution = dict(sorted(result.items()))

            return ratings_distribution
        
        def top_by_num_of_ratings(self, top_size: int):
            result = Counter()

            tmp = self.ratings.read_file()

            for i in range(1, len(tmp)):
                result[self.movies_cls.get_title(tmp[i][1])] += 1

            top_movies = dict(result.most_common(top_size))

            return top_movies
        
        def top_by_ratings(self, n, metric=Statistics.average):
            all_movies = defaultdict(list)

            tmp = self.ratings.read_file()
            del tmp[0]

            for data in tmp:
                all_movies[self.movies_cls.get_title(data[1])].append(float(data[2]))

            for movie in all_movies:
                all_movies[movie] = round(metric(all_movies[movie]), 2)

            top_movies = dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

            return top_movies
        
        def top_controversial(self, n):
            all_movies = defaultdict(list)

            tmp = self.ratings.read_file()
            del tmp[0]

            for data in tmp:
                all_movies[self.movies_cls.get_title(data[1])].append(float(data[2]))

            for movie in all_movies:
                all_movies[movie] = round(Statistics.variance(all_movies[movie]), 2)

            top_movies = dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

            return top_movies

    class Users(Movies):
        def dist_by_ratings_number(self):
            ratings_distribution = Counter()

            tmp = self.ratings.read_file()
            del tmp[0]

            for data in tmp:
                ratings_distribution[data[0]] += 1

            ratings_distribution = dict(sorted(ratings_distribution.items(), key=lambda item: item[1]))

            return ratings_distribution

        def dist_by_ratings_values(self, metric=Statistics.average):
            all_ratings = defaultdict(list)

            tmp = self.ratings.read_file()
            del tmp[0]

            for data in tmp:
                all_ratings[data[0]].append(float(data[2]))

            for user in all_ratings:
                all_ratings[user] = round(metric(all_ratings[user]), 2)

            all_ratings = dict(sorted(all_ratings.items(), key=lambda item: item[1]))

            return all_ratings

        def top_by_variance(self, n: int):
            all_ratings = defaultdict(list)

            tmp = self.ratings.read_file()
            del tmp[0]

            for data in tmp:
                all_ratings[data[1]].append(float(data[2]))

            for user in all_ratings:
                all_ratings[user] = round(Statistics.variance(all_ratings[user]), 2)

            all_ratings = dict(sorted(all_ratings.items(), key=lambda item: item[1], reverse=True)[:n])
            
            return all_ratings

class TestMovies:
    @classmethod
    def setup_class(cls):
        cls.mov = Movies('data/movies.csv')

    def test_dist_by_release(self):
        print(self.dist_by_release())
    
    def test_dist_by_genres(self):
        print(self.dist_by_release())

    def test_most_genres(self, n):
        print(self.most_genres())


class TestRatings:
    @classmethod
    def setup_class(cls):
        cls.ratings = Ratings('data/ratings.csv')
        cls.movies = Movies('data/movies.csv')
        cls.ratings_movies = Ratings.Movies(cls.ratings, cls.movies)
        cls.ratings_users = Ratings.Users(cls.ratings, cls.movies)

    def test_movies_dist_by_years(self):
        print(self.ratings_movies.dist_by_year())

    def test_movies_dist_by_rating(self):
        print(self.ratings_movies.dist_by_rating())

    def test_top_by_num_of_ratings(self, n):
        print(self.ratings_movies.top_by_num_of_ratings(n))

    def test_top_by_ratings(self, n):
        print(self.ratings_movies.top_by_ratings(n))

    def test_top_controversial(self, n):
        print(self.ratings_movies.top_controversial(n))

    def test_dist_by_ratings_number(self):
        print(self.ratings_users.dist_by_ratings_number())
    
    def test_dist_by_ratings_values(self):
        print(self.ratings_users.dist_by_ratings_values())
    
    def test_top_by_variance(self, n):
        print(self.ratings_users.top_by_variance(n))

def ratingsTest():
    rat = Ratings('data/ratings.csv')

    # testRatings = TestRatings()
    # testRatings.setup_class()
    # testRatings.test_movies_dist_by_years()
    # testRatings.test_movies_dist_by_rating()
    # testRatings.test_top_by_num_of_ratings(5)
    # testRatings.test_top_by_ratings(5)
    # testRatings.test_top_controversial(5)
    # testRatings.test_dist_by_ratings_number()
    # testRatings.test_dist_by_ratings_values()
    # testRatings.test_top_by_variance(5)

def moviesTest():
    mov = Movies('data/movies.csv')

    # testMovies = TestMovies()
    # testMovies.setup_class()
    # testMovies.test_dist_by_release()
    # testMovies.test_dist_by_genres()
    # testMovies.test_most_genres(5)

def main():
    moviesTest()
    ratingsTest()

if __name__ == '__main__':
    main()