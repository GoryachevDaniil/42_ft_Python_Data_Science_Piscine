import os
import sys
import datetime as dt
import datetime
import functools
from functools import reduce
import collections
from collections import Counter, defaultdict, OrderedDict
import urllib
import json
import re
from bs4 import BeautifulSoup
import requests




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

class Tags:
    def __init__(self, path_to_the_file):
        self.file = path_to_the_file

    def most_words(self, n):
        tags = {}
        for ind, line in enumerate(open(self.file)):
            if ind == 0:
                continue
            tag = line.split(",", 2)[2].rsplit(',', 1)[0]
            tags[tag] = len(tag.split(" "))

        big_tags = sorted(tags.items(), key=lambda item: (-item[1]))[:n]

        return dict(big_tags)

    def longest(self, n):
        tags = {}
        for ind, line in enumerate(open(self.file)):
            if ind == 0:
                continue
            tag = line.split(",", 2)[2].rsplit(',', 1)[0]
            tags[tag] = len(tag)

        big_tags = sorted(tags.items(), key=lambda item: (-item[1]))[:n]
        big_tags = map(lambda x: x[0], big_tags)
        return list(big_tags)

    def most_words_and_longest(self, n):
        top_words = list(self.most_words(n).keys())
        top_len = self.longest(n)
        return list(set(top_len + top_words))

    def most_popular(self, n):
        tags = {}
        for ind, line in enumerate(open(self.file)):
            if ind == 0:
                continue
            tag = line.split(",", 2)[2].rsplit(',', 1)[0]
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
        popular_tags = sorted(tags.items(), key=lambda item: (-item[1]))[:n]
        return dict(popular_tags)

    def tags_with(self, word):
        tags = set()
        for ind, line in enumerate(open(self.file)):
            if ind == 0:
                continue
            tag = line.split(",", 2)[2].rsplit(',', 1)[0]
            for i in tag.split(" "):
                if i in word:
                    tags.add(tag)
                    break

        return list(tags)

class Links:
    def __init__(self, path_to_the_file):
        self.file = path_to_the_file

        self.movie_imdb_ID = {}
        for i, line in enumerate(open(self.file)):
            if (i == 0): continue
            mov = line.split(',')[0]
            self.movie_imdb_ID[mov] = line.split(',')[1]
        range_nm = list(map(lambda x: str(x), range(1, 3)))
        self.data = self.get_imdb(range_nm, ['Director', 'Also known as', 'Budget', 'Gross worldwide', 'Runtime'])

    def get_links_by_movieId(self, idx):
        for i, line in enumerate(open(self.file)):
            if (i == 0): continue
            if (int(line.split[','][0] == idx)):
                return line

    def get_imdb(self, list_of_movies, list_of_fields):
        imdb_info = []
        for mov in list_of_movies:
            imdb = [mov]
            url = "http://www.imdb.com/title/tt{}".format(self.movie_imdb_ID[mov])
            response = requests.get(url, headers={'User-Agent': 'PYTHON'})
            soup = BeautifulSoup(response.text, 'lxml')
            tags = soup.find_all('li', role='presentation', class_='ipc-metadata-list__item')
            for field in list_of_fields:
                for tag in tags:
                    if (tag.text.find(field) != -1):
                        imdb.append(tag.text.replace(field, ''))
                        break
            imdb_info.append(imdb)

            imdb_info = sorted(imdb_info, key=lambda x: -int(x[0]))
        return imdb_info

    def top_directors(self, n):
        directors = [mov[1] for mov in self.data]
        cnt = Counter(directors)
        directors = dict(cnt)
        sorted_pairs = sorted(directors.items(), key=lambda item: -item[1])
        directors = OrderedDict()
        for k, v in sorted_pairs:
            if k not in directors:
                directors[k] = v
                if len(directors) == n:
                    break
        return dict(directors)

    def most_expensive(self, n):
        budgets = {}
        for mov in self.data:
            budgets[mov[2]] = self.summa_to_int(mov[3])
        sorted_pairs = sorted(budgets.items(), key=lambda item: item[1], reverse=True)
        budgets = OrderedDict()
        for k, v in sorted_pairs:
            if k not in budgets:
                budgets[k] = v
                if len(budgets) == n:
                    break

        return dict(budgets)

    def summa_to_int(self, string):
        return int(string[1::].split(' ')[0].replace(',', ''))

    def most_profitable(self, n):
        profits = {}
        for mov in self.data:
            profits[mov[2]] = self.summa_to_int(mov[4]) - self.summa_to_int(mov[3])
        sorted_pairs = sorted(profits.items(), key=lambda item: item[1], reverse=True)
        profits = OrderedDict()
        for k, v in sorted_pairs:
            if k not in profits:
                profits[k] = v
                if len(profits) == n:
                    break

        return dict(profits)

    def longest(self, n):
        runtimes = {}
        for mov in self.data:
            runtimes[mov[2]] = self.time_to_int(mov[5])
        sorted_pairs = sorted(runtimes.items(), key=lambda item: item[1], reverse=True)
        runtimes = OrderedDict()
        for k, v in sorted_pairs:
            if k not in runtimes:
                runtimes[k] = v
                if len(runtimes) == n:
                    break

        return dict(runtimes)

    def time_to_int(self, string):
        result = 0
        if 'hour' in string:
            result += int(string.split('hour')[0]) * 60
        if 'minutes' in string:
            result += int(string.split(' ')[-2])
        return result

    def top_cost_per_minute(self, n):
        costs = {}
        for mov in self.data:
            costs[mov[2]] = round(self.summa_to_int(mov[3]) / self.time_to_int(mov[5]), 2)
        sorted_pairs = sorted(costs.items(), key=lambda item: item[1], reverse=True)
        costs = OrderedDict()
        for k, v in sorted_pairs:
            if k not in costs:
                costs[k] = v
                if len(costs) == n:
                    break

        return dict(costs)

