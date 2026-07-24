#==============================================
# helper_functions.py - Olympics Analysis System
#==============================================

import numpy as np
import pandas as pd
import streamlit as st


# ==========================================================
# Function 1: Get Medal Tally
# ==========================================================
@st.cache_data
def fetch_medal_tally(df, selected_year, selected_country):
    """
    Fetch medal tally based on year and country filters.

    Args:
        df: Preprocessed DataFrame
        selected_year: Year selected by user or 'Overall'
        selected_country: Country selected by user or 'Overall'

    Returns:
        DataFrame with medal counts (Gold, Silver, Bronze, Total)
    """

    # Remove duplicates to count each medal only once
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    # Flag to track if we're analyzing one country across multiple years
    is_single_country = 0      # Default: analyzing multiple countries

    # Filter data based on user selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        # Case 1: ALL countries, ALL years
        temp_df = medal_df

    elif selected_year == 'Overall' and selected_country != 'Overall':
        # Case 2: ONE country, ALL years
        is_single_country = 1
        temp_df = medal_df[medal_df['Region'] == selected_country]

    elif selected_year != 'Overall' and selected_country == 'Overall':
        # Case 3: ALL countries, ONE year
        temp_df = medal_df[medal_df['Year'] == int(selected_year)]

    else:
        # Case 4: ONE country, ONE year
        is_single_country = 1
        temp_df = medal_df[(medal_df['Year'] == selected_year) & (medal_df['Region'] == selected_country)]

    # Group and calculate totals based on the flag
    if is_single_country == 1:
        # Single country: Group by Year
        medal_tally = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        # Multiple countries: Group by region
        medal_tally = temp_df.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            'Gold', ascending=False
        ).reset_index()

    # Calculate total medals
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    # Convert to integers for clean display
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally


# =================================================================
# Function 2: Get Years List and Countries List for Dropdown Menus
# =================================================================
def get_years_and_countries(df):
    """
    Get unique years and countries for dropdown selection.

    Args:
        df: Preprocessed DataFrame

    Returns:
        years_list: List of unique years with 'Overall' at beginning
        countries_list: List of unique countries with 'Overall' at beginning
    """

    # Get all unique years, sort them, and add 'Overall' at the start
    years_list = df['Year'].unique().tolist()
    years_list.sort()
    years_list.insert(0, 'Overall')

    # Get all unique countries, sort them, and add 'Overall' at the start
    countries_list = np.unique(df['Region'].dropna().values).tolist()
    countries_list.sort()
    countries_list.insert(0, 'Overall')

    return years_list, countries_list


# ==========================================================
# Function 3: Get Data Trends Over Time
# ==========================================================
@st.cache_data
def get_data_over_time(df, column_name):
    """
    Calculate how many unique items appeared each year.

    Args:
        df: Preprocessed DataFrame
        column_name: Column to analyze (e.g., 'Region', 'Event', 'Name')

    Returns:
        DataFrame with 'Edition' (year) and the count for the specified column

    Example:
        get_data_over_time(df, 'Region') -> Returns number of countries per year
        get_data_over_time(df, 'Event') -> Returns number of events per year
        get_data_over_time(df, 'Name') -> Returns number of athletes per year
    """

    # Drop duplicates to count each unique item only once per year
    data_over_time = df.drop_duplicates(['Year', column_name])['Year'].value_counts().reset_index()

    # Rename columns for clarity
    data_over_time.columns = ['Edition', column_name]

    # Sort by year (chronological order)
    data_over_time = data_over_time.sort_values('Edition')

    return data_over_time


# ==========================================================
# Function 4: Get Most Successful Athletes
# ==========================================================
@st.cache_data
def get_overall_top_athletes(df, selected_sport):
    """
    Get the top 15 athletes with the most medals for a given sport.

    Args:
        df: Preprocessed DataFrame
        selected_sport: Sport name or 'Overall'

    Returns:
        DataFrame with athlete names, medal counts, sport, and country
    """

    # Keep only athletes who won medals
    temp_df = df.dropna(subset=['Medal'])

    # If a specific sport is selected, filter by that sport
    if selected_sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == selected_sport]

    # If no data exists, return empty DataFrame with correct columns
    if temp_df.empty:
        return pd.DataFrame(columns=['Name', 'Medals', 'Sport', 'Region'])

    # Count medals for each athlete
    medal_count = temp_df.groupby('Name').size().reset_index(name='Medals')

    # Sort by medal count (highest first) and take top 15
    medal_count = medal_count.sort_values('Medals', ascending=False).head(15)

    # Get sport and region for these athletes (take first occurrence)
    athlete_info = temp_df[['Name', 'Sport', 'Region']].drop_duplicates('Name')

    # Combine medal counts with athlete information
    result = medal_count.merge(athlete_info, on='Name', how='left')

    return result[['Name', 'Medals', 'Sport', 'Region']]


