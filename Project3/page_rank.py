import os
import sys
import math

import numpy
import pandas

# Generalized matrix operations:

def __extract_nodes(matrix):
    nodes = set()
    for col_key in matrix:
        nodes.add(col_key)
    for row_key in matrix.T:
        nodes.add(row_key)
    return nodes

def __make_square(matrix, keys, default=0.0):
    matrix = matrix.copy()
    
    def insert_missing_columns(matrix):
        for key in keys:
            if not key in matrix:
                matrix[key] = pandas.Series(default, index=matrix.index)
        return matrix

    matrix = insert_missing_columns(matrix) # insert missing columns
    matrix = insert_missing_columns(matrix.T).T # insert missing rows

    return matrix.fillna(default)

def __ensure_rows_positive(matrix):
    matrix = matrix.T
    for col_key in matrix:
        if matrix[col_key].sum() == 0.0:
            matrix[col_key] = pandas.Series(numpy.ones(len(matrix[col_key])), index=matrix.index)
    return matrix.T

def __normalize_rows(matrix):
    return matrix.div(matrix.sum(axis=1), axis=0)

def __euclidean_norm(series):
    return math.sqrt(series.dot(series))

# PageRank specific functionality:

def __start_state(nodes):
    if len(nodes) == 0: raise ValueError("There must be at least one node.")
    start_prob = 1.0 / float(len(nodes))
    return pandas.Series({node : start_prob for node in nodes})
