import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import math

def plot_demand(data, deb = '2013-01-19 00:30:00', end= '2013-01-30 00:30:00', low_col = "#21733D", high_col = "#B03131"):
    df = data.loc[pd.to_datetime(deb):pd.to_datetime(end)]
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df.index, df['demand'], color='black', linewidth=0.8)
    ymin, ymax = ax.get_ylim()

    # Identify consecutive periods of each tariff
    tariff_changes = df['tariff'] != df['tariff'].shift()
    tariff_groups = tariff_changes.cumsum()

    for group_id in tariff_groups.unique():
        group_data = df[tariff_groups == group_id]
        tariff_value = group_data['tariff'].iloc[0]
        start_time = group_data.index[0]
        if group_id < tariff_groups.max():
            next_group_data = df[tariff_groups == group_id + 1]
            end_time = next_group_data.index[0]
        else:
            end_time = group_data.index[-1]
        
        # Choose color based on tariff
        if tariff_value == 'Low':
            color = low_col
        elif tariff_value == 'High':
            color = high_col 
        else:
            continue  # Skip if neither low nor high
        
        # Add rectangle
        ax.axvspan(start_time, end_time, color=color, alpha=0.6, label=tariff_value)


    ax.set_ylabel('Electrical demand')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_tariff_rectangle(df, start, end,
                          cols=('tariff_High', 'tariff_Normal', 'tariff_Low'),
                          colors=('#B03131', 'blue', '#21733D'),
                          figsize=(10, 4),
                          title=None):

    # Ensure DateTimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.copy()
        df.index = pd.to_datetime(df.index)

    # Slice time window
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    window = df.loc[(df.index >= start) & (df.index <= end), list(cols)]

    low   = window[cols[2]].to_numpy()
    norm  = window[cols[1]].to_numpy()
    high  = window[cols[0]].to_numpy()

    # cumulative boundaries
    bottom = np.zeros_like(low)              # 0
    low_top = low                            # Low band top
    norm_top = low + norm                    # Normal band top
    high_top = low + norm + high             # should be 1

    t = window.index

    # Plot
    fig, ax = plt.subplots(figsize=figsize)

    # Use step='post' to mimic interval-wise constant values
    ax.fill_between(t, bottom, low_top, step='post', color=colors[2], label='Low', linewidth=0)
    ax.fill_between(t, low_top, norm_top, step='post', color=colors[1], label='Normal', linewidth=0)
    ax.fill_between(t, norm_top, high_top, step='post', color=colors[0], label='High', linewidth=0)

    # Axes formatting
    ax.set_ylim(0, 1)
    ax.set_ylabel('Proportion')
    ax.set_xlabel('Date time')
    if title:
        ax.set_title(title)

    # Ticks: show daily ticks if range spans multiple days
    ax.legend(loc='upper left', frameon=False)
    ax.grid(False)

    # Tight layout for rendering
    fig.tight_layout()
    return fig, ax