# ==========================================================
# Function 5: Get Year-wise Medal Tally for a Country
# ==========================================================
@st.cache_data
def get_country_yearly_medals(df, selected_country):
    """
    Get year-wise medal count for a specific country.

    Args:
        df: Preprocessed DataFrame
        selected_country: Country name

    Returns:
        DataFrame with years and medal counts
    """
    # Keep only medal winners and remove duplicates
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True
    )

    # Filter for the selected country
    country_data = temp_df[temp_df['Region'] == selected_country]

    # Count medals per year
    yearly_medals = country_data.groupby('Year').count()['Medal'].reset_index()

    return yearly_medals


# ==========================================================
# Function 6: Get Country's Performance Heatmap Data
# ==========================================================
@st.cache_data
def get_country_heatmap_data(df, selected_country):
    """
    Create a pivot table for country's performance by sport and year.

    Args:
        df: Preprocessed DataFrame
        selected_country: Country name

    Returns:
        Pivot table with Sports as rows, Years as columns, and medal counts as values
    """

    # Keep only medal winners and remove duplicates
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True
    )

    # Filter for the selected country
    country_data = temp_df[temp_df['Region'] == selected_country]

    # Return empty DataFrame if no data found
    if country_data.empty:
        return pd.DataFrame()

    # Create pivot table: Sports Vs Years with medal counts
    heatmap_data = country_data.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0)

    return heatmap_data


# ==========================================================
# Function 7: Get Top Athletes from a Country
# ==========================================================
@st.cache_data
def get_country_top_athletes(df, selected_country):
    """
    Get the top 10 athletes from a specific country.

    Args:
        df: Preprocessed DataFrame
        selected_country: Country name

    Returns:
        DataFrame with athlete names, medal counts, and sport
    """
    # Keep only medal winners from the selected country
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['Region'] == selected_country]

    # Return empty DataFrame if no data found
    if temp_df.empty:
        return pd.DataFrame(columns=['Name', 'Medals', 'Sport'])

    # Count medals for each athlete
    medal_count = temp_df.groupby('Name').size().reset_index(name='Medals')

    # Sort and take top 10
    medal_count = medal_count.sort_values('Medals', ascending=False).head(10)

    # Get sport for these athletes
    athlete_info = temp_df[['Name', 'Sport']].drop_duplicates('Name')

    # Combine medal counts with athlete information
    result = medal_count.merge(athlete_info, on='Name', how='left')

    return result[['Name', 'Medals', 'Sport']]


# ==========================================================
# Function 8: Get Weight and Height Data
# ==========================================================
@st.cache_data
def get_weight_height_data(df, selected_sport):
    """
    Get weight and height data for a specific sport or all sports.

    Args:
        df: Preprocessed DataFrame
        selected_sport: Sport name or 'Overall'

    Returns:
        DataFrame with athlete names, weight, height, medal, and region
    """
    # Remove duplicates to get each athlete only once
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    # Fill missing medals with 'No Medal'
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    # If a specific sport is selected, filter by that sport
    if selected_sport != 'Overall':
        sport_data = athlete_df[athlete_df['Sport'] == selected_sport]
        return sport_data
    else:
        # Return all sports data
        return athlete_df


# ==========================================================
# Function 9: Get Gender Participation Trends
# ==========================================================
@st.cache_data
def get_gender_participation(df):
    """
    Compare male and female participation over time.

    Args:
        df: Preprocessed DataFrame

    Returns:
        DataFrame with years, male count, and female count
    """
    # Remove duplicates to get each athlete only once per year
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    # Count male athletes per year
    male_data = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()

    # Count female athletes per year
    female_data = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    # Combine male and female data
    gender_data = male_data.merge(female_data, on='Year', how='left')

    # Rename columns for clarity
    gender_data.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    # Fill missing values with 0
    gender_data.fillna(0, inplace=True)

    return gender_data