#!/usr/bin/env python

import pandas as pd
import numpy as np
import itertools

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


def parse_design_string(design_string):
    """
    Parse design string
    return design name, flower size, flower type maxes, bouquet sum
    """

    parsed_str = ""

    for char in design_string:
        if char.isalpha():
            parsed_str += char+","
        else:
            parsed_str += char

    parsed_str = np.array(parsed_str.split(","))

    return parsed_str[0], parsed_str[1], parsed_str[2:-1], int(parsed_str[-1])


def read_design(design_string):
    """
    Read the bouquet design string and output all
    possible bouquet permutations as Dataframe
    """

    name, sizes, flower_maxes, flower_sum = parse_design_string(design_string)

    permuts = pd.DataFrame(columns=data_columns, dtype=int)

    for r in itertools.product(*[range(1, int(n[:-1])+1) for n in flower_maxes]):
        if np.sum(r) == flower_sum:
            permuts = permuts.append(pd.Series(list(r),
                                               index=[flower[-1]+sizes
                                                      for flower in flower_maxes],
                                               dtype=int),
                                     ignore_index=True).fillna(0)
    return permuts


def make_bouquets(all_designs, flower_stock):
    """
    Take list of all design codes, and DataFrame of current flower stock.
    print valid bouquets and update flower stock
    """
    # iterating through designs
    for bouquet_design in all_designs:

        design_id = str(bouquet_design[0])
        flower_size = bouquet_design[1]

        design_perm_df = read_design(bouquet_design)

        # iterate through all permutations of given design
        for permutation in design_perm_df.index:
            bouquet_df = design_perm_df.iloc[permutation]

            # can't have negative flower stock
            if np.min((flower_stock - bouquet_df).values) >= 0:

                flower_stock -= bouquet_df

                str_bouquet = ""

                for key in bouquet_df.keys():
                    if bouquet_df[key] == 0:
                        continue
                    str_bouquet += str(int(bouquet_df[key]))+str(key[0])
                print(design_id+flower_size+str_bouquet)
#                new_bouquet = design_id+flower_size+str_bouquet
#                return design_id+flower_size+str_bouquet
#    return new_bouquet


def run_batch():
    """
    Run with the assumption that all inputs are first given then outputs printed
    """
    # Get designs
    input_designs = list(iter(input, ''))
    # Get Flowers
    input_flowers = list(iter(input, ''))

    # start with empty flower stock
    flower_stock = pd.DataFrame(np.zeros([1, 52]),
                                columns=data_columns, dtype=int)

    output_bouquets = []

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


def run_streaming():
    """
    Run streaming valid bouquet outputs as new flowers are input to flower stock.
    """
    # Get designs
    input_designs = list(iter(input, ''))

    # start with empty flower stock
    flower_stock = pd.DataFrame(np.zeros([1, 52]),
                                columns=data_columns, dtype=int)

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

        make_bouquets(input_designs, flower_stock)
    return


if __name__ == "__main__":

    run_streaming()
