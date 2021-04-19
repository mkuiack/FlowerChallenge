#!/usr/bin/env python3

import pandas as pd
import numpy as np
from typing import Tuple, Union

class bloomon_operation():

    def __init__(self):
        # Define all flower types
        data_columns: list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z']*2
        for i in range(26*2):
            if i < 26:
                data_columns[i] = data_columns[i]+"S"
            elif i >= 26:
                data_columns[i] = data_columns[i]+"L"
        data_columns.append("NameSize")


        self.flower_stock: pd.DataFrame = pd.DataFrame(np.zeros([1, 53]),
                            columns=data_columns, dtype=int)

        self.all_designs: list[pd.DataFrame, str, str, str] = []


    def submit_designs(self) -> None:
        """
        Submit new design string to operation.
        """
        new_designs: list = list(iter(input, ''))


        for design_string in new_designs:

            name, sizes, flower_maxes, design_sum = self.parse_design_string(design_string)

            design_df = pd.DataFrame()

            design_df = design_df.append(pd.Series([int(flower[:-1]) for flower in flower_maxes],
                                                       index=[flower[-1]+sizes for flower in flower_maxes],
                                                       dtype=int), 
                                             ignore_index=True).astype(int, errors='ignore')

            self.all_designs.append([design_df, design_sum, 
                                      name+sizes, design_string])

    def return_designs(self) -> None:
        """
        Print all design strings input to this operation
        """
        print(np.array(self.all_designs)[:,3])


    def parse_design_string(self, design_string: str) -> Tuple[str, str, list, int]:
        """
        Parse design string.

        Input:  Design string (string)
        Output: design name (str), flower size (str), flower maxes and type (list), bouquet sum (int)
        """

        parsed_str = ""

        for char in design_string:
            if char.isalpha():
                parsed_str += char+","
            else:
                parsed_str += char

        parsed_list = parsed_str.split(",")

        return parsed_list[0], parsed_list[1], parsed_list[2:-1], int(parsed_list[-1])


    def add_flower(self) -> Union[str,None]:
        """
        User add flower to operation stock.
        """
        input_flower: str = input()

        if input_flower == "":
            return input_flower

        try:
            self.flower_stock[input_flower] += 1
        except KeyError:
            return None
            # invalid flower


    def check_stock(self) -> None:
        """
        All design strings are checked against the currently accumulated stock.
        Any valid bouquets are made (printed) and the stock is updated. 
        """
        for i in range(len(self.all_designs)):

            design = self.all_designs[i][0]
            design_sum =  self.all_designs[i][1]

            # if  you have at least 1 of all required flower type 
            # and total quantity greater than/equal to designsum 
            if np.all(self.flower_stock[design.keys()].ge(1)) and \
            (self.flower_stock[design.keys()].values.sum() >= int(design_sum)):

                # remaining stock is max (designMax-Stock, 0) ie remove all used flowers 
                remainder = pd.concat([self.flower_stock[design.keys()].subtract(design),
                                       self.flower_stock[design.keys()].multiply(0)]).max(level=0)

                # subtracted quantity is previous stock - remaining
                stock_sub = self.flower_stock[design.keys()] - remainder


                design_name =  self.all_designs[i][2]

                # output bouquet string
                for flower in stock_sub.keys():
                    design_name += str(int(stock_sub[flower])) + flower[0]
                print(design_name)

                # update stock
                self.flower_stock[design.keys()] = remainder


if __name__ == "__main__":

    # add new bloomon operation
    amsterdam_garden = bloomon_operation()

    # submit designs to the operation
    amsterdam_garden.submit_designs()

    # stream in new flowers, and create bouquets as they become possible.
    while True:

        new_flower = amsterdam_garden.add_flower()
        if new_flower == "":
            break

        amsterdam_garden.check_stock()

