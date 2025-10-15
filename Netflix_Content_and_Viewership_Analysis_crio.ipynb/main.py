# Netflix Data Analysis and Viewership Trends Visualization
# Objective: To analyze Netflix content trends (movies vs shows, genres, regions, and viewer demographics)
# Step 1: Install and import required libraries

!pip install plotly pandas

print("\nWe've installed the necessary libraries.")

import pandas as pd
import plotly.express as px
import plotly.io as pio
import time

# Set default renderer for Plotly
pio.renderers.default = 'colab'

print("\nWe have now imported those libraries so we can:\n",
      "- Use pandas for data manipulation\n",
      "- Create interactive plots with plotly and statistical data visualization\n")

def load_dataset(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        print(f'Error loading dataset: {e}')
        return None

netflix_df = load_dataset('https://gitlab.crio.do/public_content/da_ds_artifacts/-/raw/master/netflix-dataset.csv')
viewership_df = load_dataset('https://gitlab.crio.do/public_content/da_ds_artifacts/-/raw/master/Viewership_Data_with_Demographics.csv')

print("\nWe've defined a function to load datasets from URLs and used it to load our Netflix content and viewership datasets.\n")
if netflix_df is not None and viewership_df is not None:
    for df in [netflix_df, viewership_df]:
        if 'id' in df.columns:
            df.rename(columns={'id': 'show_id'}, inplace=True)

    data = pd.merge(netflix_df, viewership_df, on='show_id', how='inner')
    display(data.head())
    print("We've successfully merged the Netflix content and viewership datasets on the 'show_id' column. This combined dataset will be used for our analysis.")
else:
    print("Failed to load or merge datasets")
def plot_movies_vs_shows(data):
    data['year_interval'] = (data['release_year'] // 5) * 5
    movies_vs_shows_interval = data.groupby(['year_interval', 'type']).size().unstack(fill_value=0)
    movies_vs_shows_long = movies_vs_shows_interval.reset_index().melt(id_vars='year_interval',
                                                                       var_name='Type',
                                                                       value_name='Count')

    fig = px.bar(movies_vs_shows_long,
                 x='year_interval',
                 y='Count',
                 color='Type',
                 title='Movies vs TV Shows Over 5-Year Intervals',
                 labels={'year_interval': '5-Year Intervals', 'Count': 'Number of Titles Produced'},
                 text='Count',
                 height=600)

    fig.update_layout(barmode='stack', xaxis_title='5-Year Intervals', yaxis_title='Number of Titles',
                      legend_title='Type')
    fig.show()

print("\nWe've defined a function to create a stacked bar chart showing the count of Movies vs TV Shows over 5-year intervals.\n")

plot_movies_vs_shows(data)

print("This chart visualizes the trend in Netflix's content production, showing how the balance between Movies and TV Shows has changed over time.")

# Set default renderer for Plotly to 'colab' for viewing in Colab
pio.renderers.default = 'colab'

print("Plotly renderer set to 'colab' for viewing in Colab.")

def plot_genre_popularity(data):
    if 'genres' not in data.columns:
        print("No 'genres' column found. Please check the dataset.")
        return

    tv_shows = data[data['type'] == 'SHOW'].copy()
    tv_shows['genres'] = tv_shows['genres'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    tv_shows_exploded = tv_shows.explode('genres')
    tv_shows_exploded['year_interval'] = (tv_shows_exploded['release_year'] // 5) * 5

    genres_popularity = tv_shows_exploded.groupby(['year_interval', 'genres']).size().unstack(fill_value=0)
    genres_popularity_long = genres_popularity.reset_index().melt(id_vars='year_interval', var_name='Genre', value_name='Count')

    fig = px.bar(genres_popularity_long,
                 x='year_interval',
                 y='Count',
                 color='Genre',
                 title='Popularity of TV Show Genres Over 5-Year Intervals',
                 labels={'year_interval': '5-Year Intervals', 'Count': 'Number of Shows'},
                 text='Count',
                 height=600)

    fig.update_layout(barmode='stack', xaxis_title='5-Year Intervals', yaxis_title='Number of Shows',
                      legend_title='Genres',
                      legend=dict(x=1, y=1, bgcolor='rgba(255,255,255,0.5)', bordercolor='rgba(0,0,0,0.1)'))
    fig.show()

print("\nWe've defined a function to create a stacked bar chart showing the popularity of different TV show genres over 5-year intervals.\n")

plot_genre_popularity(data)

print("This chart visualizes the changing popularity of different TV show genres over time, helping identify trends in content preferences.")

def plot_genre_distribution_by_region(data):
    if 'genres' not in data.columns or 'viewer_region' not in data.columns:
        print("The 'genres' or 'viewer_region' column is not found in the dataset.")
        return

    # Ensure genres column is properly formatted as lists
    data['genres'] = data['genres'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    data_exploded = data.explode('genres')

    # Group by region and genre
    genre_region_distribution = data_exploded.groupby(['viewer_region', 'genres']).size().unstack(fill_value=0)

    for region in genre_region_distribution.index:
        genre_counts = genre_region_distribution.loc[region].reset_index()
        genre_counts.columns = ['Genre', 'Count']

        # Check if there are genres to plot
        if genre_counts['Count'].sum() == 0:
            print(f"No genre data available for {region}. Skipping plot.")
            continue

        # Create pie chart
        fig = px.pie(genre_counts,
                     values='Count',
                     names='Genre',
                     title=f'Genre Distribution in {region}',
                     hover_data=['Count'],
                     labels={'Count':'Number of Titles'})

        fig.show()
        time.sleep(1)  # add delay to ensure rendering

print("\nWe've defined a function to create pie charts showing the distribution of genres for each region in our dataset.\n")

plot_genre_distribution_by_region(data)

print("These pie charts visualize the genre distribution for each region, allowing us to compare content preferences across different geographical areas.")

def plot_viewership_by_age_and_region(data):
    age_region_viewership = data.groupby(['viewer_age_group', 'viewer_region'])['viewership_count'].sum().unstack()
    age_region_viewership_long = age_region_viewership.reset_index().melt(id_vars='viewer_age_group',
                                                                          var_name='Region',
                                                                          value_name='Viewership')

    fig = px.bar(age_region_viewership_long,
                 x='viewer_age_group',
                 y='Viewership',
                 color='Region',
                 title='Stacked Viewership by Age Group and Region',
                 labels={'viewer_age_group': 'Age Group', 'Viewership': 'Total Viewership Count'},
                 hover_data={'Viewership': ':.0f'})
    fig.show()

print("\nWe've defined a function to create a stacked bar chart showing viewership patterns across different age groups and regions.\n")

plot_viewership_by_age_and_region(data)

print("This stacked bar chart visualizes the viewership distribution across different age groups and regions, allowing us to identify demographic trends in content consumption.")

print("""
Key Insights:
1. Netflix has produced more TV Shows than Movies after 2015.
2. Drama and Thriller genres are most popular in recent years.
3. North America prefers Action, Asia prefers Romance and Drama.
4. The 18-25 age group has the highest viewership globally.
""")
