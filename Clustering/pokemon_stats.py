# WillDaru22
#
# Acknowledgements
# Reading first N rows of csv file
# https://stackoverflow.com/questions/50490257/only-reading-first-n-rows-of-csv-file-with-csv-reader-in-python
# ndarray function
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html

import csv
import itertools
import numpy
import math


# takes in a string with a path to a CSV file formatted as in the link above, and returns the first 20 data points (
# without the Generation and Legendary columns but retaining all other columns) in a single structure.
def load_data(filepath):
    pokemon_data = []  # list to put pokemon data into
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # read in our csv file taking first row as dictionary names
        for row in itertools.islice(reader, 20):  # only read rows 1-20
            pokemon_dict = {"#": int(row["#"]), "Name": row["Name"], "Type 1": row["Type 1"], "Type 2": row["Type 2"],
                            "Total": int(row["Total"]), "HP": int(row["HP"]), "Attack": int(row["Attack"]),
                            "Defense": int(row["Defense"]), "Sp. Atk": int(row["Sp. Atk"]),
                            "Sp. Def": int(row["Sp. Def"]), "Speed": int(row["Speed"])}
            pokemon_data.append(pokemon_dict)  # add to list of pokemon
    return pokemon_data


# takes in one row from the data loaded from the previous function, calculates the corresponding x, y values for that
# Pokemon as specified above, and returns them in a single structure.
def calculate_x_y(stats):
    x = int(stats["Attack"])+int(stats["Sp. Atk"])+int(stats["Speed"])  # get offensive values
    y = int(stats["Defense"])+int(stats["Sp. Def"])+int(stats["HP"])  # get defensive values
    return x, y  # return as tuple


# performs single linkage hierarchical agglomerative clustering on the Pokemon with the (x,y) feature representation,
# and returns a data structure representing the clustering.
def hac(dataset):  # pass in a list of tuples of length m.  (so a 20 x 2 list)
    if not dataset:
        return
    clusters = {}
    number = 0
    cluster_array = []
    cluster_array = numpy.ndarray(shape=(len(dataset)-1, 4))  # create our m-1 x 4 array
    for i, cluster in enumerate(dataset):  # giving each item in dataset it's own cluster index
        clustlist = [cluster]
        clusters[i] = {'number': i, 'cluster': clustlist}
        number += 1
    for cluster1 in clusters.values():  # get distances for every cluster to every other cluster
        # print(cluster1['cluster'])  # debug
        distances = {}
        for j, cluster2 in enumerate(clusters.values()):  # remember to not use distance to current point
            # print(cluster2, j)
            if cluster1 != cluster2:  # dont check self
                distances[cluster2["number"]] = (euclidean_distance(cluster1["cluster"], cluster2["cluster"]))
        cluster1['distances'] = distances
        cluster1["data points"] = 1

    for row in cluster_array:  # start filling in array
        row[0], row[1], row[2], row[3] = calculate_minimum_distance(clusters)  # fill in all the data points
        # update the clusters dictionary with the new point
        clusters[number] = {'number': number, 'cluster': clusters[row[0]]['cluster'] + clusters[row[1]]['cluster'],
                            'data points': row[3]}
        del(clusters[row[0]])
        del(clusters[row[1]])
        # added new cluster and removed combined clusters.  Recalculate distances now
        for cluster1 in clusters.values():  # get distances for every cluster to every other cluster
            # print(cluster1['cluster'])  # debug
            distances = {}
            for j, cluster2 in enumerate(clusters.values()):  # remember to not use distance to current point
                # print(cluster2, j)
                if cluster1 != cluster2:  # dont check self
                    distances[cluster2["number"]] = (euclidean_distance(cluster1["cluster"], cluster2["cluster"]))
            cluster1['distances'] = distances
        number += 1
    return cluster_array


# distance between points = sqrt((x2-x1)^2 + (y2-y1)^2)
def euclidean_distance(p1, p2):  # helper function for euclidean distance
    # print(p1, p2)  # debug
    min_dist = 2130000000  # big ole number here to start
    for tup1 in p1:  # list of tuples now, loop through and get points between
        for tup2 in p2:
            min_dist = min(min_dist, math.sqrt(math.pow((tup2[0] - tup1[0]), 2) + math.pow((tup2[1]-tup1[1]), 2)))
    return min_dist


# helper method to calculate minimum distance in the dictionary and return the points the distance is between
def calculate_minimum_distance(cluster_dict):
    current_p1 = 0
    current_p2 = 0
    current_min = 2130000000  # hoping we dont get above this for distance
    data_points = 0
    for diction in cluster_dict.values():
        for key, dist in diction["distances"].items():
            if dist < current_min:  # check for min distance
                current_p1 = diction["number"]
                current_p2 = key
                current_min = dist
                data_points = diction["data points"]  # first part of data points to add
            elif dist == current_min:  # check for ties
                if diction["number"] < current_p1:  # check if new i index is smaller
                    current_p1 = diction["number"]
                    current_p2 = key
                    current_min = dist
                    data_points = diction["data points"]  # first part of data points to add
                elif diction["number"] == current_p1:  # if first indices are same
                    if key < current_p2:  # check for backup tiebreaker
                        current_p1 = diction["number"]
                        current_p2 = key
                        current_min = dist
                        data_points = diction["data points"]  # first part of data points to add
    # min found and established, add second part of data points using key
    for point in cluster_dict.values():
        if current_p2 == point["number"]:  # find matching key
            data_points += point["data points"]  # add second part of data points
    return current_p1, current_p2, current_min, data_points