class TestMovies:
    @classmethod
    def setup_class(cls):
        cls.movies = Movies('data/movies.csv')

    def test_dist_by_release(self):
        self.movies.dist_by_release()
    
    def test_dist_by_genres(self):
        self.movies.dist_by_release()

    def test_most_genres(self, n):
        self.movies.most_genres(n)


class TestRatings:
    @classmethod
    def setup_class(cls):
        cls.ratings = Ratings('data/ratings.csv')
        cls.movies = Movies('data/movies.csv')
        cls.ratings_movies = Ratings.Movies(cls.ratings, cls.movies)
        cls.ratings_users = Ratings.Users(cls.ratings, cls.movies)

    def test_movies_dist_by_years(self):
        self.ratings_movies.dist_by_year()

    def test_movies_dist_by_rating(self):
        self.ratings_movies.dist_by_rating()

    def test_top_by_num_of_ratings(self, n):
        self.ratings_movies.top_by_num_of_ratings(n)

    def test_top_by_ratings(self, n):
        self.ratings_movies.top_by_ratings(n)

    def test_top_controversial(self, n):
        self.ratings_movies.top_controversial(n)

    def test_dist_by_ratings_number(self):
        self.ratings_users.dist_by_ratings_number()
    
    def test_dist_by_ratings_values(self):
        self.ratings_users.dist_by_ratings_values()
    
    def test_top_by_variance(self, n):
        self.ratings_users.top_by_variance(n)

class Tests:
    def setup_class(self):
        self.tags = Tags('data/tags.csv')
        self.links = Links('data/links.csv')

    def test_tags_most_words(self):
        result = self.tags.most_words(10)
        return (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                    set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_tags_longest(self):
        result = self.tags.longest(10)
        return (isinstance(result, list) and
                (set(map(type, result)) == {str}))

    def test_tags_most_words_and_longest(self):
        result = self.tags.most_words_and_longest(232)
        return (isinstance(result, list) and
                set(map(type, result)) == {str})

    def test_tags_most_popular(self):
        result = self.tags.most_popular(10)
        return (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                    set(map(type, result.keys())) == {str}) and
                sorted(result.values(), reverse=True) == list(result.values()))

    def test_get_imdb(self):
        result = self.links.get_imdb(['1', '2', '3', '4', '5'], ['director', 'name', 'genre', 'actor'])
        return (isinstance(result, list) and
                set(map(type, result)) == {list} and
                sorted(result, reverse=True, key=lambda x: x[0]) == list(result))

    def test_top_directors(self):
        self.links.get_imdb(['1', '2', '3', '4', '5'], ['director', 'name', 'genre', 'actor'])
        result = self.links.top_directors(3)
        return (isinstance(result, dict) and
                (set(map(type, result.values())) == {int} and
                    set(map(type, result.keys())) == {str}) and
                sorted(result, reverse=True, key=lambda x: x[1]) == list(result))

def tags_n_linksTest():
    testTags_n_Links = Tests()
    testTags_n_Links.setup_class()

    print(testTags_n_Links.test_tags_most_words())
    print(testTags_n_Links.test_tags_longest())
    print(testTags_n_Links.test_tags_most_words_and_longest())
    print(testTags_n_Links.test_tags_most_popular())
    print(testTags_n_Links.test_get_imdb())
    
    testTags_n_Links.test_top_directors()

def ratingsTest():
    testRatings = TestRatings()
    testRatings.setup_class()

    # testRatings.test_movies_dist_by_years()
    # testRatings.test_movies_dist_by_rating()
    # testRatings.test_top_by_num_of_ratings(5)
    # testRatings.test_top_by_ratings(5)
    # testRatings.test_top_controversial(5)
    # testRatings.test_dist_by_ratings_number()
    # testRatings.test_dist_by_ratings_values()
    # testRatings.test_top_by_variance(5)

def moviesTest():
    testMovies = TestMovies()
    testMovies.setup_class()
    
    # testMovies.test_dist_by_release()
    # testMovies.test_dist_by_genres()
    # testMovies.test_most_genres(5)

def main():
    moviesTest()
    ratingsTest()
    tags_n_linksTest()





if __name__ == '__main__':
    main()