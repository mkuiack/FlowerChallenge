#!/usr/bin/env python

import pandas as pd
import numpy as np
import itertools
from typing import Tuple

# Define all flower types
data_columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z']

data_columns *= 2

for i in range(26*2):
    if i < 26:
        data_columns[i] = data_columns[i]+"S"
    elif i >= 26:
        data_columns[i] = data_columns[i]+"L"

data_columns.append("NameSize")

def parse_design_string(design_string: str) -> Tuple[str, str, list, int]:
    """
    Parse design string.

    Input:  Design string (string)
    Output: design name (str), flower size (str), flower type maxes (str), bouquet sum (int)
    """

    parsed_str = ""

    for char in design_string:
        if char.isalpha():
            parsed_str += char+","
        else:
            parsed_str += char

    parsed_list = parsed_str.split(",")

    return parsed_list[0], parsed_list[1], parsed_list[2:-1], int(parsed_list[-1])


def read_design(design_string: str) -> pd.DataFrame:
    """
    Read design sting, parse and generate all valid bouquet permutations.

    Input: Bouquet design (string)
    Output: All valid bouquet permutations (Dataframe)
    """

    name, sizes, flower_maxes, flower_sum = parse_design_string(design_string)

    permuts = pd.DataFrame(columns=data_columns)

    for flower_counts in itertools.product(*[range(1, int(n[:-1])+1) for n in flower_maxes]):
        if np.sum(flower_counts) == flower_sum:

            permuts = permuts.append(pd.Series(list(flower_counts)+[name+sizes],
                                               index=[flower[-1] + sizes
                                                      for flower in flower_maxes] + ["NameSize"],
                                               dtype=object), ignore_index=True).fillna(0)
    return permuts.astype(int, errors='ignore')


def make_bouquets(possible_designs: pd.DataFrame, flower_stock: pd.DataFrame) -> None:
    """
    Compare current flower stock to all valid bouquets, print the first constructable
    bouquet and update flower stock.

    Input: all valid bouquet designs (DataFrame)
    print constructed bouquet
    Output: updated flower stock (DataFrame)
    """

    # iterate through all permutations of given design
    for permutation in possible_designs.index:
        bouquet_df = possible_designs.iloc[permutation]

        # can't have negative flower stock
        if np.min((flower_stock[data_columns[:-1]] - bouquet_df[data_columns[:-1]]).values) >= 0:

            flower_stock[data_columns[:-1]] -= bouquet_df[data_columns[:-1]]

            str_bouquet = ""

            for key in bouquet_df[data_columns[:-1]].keys():
                if bouquet_df[key] == 0:
                    continue
                str_bouquet += str(int(bouquet_df[key]))+str(key[0])
            # print(bouquet_df)
            print(bouquet_df["NameSize"]+str_bouquet)
    return
#                new_bouquet = design_id+flower_size+str_bouquet
#                return design_id+flower_size+str_bouquet
#    return new_bouquet


def run_batch() -> None:
    """
    Run with the assumption that all inputs are first given then outputs printed
    """
    # Get designs
    input_designs = list(iter(input, ''))
    # Get Flowers
    input_flowers = list(iter(input, ''))

    # start with empty flower stock
    flower_stock = pd.DataFrame(np.zeros([1, 53]),
                                columns=data_columns, dtype=int)


    # Make bouquets in order of flower addition,
    # Getting flowers can be added to a loop for streaming bouquet making
    for flower in input_flowers:
        try:
            flower_stock[flower] += 1
        except KeyError:
            # invalid flower
            continue

        make_bouquets(input_designs, flower_stock)
    return


def run_streaming() -> None:
    """
    Run streaming valid bouquet outputs as new flowers are input to flower stock.
    """
    # Get designs
    input_designs = list(iter(input, ''))

    # Calculate all possible bouquet permutations once.
    design_permutations = pd.concat([read_design(bouquet_design)
                                     for bouquet_design in input_designs],
                                    ignore_index=True)

    # Start with empty flower stock.
    flower_stock = pd.DataFrame(np.zeros([1, 53]),
                                columns=data_columns, dtype=int)

    # Users add new flower, accumulated stock is checked against all bouquets.
    go = True
    while go:

        input_flower = input()

        if input_flower == "":
            go = False

        try:
            flower_stock[input_flower] += 1
        except KeyError:
            # invalid flower
            continue

        make_bouquets(design_permutations, flower_stock)
    return


if __name__ == "__main__":

    run_streaming()
