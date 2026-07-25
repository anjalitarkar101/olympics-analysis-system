#=============================================
# app.py - Olympics Analysis System
#=============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import os

# Import custom modules
import preprocessor
import helper_functions as helper

# Create saved_visualizations folder if it doesn't exist
os.makedirs('saved_visualizations', exist_ok=True)

# ==========================================================
# Load Data from data/ folder
# ==========================================================
@st.cache_data
def load_data():
    """Load and preprocess the Olympics dataset from data/ folder."""
    try:
        df = pd.read_csv('data/athlete_events.csv')
        region_df = pd.read_csv('data/noc_regions.csv')
        df = preprocessor.preprocess(df, region_df)
        return df
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.info("Please make sure 'athlete_events.csv' and 'noc_regions.csv' are in the 'data/' folder")
        st.stop()

df = load_data()


# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Olympics Analysis System",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# Main Title
# ==========================================================
st.title("🏅 Olympics Analysis System")
st.markdown("Explore Olympic history with interactive visualizations and insights!")
st.markdown("---")


# ==========================================================
# Sidebar
# ==========================================================
st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image(
    'images/olympic_rings.png',
    use_column_width=True
)

st.sidebar.markdown("---")

# Season Selection - Just Summer or Winter
st.sidebar.subheader("Select Season")
selected_season = st.sidebar.radio(
    "Choose Season:",
    ['Summer Olympics', 'Winter Olympics']
)

# Filter data based on season selection
if selected_season == 'Summer Olympics':
    filtered_df = df[df['Season'] == 'Summer']
    season_icon = "☀️"
else:
    filtered_df = df[df['Season'] == 'Winter']
    season_icon = "❄️"

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {season_icon} {selected_season}")

st.sidebar.markdown("### Navigation")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# ==========================================================
# SECTION 1  : Medal Tally
# ==========================================================
if user_menu == 'Medal Tally':
    st.title(f"{season_icon} {selected_season} - Medal Tally Dashboard")
    st.write("Explore medal counts by country and year")

    st.sidebar.subheader("Filter Options")
    years_list, countries_list = helper.get_years_and_countries(filtered_df)  # Updated

    selected_year = st.sidebar.selectbox("Select Year", years_list)
    selected_country = st.sidebar.selectbox("Select Country", countries_list)

    # Display title based on selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader(f"🏆 Overall Medal Tally ({selected_season})")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader(f"🏆 Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader(f"🏆 {selected_country} Overall Performance")
    else:
        st.subheader(f"🏆 {selected_country} Performance in {selected_year}")

    medal_tally = helper.fetch_medal_tally(filtered_df, selected_year, selected_country)

    # Display with styling
    col1, col2 = st.columns([3, 1])
    with col1:
        if not medal_tally.empty:
            display_df = medal_tally.copy()
            display_df.columns = ['Country', '🥇 Gold', '🥈 Silver', '🥉 Bronze', '🥇🥈🥉 Total']
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    with col2:
        # Summary statistics
        if not medal_tally.empty:
            total_gold = medal_tally['Gold'].sum()
            total_silver = medal_tally['Silver'].sum()
            total_bronze = medal_tally['Bronze'].sum()
            total_medals = medal_tally['total'].sum()

            st.metric("🥇 Gold", total_gold)
            st.metric("🥈 Silver", total_silver)
            st.metric("🥉 Bronze", total_bronze)
            st.metric("🥇🥈🥉 Total", total_medals)

