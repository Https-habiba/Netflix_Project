import pandas as pd 
df = pd.read_csv('Netflix_titles.csv')
print(df.head())
print(df.info())
print(df.describe())
print(df.columns)
print(df.shape)
print(df.isnull().sum())
print(df.dtypes)
print(df['country'].value_counts())
print("\n----- COUNTRY ANALYSIS -----")
country_series = df['country'].dropna().str.split(', ')
country_exploded = country_series.explode()
country_counts = country_exploded.value_counts()
print("\nTop 10 countries:")
print(country_counts.head(10))

print("\n----- GENRE / LISTED_IN ANALYSIS -----")
genres_series = df['listed_in'].dropna().str.split(', ')
genres_exploded = genres_series.explode()
genre_counts = genres_exploded.value_counts()
print("\nTop 10 genres:")
print(genre_counts.head(10))
print("\n----- DIRECTOR ANALYSIS -----")
director_series = df['director'].dropna().str.split(', ')
director_exploded = director_series.explode()
director_counts = director_exploded.value_counts()
print("\nTop 10 directors:")
print(director_counts.head(10))
print("\n----- CAST ANALYSIS -----")
cast_series = df['cast'].dropna().str.split(', ')
cast_exploded = cast_series.explode()
cast_counts = cast_exploded.value_counts()
print("\nTop 10 actors/actresses:")
print(cast_counts.head(10))
print("\n----- RELEASE YEAR ANALYSIS -----")
release_year_counts = df['release_year'].value_counts().sort_index()
print("\nNumber of titles released each year:")
print(release_year_counts)
print("\n----- RUNTIME ANALYSIS -----")
def extract_runtime(runtime_str):
    if pd.isnull(runtime_str):
        return None
    parts = runtime_str.split()
    if len(parts) != 2:
        return None
    try:
        return int(parts[0])
    except ValueError:
        return None
df['runtime_minutes'] = df['duration'].apply(extract_runtime)
print("\nRuntime statistics (in minutes):")
print(df['runtime_minutes'].describe())
print("\n----- RELEASE YEAR ANALYSIS -----")
release_year_counts = df['release_year'].value_counts().sort_index()
print("\nNumber of titles released each year:")
print(release_year_counts)
print("\n----- RUNTIME ANALYSIS -----")

print("\n----- BUILDING GENRE TABLE -----")

# Create a smaller table first with id, title, type, country, listed_in
base = df[['show_id', 'title', 'type', 'country', 'release_year', 'listed_in']].copy()

# Split listed_in into lists
base['genre_list'] = base['listed_in'].dropna().str.split(', ')

# Explode so each genre gets its own row
genre_df = base.explode('genre_list')

# Rename for clarity
genre_df = genre_df.rename(columns={'genre_list': 'genre'})

print("Sample of genre_df:")
print(genre_df.head(10))
print("\nRows in genre_df:", len(genre_df))
print("\nRuntime statistics (in minutes):")
print(df['runtime_minutes'].describe())

print("\n----- TOP GENRES BY TYPE (MOVIE VS TV SHOW) -----")

# Group by type (Movie/TV Show) and genre, then count
genre_by_type = (
    genre_df
    .groupby(['type', 'genre'])
    .size()
    .reset_index(name='count')
)

# For each type, get top 10 genres
for content_type in ['Movie', 'TV Show']:
    print(f"\nTop 10 genres for {content_type}s:")
    temp = (
        genre_by_type[genre_by_type['type'] == content_type]
        .sort_values('count', ascending=False)
        .head(10)
    )
    print(temp[['genre', 'count']].to_string(index=False))

print("\n----- TOP GENRES IN RECENT YEARS (2015+) -----")

recent = genre_df[genre_df['release_year'] >= 2015]

recent_genre_counts = (
    recent['genre']
    .value_counts()
    .head(15)
)

print("Top 15 genres since 2015:")
print(recent_genre_counts)
