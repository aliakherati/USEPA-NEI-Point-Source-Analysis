import pandas as pd

def filter_scc_data(df: pd.DataFrame, keywords: str | list[str] | None = None, scc_level: int | None = None) -> pd.DataFrame:
    """
    Filter SCC data based on data category, status and optional keyword search in SCC levels
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing SCC data
    keywords : str or list of str, optional
        One or more keywords to search in specified SCC level
    scc_level : int, optional
        Which SCC level to search keyword in. Must be one of: 1, 2, 3, 4
        
    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe
    """
    # Basic filters
    filtered_df = df[
        (df["data category"] == "Point") &
        (df["status"] == "Active")
    ]
    
    # Apply keyword filter if both keywords and scc_level are provided
    if keywords and scc_level:
        level_map = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        if scc_level not in level_map:
            raise ValueError(f"scc_level must be one of {list(level_map.keys())}")
            
        scc_level_str = f"scc level {level_map[scc_level]}"
        
        # Convert single keyword to list
        if isinstance(keywords, str):
            keywords = [keywords]
            
        # Filter for any of the keywords
        mask = filtered_df[scc_level_str].str.contains(keywords[0], case=False, na=False)
        for keyword in keywords[1:]:
            mask |= filtered_df[scc_level_str].str.contains(keyword, case=False, na=False)
        filtered_df = filtered_df[mask]
        
        # Print unique values after filtering, one per line
        print(f"\nUnique values in {scc_level_str} after filtering:")
        for i, value in enumerate(sorted(filtered_df[scc_level_str].unique())):
            print(f"{i+1}: {value}")
    
    return filtered_df

def filter_poll_data(df: pd.DataFrame, poll: str | list[str], scc_set: set) -> pd.DataFrame:
    """
    Filter dataframe for specific pollutant(s) and valid stack heights, limiting to provided SCCs
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe to filter
    poll : str or list of str
        Pollutant(s) to filter for
    scc_set : set
        Set of SCC codes to filter for
        
    Returns
    -------
    pandas.DataFrame
        Filtered dataframe
    """
    # Convert single pollutant to list
    if isinstance(poll, str):
        poll = [poll]
        
    filtered_df = df[
        (df.poll.isin(poll)) &
        (df.stkhgt.notna()) &
        (df["scc"].isin(scc_set))
    ]
    
    return filtered_df

def filter_poll_data_with_capacity(df: pd.DataFrame, poll: str | list[str], scc_set: set) -> pd.DataFrame:
    """
    Filter dataframe for specific pollutant(s), valid stack heights, and design capacity data, 
    limiting to provided SCCs
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe to filter
    poll : str or list of str
        Pollutant(s) to filter for
    scc_set : set
        Set of SCC codes to filter for
        
    Returns
    -------
    pandas.DataFrame
        Filtered dataframe with stkhgt, design_capacity, and design_capacity_units columns
    """
    # Convert single pollutant to list
    if isinstance(poll, str):
        poll = [poll]
        
    # Check if design capacity columns exist
    required_columns = ['stkhgt', 'design_capacity', 'design_capacity_units']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
        
    filtered_df = df[
        (df.poll.isin(poll)) &
        (df.stkhgt.notna()) &
        (df["scc"].isin(scc_set))
    ]
    
    return filtered_df[['stkhgt', 'design_capacity', 'design_capacity_units']]