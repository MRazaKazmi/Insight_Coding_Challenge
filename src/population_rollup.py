# Written by: Mohammad Raza Kazmi
# Using: python3
# For: Insight Data Engineering Fellowship
# Date: 19 October 2020

# The purpose of this program is to process an input file which contains population information of core areas
# which is detailed to the tract level and produce an output file which rollsup the information to the core area
# level


# importing the required libraries

import sys
import csv


class Core_Area():
    """
    Class for tracking core area information such as core area code, core area title, number of tracts,
    the area's 2000 population, the area's 2010 population, the area's population percent change between 2000 and 2010
    """
    def __init__(self, core_area_code, core_area_title, population_00, population_10, population_percent_change):
        
        self.core_area_code = core_area_code
        self.core_area_title = core_area_title
        self.num_of_tracts = 1
        self.population_00_list = [population_00]
        self.population_10_list = [population_10]
        self.population_percent_change_list = [population_percent_change]

    def add_tract(self):
        """
        Adds a tract to the core area by increasing the number by 1
        """
        self.num_of_tracts += 1
        
    def add_population_00(self, population_00):
        """
        Adds the tract's 2000 population the core area's list of 2000 population
        """
        self.population_00_list.append(population_00)

    def add_population_10(self, population_10):
        """
        Adds the tract's 2010 population the core area's list of 2010 population
        """
        self.population_10_list.append(population_10)

    def add_population_percent_change(self, population_percent_change):
        """
        Adds the tract's population percent change the core area's list of population percent change
        """
        self.population_percent_change_list.append(population_percent_change)



# defining utility functions

def add_population(population_list):
    """Sums populations of different tracts in core area"""
    total_population = sum(population_list)
    return total_population

def take_average_population_percent_change(population_percent_change_list):
    """Takes mean of population percent change of different tracts in core area"""
    average_population_percent_change = sum(population_percent_change_list) / len(population_percent_change_list)
    
    rounded_average_population_percent_change = round(average_population_percent_change, 2)

    return rounded_average_population_percent_change



class Core_Area_Process:
    """
    Class for processing core area file, taking the input file and output file paths as inputs
    """
    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile
        self.outputfile = outputfile

    def process_file(self): 

        # creating core area dictionary
        core_area_dict = {}

        try:
            input_file = open(self.inputfile, "r")
        except Exception as e:
            raise type(e)("Failed to open input file")

        # removing header
        input_file.readline()

        # iterating line by line to bypass memory issues arising from larger files
        for line in input_file:

            # separating the fields based on ',' and accounting for the double quoted 
            # core area title field
            fields = [ '{}'.format(x) for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0] ]
            
            try:
                core_area_code = int(fields[7])
                core_area_title = f'"{fields[8]}"'
                population_00 = int(fields[12].replace(',', ''))
                population_10 = int(fields[14].replace(',', ''))
                population_percent_change = float(fields[17])
            except Exception as e:
                continue
            
            # checking for missing values and skipping these if any
            if (core_area_code == '' or core_area_title == '""' or population_00 == '' or population_10 == ''or population_percent_change == ''):
                continue

            # checking if core area code, core area title in dictionary keys
            # if key present, then add tract number by 1, append the 2000 and
            # 2010 population and population percent change to the respective lists
            # if key absent, instantiate a new core area object with the information
            if (core_area_code, core_area_title) in core_area_dict.keys():
                core_area_dict[(core_area_code, core_area_title)].add_tract()
                core_area_dict[(core_area_code, core_area_title)].add_population_00(population_00)
                core_area_dict[(core_area_code, core_area_title)].add_population_10(population_10)
                core_area_dict[(core_area_code, core_area_title)].add_population_percent_change(population_percent_change)
            else:
                core_area_dict[(core_area_code, core_area_title)] = Core_Area(core_area_code, core_area_title,population_00,population_10, population_percent_change)

        return core_area_dict


    def save_file(self, core_area_dict):
        """
        Saves result as a csv file
        """
        
        try:
            with open(self.outputfile, "w+") as output_file:
            
                # iterating over each dictionary value and calcualting aggregated view using the Core_Area
                # class' methods and utility functions
                for key, value in core_area_dict.items():
                            
                    total_population_00 = add_population(value.population_00_list)

                    total_population_10 = add_population(value.population_10_list)

                    average_population_percent_change = take_average_population_percent_change(value.population_percent_change_list)

                    output_list = [value.core_area_code, value.core_area_title, value.num_of_tracts,total_population_00,total_population_10,
                        average_population_percent_change]
                
                    output_str = "{},{},{},{},{},{}\n".format(output_list[0], output_list[1], output_list[2], output_list[3], output_list[4], output_list[5])
                    output_file.write(output_str)
                    
                output_file.close()

        except Exception as e:
                raise type(e)("Failed to write output file")



if __name__ == "__main__":

    input_file, output_file = sys.argv[1], sys.argv[2]

    population_rollup = Core_Area_Process(input_file, output_file)
    results_dict = population_rollup.process_file()
    population_rollup.save_file(results_dict)

