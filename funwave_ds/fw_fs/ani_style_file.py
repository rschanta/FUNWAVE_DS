import pandas as pd

def read_ani_style_file(path):


    ## Read the style file
    df = pd.read_csv(path)
    
    ## Initialize variable lists
    static_variables = []
    dynamic_variables = []
    attribute_labels = []
    animation_variables = {}
    
    ## Determine which values are represented
    essential_columns = ['Key', 'Type', 'Value']
    
    extra_attribute_columns = []
    for column in df.columns:
        if column not in essential_columns:
            extra_attribute_columns.append(column)
            
            
    # Iterate through the DataFrame rows
    for _, row in df.iterrows():
        
        # Get variable name and type
        key = row['Key']
        var_type = row.get('Type', '')
        
    
        # Get other attributes in this row
        extra_attributes = {col: row[col] for col in extra_attribute_columns if pd.notna(row[col])}
        
        
        
        # Get Animation Variables
        if var_type == 'animation':
            animation_variables[key] = row['Value']
            
        # Get Static Variables
        elif var_type == 'static':
            static_variables.append({'key': key, **extra_attributes})
        
        # Get Dynamic Variables
        elif var_type == 'dynamic':
            dynamic_variables.append({'key': key, **extra_attributes})
        
        # Get Attribute Labels
        elif var_type == 'attribute':
            attribute_labels.append(key)
    
    return static_variables, dynamic_variables, attribute_labels,animation_variables
