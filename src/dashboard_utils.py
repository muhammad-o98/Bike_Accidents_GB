# src/dashboard_utils.py
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple

def filter_dataframe(
    df: pd.DataFrame,
    year_range: Optional[Tuple[int, int]] = None,
    severity: Optional[List[str]] = None,
    gender: Optional[List[str]] = None,
    age_groups: Optional[List[str]] = None,
    road_conditions: Optional[List[str]] = None,
    weather_conditions: Optional[List[str]] = None,
    road_type: Optional[List[str]] = None,
    light_conditions: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Apply multiple filters to the dataframe based on dashboard selections.
    
    Args:
        df: Input dataframe
        year_range: Tuple of (min_year, max_year)
        severity: List of severity levels to include
        gender: List of genders to include
        age_groups: List of age groups to include
        road_conditions: List of road conditions to include
        weather_conditions: List of weather conditions to include
        road_type: List of road types to include
        light_conditions: List of light conditions to include
    
    Returns:
        Filtered dataframe
    """
    filtered_df = df.copy()
    
    # Filter by year range
    if year_range:
        min_year, max_year = year_range
        filtered_df = filtered_df[
            (filtered_df['year'] >= min_year) & 
            (filtered_df['year'] <= max_year)
        ]
    
    # Filter by categorical columns
    filter_mapping = {
        'severity': severity,
        'gender': gender,
        'age_grp': age_groups,
        'road_conditions': road_conditions,
        'weather_conditions': weather_conditions,
        'road_type': road_type,
        'light_conditions': light_conditions
    }
    
    for column, values in filter_mapping.items():
        if values and column in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[column].isin(values)]
    
    return filtered_df

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate key performance indicators from the filtered dataframe.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with KPI values
    """
    return {
        'total_accidents': len(df),
        'total_casualties': df['number_of_casualties'].sum() if 'number_of_casualties' in df.columns else 0,
        'total_vehicles': df['number_of_vehicles'].sum() if 'number_of_vehicles' in df.columns else 0,
        'fatal_accidents': len(df[df['severity'] == 'Fatal']) if 'severity' in df.columns else 0,
        'serious_accidents': len(df[df['severity'] == 'Serious']) if 'severity' in df.columns else 0,
        'slight_accidents': len(df[df['severity'] == 'Slight']) if 'severity' in df.columns else 0,
        'avg_casualties_per_accident': df['number_of_casualties'].mean() if 'number_of_casualties' in df.columns else 0,
        'year_range': f"{df['year'].min()}-{df['year'].max()}" if 'year' in df.columns and len(df) > 0 else "N/A"
    }

def group_rare_categories(
    series: pd.Series, 
    min_count: int = 100, 
    other_label: str = "Other"
) -> pd.Series:
    """
    Group rare categories (with count < min_count) into 'Other' category.
    
    Args:
        series: Pandas Series with categorical data
        min_count: Minimum count threshold for keeping category separate
        other_label: Label for grouped rare categories
    
    Returns:
        Series with rare categories grouped
    """
    value_counts = series.value_counts()
    rare_categories = value_counts[value_counts < min_count].index
    
    # Replace rare categories with 'Other'
    result = series.copy()
    result.loc[result.isin(rare_categories)] = other_label
    
    return result

def prepare_time_series_data(df: pd.DataFrame, freq: str = 'year') -> pd.DataFrame:
    """
    Prepare data for time series visualization.
    
    Args:
        df: Input dataframe
        freq: Frequency for aggregation ('year', 'month', 'day_of_week')
    
    Returns:
        DataFrame with time-based aggregation
    """
    if freq == 'year':
        return df.groupby('year').size().reset_index(name='count')
    elif freq == 'month':
        return df.groupby(['year', 'month']).size().reset_index(name='count')
    elif freq == 'day_of_week':
        # Define proper day order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['day_of_week'].value_counts()
        day_df = pd.DataFrame({'day_of_week': day_order})
        day_df['count'] = day_df['day_of_week'].map(day_counts).fillna(0)
        return day_df
    else:
        return df.groupby(freq).size().reset_index(name='count')

def prepare_stacked_bar_data(
    df: pd.DataFrame, 
    x_column: str, 
    color_column: str
) -> pd.DataFrame:
    """
    Prepare data for stacked bar charts.
    
    Args:
        df: Input dataframe
        x_column: Column for x-axis grouping
        color_column: Column for color/stack grouping
    
    Returns:
        Crosstab DataFrame suitable for stacked plotting
    """
    return pd.crosstab(df[x_column], df[color_column])

def prepare_correlation_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare data for correlation analysis between numeric variables.
    
    Args:
        df: Input dataframe
    
    Returns:
        Correlation matrix DataFrame
    """
    numeric_cols = ['speed_limit', 'number_of_vehicles', 'number_of_casualties', 'severity_numeric']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) > 1:
        return df[available_cols].corr()
    else:
        return pd.DataFrame()

def get_top_categories(
    df: pd.DataFrame, 
    column: str, 
    top_n: int = 10
) -> List[str]:
    """
    Get top N categories by count for a given column.
    
    Args:
        df: Input dataframe
        column: Column name to analyze
        top_n: Number of top categories to return
    
    Returns:
        List of top category names
    """
    if column in df.columns:
        return df[column].value_counts().head(top_n).index.tolist()
    return []

def prepare_severity_analysis(df: pd.DataFrame, by_column: str) -> pd.DataFrame:
    """
    Prepare severity analysis data grouped by a specified column.
    
    Args:
        df: Input dataframe
        by_column: Column to group by for severity analysis
    
    Returns:
        DataFrame with severity counts by the specified column
    """
    if 'severity' in df.columns and by_column in df.columns:
        severity_order = ['Slight', 'Serious', 'Fatal']
        return pd.crosstab(
            df[by_column], 
            df['severity'], 
            normalize='index'
        ).reindex(columns=severity_order, fill_value=0) * 100
    return pd.DataFrame()

def format_large_numbers(number: float) -> str:
    """
    Format large numbers with K, M suffixes for better readability.
    
    Args:
        number: Number to format
    
    Returns:
        Formatted string
    """
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:,.0f}"

def get_unique_values_for_filters(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Get unique values for each categorical column to populate filter options.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with column names as keys and sorted unique values as lists
    """
    categorical_columns = [
        'severity', 'gender', 'age_grp', 'road_conditions', 
        'weather_conditions', 'road_type', 'light_conditions', 'day_of_week'
    ]
    
    unique_values = {}
    for col in categorical_columns:
        if col in df.columns:
            # Remove NaN values and sort
            values = df[col].dropna().unique()
            values = sorted([str(val) for val in values if str(val) != 'nan'])
            unique_values[col] = values
    
    return unique_values

def calculate_accident_rates(df: pd.DataFrame, by_column: str) -> pd.DataFrame:
    """
    Calculate accident rates and percentages by a specified column.
    
    Args:
        df: Input dataframe
        by_column: Column to calculate rates by
    
    Returns:
        DataFrame with counts and percentages
    """
    if by_column in df.columns:
        counts = df[by_column].value_counts()
        percentages = (counts / counts.sum() * 100).round(1)
        
        result_df = pd.DataFrame({
            'count': counts,
            'percentage': percentages
        })
        result_df.index.name = by_column
        return result_df.reset_index()
    
    return pd.DataFrame()

# Advanced Analysis Functions

def extract_hour_from_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract hour from time column for temporal analysis.
    
    Args:
        df: Input dataframe with 'time' column
    
    Returns:
        DataFrame with additional 'hour' column
    """
    df_copy = df.copy()
    if 'time' in df.columns:
        # Handle both string and datetime time formats
        try:
            df_copy['hour'] = pd.to_datetime(df_copy['time'], format='%H:%M:%S').dt.hour
        except:
            try:
                df_copy['hour'] = pd.to_datetime(df_copy['time']).dt.hour
            except:
                # If conversion fails, create a default hour column
                df_copy['hour'] = np.nan
    else:
        df_copy['hour'] = np.nan
    
    return df_copy

def prepare_severity_speed_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare data for severity vs speed limit heatmap.
    
    Args:
        df: Input dataframe
    
    Returns:
        Pivot table for heatmap visualization
    """
    if 'severity' in df.columns and 'speed_limit' in df.columns:
        # Create speed bins
        df_temp = df.copy()
        df_temp = df_temp.dropna(subset=['speed_limit'])
        
        # Create speed limit bins
        speed_bins = [0, 20, 30, 40, 50, 60, 70, 100]
        speed_labels = ['≤20', '21-30', '31-40', '41-50', '51-60', '61-70', '>70']
        
        try:
            df_temp['speed_bin'] = pd.cut(df_temp['speed_limit'], bins=speed_bins, labels=speed_labels, include_lowest=True)
            
            # Create pivot table
            heatmap_data = pd.crosstab(df_temp['speed_bin'], df_temp['severity'], normalize='index') * 100
            return heatmap_data.round(1)
        except:
            return pd.DataFrame()
    
    return pd.DataFrame()

def prepare_temporal_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Prepare data for various temporal analyses.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with different temporal analysis datasets
    """
    df_with_hour = extract_hour_from_time(df)
    results = {}
    
    # Hourly distribution
    if 'hour' in df_with_hour.columns:
        hourly_data = df_with_hour.groupby('hour').size().reset_index(name='count')
        results['hourly'] = hourly_data
    
    # Weekday vs Weekend
    if 'day_of_week' in df.columns:
        df_temp = df.copy()
        df_temp['is_weekend'] = df_temp['day_of_week'].isin(['Saturday', 'Sunday'])
        weekend_severity = pd.crosstab(df_temp['is_weekend'], df_temp['severity'], normalize='index') * 100
        weekend_severity.index = ['Weekday', 'Weekend']
        weekend_severity.index.name = 'day_type'  # Give the index a name
        results['weekend_vs_weekday'] = weekend_severity
    
    # Monthly trends with rolling average
    if 'date' in df.columns:
        monthly_counts = df.groupby(df['date'].dt.to_period('M')).size()
        monthly_df = pd.DataFrame({
            'month': monthly_counts.index.astype(str),
            'count': monthly_counts.values,
            'rolling_avg': monthly_counts.rolling(window=3, center=True).mean().values
        })
        results['monthly_trends'] = monthly_df
    
    return results

def prepare_demographic_severity_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Prepare demographic-severity analysis data.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with demographic analysis datasets
    """
    results = {}
    
    # Age vs Severity heatmap
    if 'age_grp' in df.columns and 'severity' in df.columns:
        age_severity = pd.crosstab(df['age_grp'], df['severity'], normalize='index') * 100
        results['age_severity_heatmap'] = age_severity.round(1)
    
    # Gender vs Accident conditions
    if 'gender' in df.columns and 'road_conditions' in df.columns:
        # Group rare road conditions
        df_temp = df.copy()
        df_temp['road_conditions'] = group_rare_categories(df_temp['road_conditions'], min_count=1000)
        gender_road = pd.crosstab(df_temp['gender'], df_temp['road_conditions'], normalize='index') * 100
        results['gender_road_conditions'] = gender_road.round(1)
    
    # Age and Gender vs Time (if hour extraction is possible)
    df_with_hour = extract_hour_from_time(df)
    if 'hour' in df_with_hour.columns and 'age_grp' in df_with_hour.columns and 'gender' in df_with_hour.columns:
        # Create age-gender groups for cleaner visualization
        df_temp = df_with_hour.copy()
        df_temp = df_temp.dropna(subset=['hour'])
        
        # Aggregate by broader categories for clarity
        age_gender_time = df_temp.groupby(['hour', 'gender']).size().reset_index(name='count')
        results['age_gender_time'] = age_gender_time
    
    return results

def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical variables.
    
    Args:
        df: Input dataframe
    
    Returns:
        Correlation matrix DataFrame
    """
    # Add hour if possible
    df_with_hour = extract_hour_from_time(df)
    
    # Select numerical columns
    numeric_cols = ['speed_limit', 'number_of_casualties', 'number_of_vehicles', 'severity_numeric']
    if 'hour' in df_with_hour.columns:
        numeric_cols.append('hour')
    
    available_cols = [col for col in numeric_cols if col in df_with_hour.columns]
    
    if len(available_cols) > 1:
        correlation_data = df_with_hour[available_cols].dropna()
        if len(correlation_data) > 0:
            return correlation_data.corr()
    
    return pd.DataFrame()

def prepare_severity_trends_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare severity trends over time for stacked area chart.
    
    Args:
        df: Input dataframe
    
    Returns:
        DataFrame with yearly severity counts
    """
    if 'year' in df.columns and 'severity' in df.columns:
        severity_trends = df.groupby(['year', 'severity']).size().unstack(fill_value=0)
        severity_trends = severity_trends.reset_index()
        return severity_trends
    
    return pd.DataFrame()

def prepare_environmental_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Prepare environmental condition analysis data.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with environmental analysis datasets
    """
    results = {}
    
    # Weather vs Severity (normalized percentages)
    if 'weather_conditions' in df.columns and 'severity' in df.columns:
        df_temp = df.copy()
        df_temp['weather_conditions'] = group_rare_categories(df_temp['weather_conditions'], min_count=500)
        weather_severity = pd.crosstab(df_temp['weather_conditions'], df_temp['severity'], normalize='index') * 100
        results['weather_severity'] = weather_severity.round(1)
    
    # Road Type vs Severity
    if 'road_type' in df.columns and 'severity' in df.columns:
        df_temp = df.copy()
        df_temp['road_type'] = group_rare_categories(df_temp['road_type'], min_count=500)
        road_severity = pd.crosstab(df_temp['road_type'], df_temp['severity'])
        results['road_type_severity'] = road_severity
    
    # Light Conditions vs Severity
    if 'light_conditions' in df.columns and 'severity' in df.columns:
        df_temp = df.copy()
        df_temp['light_conditions'] = group_rare_categories(df_temp['light_conditions'], min_count=500)
        light_severity = pd.crosstab(df_temp['light_conditions'], df_temp['severity'], normalize='index') * 100
        results['light_severity'] = light_severity.round(1)
    
    return results

def create_sankey_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Prepare data for Sankey diagram showing flow from road_type -> weather -> severity.
    
    Args:
        df: Input dataframe
    
    Returns:
        Dictionary with Sankey diagram data
    """
    if not all(col in df.columns for col in ['road_type', 'weather_conditions', 'severity']):
        return {}
    
    # Group rare categories for cleaner visualization
    df_temp = df.copy()
    df_temp['road_type'] = group_rare_categories(df_temp['road_type'], min_count=1000)
    df_temp['weather_conditions'] = group_rare_categories(df_temp['weather_conditions'], min_count=1000)
    
    # Create the flow data
    flow_counts = df_temp.groupby(['road_type', 'weather_conditions', 'severity']).size().reset_index(name='count')
    flow_counts = flow_counts[flow_counts['count'] >= 100]  # Filter small flows for clarity
    
    # Create node labels and indices
    road_types = df_temp['road_type'].unique()
    weather_types = df_temp['weather_conditions'].unique()
    severities = df_temp['severity'].unique()
    
    # Create node list
    nodes = list(road_types) + list(weather_types) + list(severities)
    
    # Create source, target, and value lists for Sankey
    sources = []
    targets = []
    values = []
    
    # Road -> Weather flows
    road_weather_counts = df_temp.groupby(['road_type', 'weather_conditions']).size()
    for (road, weather), count in road_weather_counts.items():
        if count >= 100:  # Filter small flows
            sources.append(nodes.index(road))
            targets.append(nodes.index(weather))
            values.append(count)
    
    # Weather -> Severity flows
    weather_severity_counts = df_temp.groupby(['weather_conditions', 'severity']).size()
    for (weather, severity), count in weather_severity_counts.items():
        if count >= 100:  # Filter small flows
            sources.append(nodes.index(weather))
            targets.append(nodes.index(severity))
            values.append(count)
    
    return {
        'nodes': nodes,
        'sources': sources,
        'targets': targets,
        'values': values
    }