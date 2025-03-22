from .assertions import assert_design_matrix_csv, assert_design_matrix_dict

import pandas as pd
import numpy as np
from itertools import product

# Fortran numbers
def convert_to_number(value):
    try:
        # Convert float: will work for ints/floats, strings fail
        float_value = float(value)
        
        # Convert to inter if not '.' is found in the original input string
        if '.' in str(value).strip():
            return float_value
        # Case to return int: if no decimal point is provided
        else: 
            return int(float_value)
        
    # Case to return string: if conversion to float fails
    except ValueError:
        return value



def find_combinations_from_csv(matrix_path):
    
    # Read in the Matrix
    df = pd.read_csv(matrix_path,
                     dtype=str,
                     na_values=["", "NULL", "NA"])
    # Assert Conditions
    df = assert_design_matrix_csv(df)

    # Dictionary: key = Parameter, value = list of values it assumes
    param_ranges = {}
    
    # Find every unique PARAMETER represented in the matrix 
    for name, group in df.groupby('VAR'):
        print(name)
        
        # List: contains every VALUE the parameter assumes
        val_list = []
        # Within each group
        for i,row in group.iterrows():
            
            # If constant (CON), just append to the list
            if not pd.isna(row['CON']):
                # Convert as necessary
                value = convert_to_number(row['CON'])
                val_list.append(value)
                print(f"\t• CONSTANT: {row['CON']}")
                
            # If ranged, construct the range
            elif not (pd.isna(row['LO']) & pd.isna(row['HI']) & pd.isna(row['NUM'])):
                # Convert as necessary
                val_lo = convert_to_number(row['LO'])
                val_hi = convert_to_number(row['HI'])
                val_num = convert_to_number(row['NUM'])
                
                # Construct the linspace and append
                val_list.extend(np.linspace(val_lo,val_hi,val_num))
                print(f"\t• RANGED: np.linspace({row['LO']},{row['HI']}, {row['NUM']})")
        
        # Append to dictionary                
        param_ranges[name] = val_list
        
    # Find all combinations and convert to dataframe
    combinations = list(product(*param_ranges.values()))
    dfv = pd.DataFrame(combinations, columns=param_ranges.keys())
    
    return dfv



def find_combinations_from_dict(input_dict):
    # 
    print('\nRANGES OF FUNWAVE-TVD VALUES' + '=' * (80 - len('\nRANGES OF FUNWAVE-TVD VALUES')))
    # Assert condition
    assert_design_matrix_dict(input_dict)
    # Loop through each category
    
    param_ranges = {}
    for category, category_dict in input_dict.items():
        print(f'{category}' + '-' * (80 - len(category)))
        
        
        # Loop through each FUNWAVE parameter
        for FW_PARAM_NAME, FW_PARAM_VALUES in category_dict.items():
            val_list = []
            print(f'\t{FW_PARAM_NAME}')
            
            # If value is just a string, add to list
            if isinstance(FW_PARAM_VALUES, str):
                # Convert and append to list
                value =  convert_to_number(FW_PARAM_VALUES)
                val_list.append(value)
                print(f'\t\t• CONSTANT: {FW_PARAM_VALUES}')
                
            # If a tuple, it's a ranged parameter
            elif isinstance(FW_PARAM_VALUES, tuple):
                print(f"\t\t• RANGED: np.linspace({FW_PARAM_VALUES[0]},{FW_PARAM_VALUES[1]},{FW_PARAM_VALUES[2]})")
                val_list.extend(np.linspace(FW_PARAM_VALUES[0],FW_PARAM_VALUES[1],FW_PARAM_VALUES[2]))
            
            # If value is a list, it's either a list/ranged parameter
            elif isinstance(FW_PARAM_VALUES, list):
                for entry in FW_PARAM_VALUES:
                    # Deal with constants
                    if isinstance(entry,str):
                        value =  convert_to_number(entry)
                        val_list.append(value)
                        print(f'\t\t• CONSTANT: {value}')
                        
                    # Deal with ranges
                    if isinstance(entry,tuple):
                        print(f"\t\t• RANGED: np.linspace({entry[0]},{entry[1]},{entry[2]})")
                        val_list.extend(np.linspace(entry[0],entry[1],entry[2]))
                        
            # Add onto ranges
            param_ranges[FW_PARAM_NAME] = val_list
    
    # Find all combinations and convert to dataframe
    combinations = list(product(*param_ranges.values()))
    dfv = pd.DataFrame(combinations, columns=param_ranges.keys())
    
    print('='*80)
    return dfv


def find_combinations(matrix_dict=None,
                      matrix_csv= None):
      # Assert that both are not specified
      assert not (matrix_dict is not None 
                  and matrix_csv is not None), "Choose either dictionary OR CSV, not both!"
      # Deal with the csv version
      if matrix_csv:
            df_permutations = find_combinations_from_csv(matrix_csv)
      # Deal with the dictionary version
      elif matrix_dict:
            df_permutations = find_combinations_from_dict(matrix_dict)
      # Raise error if both are none
      else:
            raise ValueError('Need either matrix_csv or matrix_dict!')
      
      return df_permutations