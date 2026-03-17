import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from datetime import timedelta, timezone, datetime

data = pd.read_csv('sentiment_index_history.csv')

pd.set_option('display.max_columns', 10)

def display_last_day_scores(ax):

    last_day = data['date'].iloc[-1] # Get last day from last entry
    last_day_times = data[data['date'] == last_day][['hour_start', 'hour_end']]
    last_day_scores = data[data['date'] == last_day]['sentiment_index_score']

    last_day_times_start = last_day_times['hour_start'].tolist() # Starts of intervals
    last_day_times_end = last_day_times['hour_end'].tolist() # Ends of intervals

    # Display the time nicely in the x-axis of the graph
    plot_time_axis = [f"{start_time}:00-{end_time}:00"
                      for start_time, end_time in zip(last_day_times_start, last_day_times_end)]

    ax.plot(plot_time_axis, last_day_scores, marker='o', linestyle='-', color='red')
    ax.hlines(xmin=plot_time_axis[0], xmax=plot_time_axis[-1], y=0) # Add the y=0 line to the graph
    ax.set_ylim(min(last_day_scores) - 0.01, max(last_day_scores) + 0.01) # Lock the y limits
    ax.set_title(f"Sentiment Index Score {last_day}")
    ax.set_xticks(plot_time_axis) # Set xticks to time periods
    ax.set_xlabel('Hours')
    ax.set_ylabel('Sentiment score')
    ax.grid(linestyle='--')  # Add grid
    ax.grid(color='gray', alpha=0.5, linestyle='--')


def display_last_week_scores(ax):

    last_day = pd.to_datetime(data['date'].iloc[-1]) # Get last day from last entry
    first_day = last_day - timedelta(days=7) + timedelta(days=1) # Date one week ago

    data['date'] = pd.to_datetime(data['date']) # Convert string to datetime object

    last_week_data = data[data['date'] >= first_day] # Only the entries in the past 7 days

    scores = last_week_data.groupby('date')['sentiment_index_score'].mean() # Group by days and get the mean

    # Plot
    ax.plot(scores.index, scores.values, marker='o', linestyle='-', color='blue')
    ax.hlines(xmin=scores.index[0], xmax=scores.index[-1], y=0) # Add the y=0 line to the graph
    ax.set_ylim(scores.values.min() - 0.001, scores.values.max() + 0.001) # Lock the y limits
    ax.set_title(f'Average Sentiment Index Score {first_day.strftime("%Y/%m/%d")} - {last_day.strftime("%Y/%m/%d")}')
    ax.set_xticks(scores.index) # Set xticks to days
    ax.set_xlabel('Date')
    ax.set_ylabel('Average sentiment score')
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f')) # Only 4 digits after decimal on y-axis
    ax.grid(color='gray', alpha=0.5, linestyle='--')

plt.rcParams['font.family'] = 'Century Gothic' # Change font
plt.style.use('dark_background') # BG color

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

display_last_day_scores(ax1) # First plot on the top
display_last_week_scores(ax2) # Second one on the bottom

plt.tight_layout(pad=2.0) # Prevent overlap
plt.savefig('recent_results.png', facecolor=fig.get_facecolor(), dpi=300)