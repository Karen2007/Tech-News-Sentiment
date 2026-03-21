import pandas as pd
import requests
import io
import tempfile
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.font_manager as fm
from datetime import timedelta, timezone, datetime

# Download new font for GitHub
url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf"
response = requests.get(url)

with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as f:
    f.write(response.content)
    font_path = f.name

fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Poppins'

data = pd.read_csv('sentiment_index_history.csv')

def display_last_day_scores(ax):

    recent_day = data['date'].iloc[-1]  # Get last day from last entry

    # If at least 24 rows are present, plot the last 24
    if len(data) >= 24:
        recent_hours = data.iloc[-24:]
        recent_starts = recent_hours['hour_start'].tolist()
        recent_ends = recent_hours['hour_end'].tolist()
        recent_day_scores = recent_hours['sentiment_index_score']
    
    else:
        recent_day_times = data[data['date'] == recent_day][['hour_start', 'hour_end']]
        recent_day_scores = data[data['date'] == recent_day]['sentiment_index_score']
    
        recent_starts = recent_day_times['hour_start'].tolist() # Starts of intervals
        recent_ends = recent_day_times['hour_end'].tolist() # Ends of intervals

    # Display the time nicely in the x-axis of the graph
    plot_time_axis = [f"{start_time}:00-{end_time}:00"
                      for start_time, end_time in zip(recent_starts, recent_ends)]

    ax.plot(plot_time_axis, recent_day_scores, marker='o', linestyle='-', color='red')
    ax.autofmt_xdate()  # Fix overlap if too many values are present on the x-axis
    ax.hlines(xmin=plot_time_axis[0], xmax=plot_time_axis[-1], y=0, alpha=0.7, linestyle='--') # Add the y=0 line to the graph
    ax.set_ylim(min(recent_day_scores) - 0.01, max(recent_day_scores) + 0.01) # Lock the y limits
    ax.set_title(f"Sentiment Index Score In The Last 24 Hours")
    ax.set_xticks(plot_time_axis) # Set xticks to time periods
    ax.set_xlabel('Hours')
    ax.set_ylabel('Sentiment score')
    ax.tick_params(axis='x', rotation=45) # Rotate ticks to prevent overlap
    ax.grid(color='gray', alpha=0.5, linestyle='--') # Add grid


def display_last_week_scores(ax):

    last_day = pd.to_datetime(data['date'].iloc[-1]) # Get last day from last entry
    first_day = last_day - timedelta(days=6) # Date one week ago

    data['date'] = pd.to_datetime(data['date']) # Convert string to datetime object

    last_week_data = data[data['date'] >= first_day] # Only the entries in the past 7 days

    scores = last_week_data.groupby('date')['sentiment_index_score'].mean() # Group by days and get the mean

    # Plot
    ax.plot(scores.index, scores.values, marker='o', linestyle='-', color='blue')
    ax.hlines(xmin=scores.index[0], xmax=scores.index[-1], y=0, linestyle='--', alpha=0.7) # Add the y=0 line to the graph
    ax.set_ylim(scores.values.min() - 0.001, scores.values.max() + 0.001) # Lock the y limits
    ax.set_title(f'Average Sentiment Index Score {first_day.strftime("%Y/%m/%d")} - {last_day.strftime("%Y/%m/%d")}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average sentiment score')
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f')) # Only 4 digits after decimal on y-axis
    ax.grid(color='gray', alpha=0.5, linestyle='--')

plt.style.use('dark_background') # BG color

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
fig.suptitle('Recent Results', fontsize=20)

display_last_day_scores(ax1) # First plot on the top
display_last_week_scores(ax2) # Second one on the bottom

plt.tight_layout(pad=2.0) # Prevent overlap
plt.savefig('recent_results.png', facecolor=fig.get_facecolor(), dpi=300) # Save to file
plt.show()