# ==========================================================
# SECTION 2 : Overall Analysis
# ==========================================================
elif user_menu == 'Overall Analysis':
    st.title(f"{season_icon} {selected_season} - Overall Analysis")
    st.write("Comprehensive overview of all Olympic Games")

    # Top Statistics
    editions = filtered_df['Year'].unique().shape[0]
    cities = filtered_df['City'].unique().shape[0]
    sports = filtered_df['Sport'].unique().shape[0]
    events = filtered_df['Event'].unique().shape[0]
    athletes = filtered_df['Name'].unique().shape[0]
    nations = filtered_df['Region'].unique().shape[0]

    st.subheader("📈 Key Statistics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("🏛️ Editions", editions)
    with col2:
        st.metric("🏙️ Host Cities", cities)
    with col3:
        st.metric("🏃 Sports", sports)
    with col4:
        st.metric("🎯 Events", events)
    with col5:
        st.metric("🌍 Nations", nations)
    with col6:
        st.metric("👥 Athletes", athletes)

    st.markdown("---")

    # Participating Nations Over Time
    st.subheader("🌍 Participating Nations Over the Years")
    nations_over_time = helper.get_data_over_time(filtered_df, 'Region')
    fig = px.line(
        nations_over_time,
        x="Edition",
        y="Region",
        title=f"Number of Participating Nations by Year ({selected_season})",
        labels={"Region": "Number of Nations"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Events Over Time
    st.subheader("🎯 Events Over the Years")
    events_over_time = helper.get_data_over_time(filtered_df, 'Event')
    fig = px.line(
        events_over_time,
        x="Edition",
        y="Event",
        title=f"Number of Events by Year ({selected_season})",
        labels={"Event": "Number of Events"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Athletes Over Time
    st.subheader("👥 Athletes Over the Years")
    athlete_over_time = helper.get_data_over_time(filtered_df, 'Name')  # Updated
    fig = px.line(
        athlete_over_time,
        x="Edition",
        y="Name",
        title=f"Number of Athletes by Year ({selected_season})",
        labels={"Name": "Number of Athletes"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap - Events per Sport per Year
    st.subheader("📊 Events Heatmap by Sport and Year")
    with st.expander("Click to view Heatmap"):
        fig, ax = plt.subplots(figsize=(20, 20))
        x = filtered_df.drop_duplicates(['Year', 'Sport', 'Event'])
        heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
        ax.set_title(f'Number of Events by Sport and Year ({selected_season})', fontsize=20)
        plt.tight_layout()
        st.pyplot(fig)
        plt.savefig(f'saved_visualizations/events_heatmap_{selected_season.replace(" ", "_")}.png', dpi=150, bbox_inches='tight')
        plt.close()

    # Most Successful Athletes
    st.subheader("🏅 Most Successful Athletes")
    sport_list = filtered_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    top_athletes = helper.get_overall_top_athletes(filtered_df, selected_sport)  # Updated

    if not top_athletes.empty:
        st.dataframe(top_athletes, use_container_width=True, hide_index=True)
    else:
        st.info("No medal data available for this sport")

# ==========================================================
# SECTION 3 : Country-wise Analysis
# ==========================================================
elif user_menu == 'Country-wise Analysis':
    st.title(f"{season_icon} {selected_season} - Country-wise Analysis")
    st.write("Analyze performance by country")

    st.sidebar.subheader("Country Selection")
    country_list = filtered_df['Region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Country Medal Tally Over Time
    st.subheader(f"📈 {selected_country} Medal Tally Over the Years")
    country_df = helper.get_country_yearly_medals(filtered_df, selected_country)  # Updated

    if not country_df.empty:
        fig = px.line(
            country_df,
            x="Year",
            y="Medal",
            title=f"{selected_country} - Medals by Year ({selected_season})",
            labels={"Medal": "Number of Medals"}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No medal data available for {selected_country}")

    # Country Sport Performance Heatmap
    st.subheader(f"🏅 {selected_country} Performance by Sport")
    with st.expander("Click to view Performance Heatmap"):
        pt = helper.get_country_heatmap_data(filtered_df, selected_country)  # Updated
        if not pt.empty:
            fig, ax = plt.subplots(figsize=(20, 10))
            sns.heatmap(pt, annot=True, fmt='g', cmap='Blues', ax=ax)
            ax.set_title(f'{selected_country} - Medals by Sport and Year ({selected_season})', fontsize=16)
            plt.tight_layout()
            st.pyplot(fig)
            plt.savefig(f'saved_visualizations/{selected_country}_heatmap.png', dpi=150, bbox_inches='tight')
            plt.close()
        else:
            st.info(f"No sport medal data available for {selected_country}")

    # Top Athletes from Country
    st.subheader(f"🏅 Top 10 Athletes from {selected_country}")
    top10_df = helper.get_country_top_athletes(filtered_df, selected_country)  # Updated (same name)

    if not top10_df.empty:
        st.dataframe(top10_df, use_container_width=True, hide_index=True)
    else:
        st.info(f"No athletes found for {selected_country}")

# ==========================================================
# SECTION 4 : Athlete-wise Analysis
# ==========================================================
elif user_menu == 'Athlete-wise Analysis':
    st.title(f"{season_icon} {selected_season} - Athlete-wise Analysis")
    st.write("Analyze athlete demographics and performance")

    athlete_df = filtered_df.drop_duplicates(subset=['Name', 'Region'])

    # Age Distribution
    st.subheader("📊 Age Distribution of Athletes")

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(
        height=500,
        title=f"Age Distribution by Medal Category ({selected_season})",
        xaxis_title="Age",
        yaxis_title="Density"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Age Distribution by Sport (Gold Medalists)
    st.subheader("🏅 Age Distribution by Sport (Gold Medalists)")

    # Get top sports for this season
    top_sports = filtered_df['Sport'].value_counts().head(20).index.tolist()

    x_data = []
    sport_names = []

    for sport in top_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not age_data.empty:
            x_data.append(age_data)
            sport_names.append(sport)

    if x_data:
        fig = ff.create_distplot(x_data, sport_names, show_hist=False, show_rug=False)
        fig.update_layout(
            height=600,
            title=f"Age Distribution of Gold Medalists by Sport ({selected_season})",
            xaxis_title="Age",
            yaxis_title="Density"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for selected sports")

    # Height vs Weight Analysis
    st.subheader("📏 Height vs Weight Analysis")
    sport_list = filtered_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport for Height/Weight Analysis', sport_list)
    temp_df = helper.get_weight_height_data(filtered_df, selected_sport)  # Updated

    if not temp_df.empty:
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = sns.scatterplot(
            data=temp_df,
            x='Weight',
            y='Height',
            hue='Medal',
            style='Sex',
            s=60,
            ax=ax
        )
        ax.set_title(f'Height vs Weight - {selected_sport} ({selected_season})' if selected_sport != 'Overall' else f'Height vs Weight - All Sports ({selected_season})')
        plt.tight_layout()
        st.pyplot(fig)
        plt.savefig(f'saved_visualizations/height_weight_scatter_{selected_season.replace(" ", "_")}.png', dpi=150, bbox_inches='tight')
        plt.close()
    else:
        st.info("No data available for this sport")

    # Gender Participation Over Time
    st.subheader("👫 Men vs Women Participation Over the Years")
    final = helper.get_gender_participation(filtered_df)  # Updated

    if not final.empty:
        fig = px.line(
            final,
            x="Year",
            y=["Male", "Female"],
            title=f"Gender Participation Trends ({selected_season})",
            labels={"value": "Number of Athletes", "variable": "Gender"}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No gender data available")

# ==========================================================
# Footer
# ==========================================================
st.markdown("---")
st.caption(f"🏅 Olympics Analysis System | Showing: {selected_season}")
st.caption("📊 Data source: 120+ years of Olympic history")