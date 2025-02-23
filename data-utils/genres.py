import pandas as pd

# Read the CSV file
file_path = "../Songkick_upcoming_events_2025_dataMOM070225.csv"
data = pd.read_csv(file_path)

# Drop rows where 'Genres' is missing
genres_series = data["Genres"].dropna()

# Split the genres (assuming they are comma-separated) and collect unique values
unique_genres = set()
for genres in genres_series:
    for genre in genres.split(","):
        unique_genres.add(genre.strip())

# Save the unique genres to a text file
with open("unique_genres.txt", "w") as f:
    for genre in sorted(unique_genres):
        f.write(genre + "\n")

# Optionally, print the unique genres to the console
print("Unique Genres:")
print(sorted(unique_genres))
