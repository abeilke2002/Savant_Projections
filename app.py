import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="MLB Hitter Projections",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("vox")

#######################
data = pd.read_csv('preds.csv')  # This is your dataset
data['Season'] = data['Season'] + 1
data = data.drop(columns=['Unnamed: 0'], errors='ignore')

#######################
# Sidebar
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.title('Hitter Savant')
    
    # Reverse the player and year lists for display
    player_list = list(data.Name.unique())[::-1]
    year_list = list(data.Season.unique())[::-1]
    stat_list = list(data.Stat.unique())[::-1]
    
    # Set default selections
    default_player = 'Isaac Paredes'
    default_actual_year = 2024
    default_predicted_year = 2025
    
    # Ensure the default player and years are in the lists, if not fallback to the first item
    selected_player = st.selectbox('Select a Player', player_list, index=player_list.index(default_player) if default_player in player_list else 0)
    
    # Create two columns in the sidebar for actual year and predicted year
    col1, col2 = st.columns(2)

    with col1:
        selected_act_year = st.selectbox('Select Actual Year', year_list, index=year_list.index(default_actual_year) if default_actual_year in year_list else 0, key='actual_year')
    
    with col2:
        selected_pred_year = st.selectbox('Select Predicted Year', year_list, index=year_list.index(default_predicted_year) if default_predicted_year in year_list else 0, key='predicted_year')

    # Spacer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Stat selection
    st.subheader('Model Performance Stat')
    selected_stat = st.selectbox('Select a Stat', stat_list)
    
    # Filter the data based on selected player and year
    df_selected_player = data[(data['Name'] == selected_player)]
    df_selected_player_act = data[(data['Name'] == selected_player) & (data['Season'] == selected_act_year)]
    df_selected_player_pred = data[(data['Name'] == selected_player) & (data['Season'] == selected_pred_year)]


    # Main Section

def plot_grouped_bar(data, selected_player, selected_stat):
    # Filter the data for the selected player and stat
    input_df = data[(data['Name'] == selected_player) & (data['Stat'] == selected_stat)]
    
    # Set up the bar chart data
    seasons = input_df['Season'].values
    actual_values = input_df['Actual'].values
    predicted_values = input_df['Predicted'].values

    # Set up bar width and positions
    bar_width = 0.35
    r1 = np.arange(len(seasons))
    r2 = [x + bar_width for x in r1]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot actual and predicted values
    ax.bar(r1, actual_values, color='blue', width=bar_width, edgecolor='grey', label='Actual')
    ax.bar(r2, predicted_values, color='orange', width=bar_width, edgecolor='grey', label='Predicted')

    # Add labels and title
    ax.set_xlabel('Season', fontweight='bold')
    ax.set_ylabel('Value', fontweight='bold')
    ax.set_xticks([r + bar_width / 2 for r in range(len(seasons))])
    ax.set_xticklabels(seasons)

    # Add legend
    ax.legend()

    # Show the plot using Streamlit
    st.pyplot(fig)

def plot_actual_percentiles(data, selected_player, selected_act_year):
    if selected_act_year == 2025:
        st.write("This season has not happened yet.")
    else:
        fig, ax = plt.subplots(figsize=(10, 15))

        # Create a colormap that goes from blue to grey to red
        cmap = mcolors.LinearSegmentedColormap.from_list('blue_grey_red', ['blue', 'grey', 'red'])

        # Normalize the color range from 0 to 100
        norm = mcolors.Normalize(vmin=0, vmax=100)

        # Define the custom order of stats
        stat_order = ['xwOBA', 'xBA', 'xSLG', 'EV', 'Barrel%', 'HardHit%', 'Chase%', 'Whiff%', 'K%', 'BB%']

        # Lists for different rounding logic
        round_to_1_decimal_stats = ['BB%', 'K%', 'HardHit%', 'Barrel%', 'Chase%', 'Whiff%']
        round_to_3_decimal_stats = ['xwOBA', 'xBA', 'xSLG']

        plt.title("Actual Results Plot", fontsize=50, loc='center')

        fig.suptitle(f'Selected Year: {selected_act_year}', fontsize=16, y=0.86)

        # Loop through each stat in the custom order and plot its percentile and actual value
        for i, stat in enumerate(stat_order):
            # Check if the stat exists in the DataFrame
            if not data['Stat'].str.contains(stat, case=False).any():
                continue  # Skip if the stat is not found in the DataFrame

            y_coord = 0.5 - i * 0.3
            
            # Filter data for the current stat
            stat_data = data[data['Stat'].str.contains(stat, case=False)]
            
            # Take the mean percentile and actual for this stat
            percentile = stat_data['Actual_Percentile'].mean()
            actual_value = stat_data['Actual'].mean()

            # Check if percentile is NaN before plotting
            if pd.isna(percentile):
                continue  # Skip this iteration if the percentile is NaN

            # Apply different rounding logic
            if stat in round_to_1_decimal_stats:
                actual_value = round(actual_value * 100, 1)
            elif stat in round_to_3_decimal_stats:
                actual_value = round(actual_value, 3)
            elif stat == 'EV':  # Do not multiply EV by 100
                actual_value = round(actual_value, 1)
            
            # Get the color for the percentile based on the colormap
            color = cmap(norm(percentile))
            
            # Plot a thicker horizontal line from 0 to 100
            ax.hlines(y=y_coord, xmin=0, xmax=100, color='grey', linewidth=3)
            
            # Plot an additional line from 0 to the percentile
            ax.hlines(y=y_coord, xmin=0, xmax=percentile, color=color, linewidth=20)
            
            # Add percentile value inside the circle
            ax.text(percentile + 1.67, y_coord, f'{int(percentile)}', ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=5)
            
            # Plot the percentile value as a thicker marker on the line
            ax.scatter(percentile + 1.5, y_coord, color=color, s=400, zorder=4, linewidths=2)
            
            # Add the stat name to the left of the line with a larger font size
            ax.text(-5, y_coord, stat, ha='right', va='center', fontsize=15, color='black', fontweight='bold')
            
            # Add the actual value to the right of the line
            ax.text(105, y_coord, f'{actual_value}', ha='left', va='center', fontsize=15, color='black', fontweight='bold')

        # Adjust y-axis limits to fit the variables properly
        ymin_value = 0.5 - (len(stat_order) - 1) * 0.3 - 0.15
        ymax_value = 0.5 + 0.15

        for x in [25, 50, 75]:
            ax.vlines(x=x, ymin=ymin_value, ymax=ymax_value, color='white', linestyle='-', linewidth=.8)

        # Set the x-axis limits to go from 0 to 100
        ax.set_xlim(0, 107)

        # Remove all the borders and ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(left=False, bottom=False)

        # Remove y-axis labels and ticks since we don't need them
        ax.yaxis.set_visible(False)

        # Remove x-axis labels
        ax.set_xticks([])

        st.pyplot(fig)

def plot_predicted_percentiles(data, selected_player, selected_act_year):
    if selected_pred_year == 2026:
        st.write("This season has not happened yet.")
    else:
        fig, ax = plt.subplots(figsize=(10, 15))

        # Create a colormap that goes from blue to grey to red
        cmap = mcolors.LinearSegmentedColormap.from_list('blue_grey_red', ['blue', 'grey', 'red'])

        # Normalize the color range from 0 to 100
        norm = mcolors.Normalize(vmin=0, vmax=100)

        # Define the custom order of stats
        stat_order = ['xwOBA', 'xBA', 'xSLG', 'EV', 'Barrel%', 'HardHit%', 'Chase%', 'Whiff%', 'K%', 'BB%']

        # List of stats that need to be rounded to 2 decimal places and multiplied by 100
        round_to_1_decimal_stats = ['BB%', 'K%', 'HardHit%', 'Barrel%', 'Chase%', 'Whiff%']

        plt.title("Prediction Results Plot", fontsize=50, loc='center')

        fig.suptitle(f'Selected Year: {selected_pred_year}', fontsize=16, y=0.86)

        # Loop through each stat in the custom order and plot its percentile and actual value
        for i, stat in enumerate(stat_order):
            # Check if the stat exists in the DataFrame
            if not data['Stat'].str.contains(stat, case=False).any():
                continue  # Skip if the stat is not found in the DataFrame

            y_coord = 0.5 - i * 0.3
            
            # Filter data for the current stat
            stat_data = data[data['Stat'].str.contains(stat, case=False)]
            
            # Take the mean percentile and actual for this stat
            percentile = stat_data['Predicted_Percentile'].mean()
            predicted_value = stat_data['Predicted'].mean()

            # Check if percentile is NaN before plotting
            if pd.isna(percentile):
                continue  # Skip this iteration if the percentile is NaN

            # Round the actual value to 2 decimal places and multiply by 100 if it's in the specific list
            if stat in round_to_1_decimal_stats:
                predicted_value = round(predicted_value * 100, 1)
            
            # Get the color for the percentile based on the colormap
            color = cmap(norm(percentile))
            
            # Plot a thicker horizontal line from 0 to 100
            ax.hlines(y=y_coord, xmin=0, xmax=100, color='grey', linewidth=3)
            
            # Plot an additional line from 0 to the percentile
            ax.hlines(y=y_coord, xmin=0, xmax=percentile, color=color, linewidth=20)
            
            # Add percentile value inside the circle
            ax.text(percentile + 1.67, y_coord, f'{int(percentile)}', ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=5)
            
            # Plot the percentile value as a thicker marker on the line
            ax.scatter(percentile + 1.5, y_coord, color=color, s=400, zorder=4, linewidths=2)
            
            # Add the stat name to the left of the line with a larger font size
            ax.text(-5, y_coord, stat, ha='right', va='center', fontsize=15, color='black', fontweight='bold')
            
            # Add the actual value to the right of the line, multiplying by 100 if in the specific list
            ax.text(105, y_coord, 
                    f'{predicted_value:.3f}' if stat not in round_to_1_decimal_stats else f'{predicted_value:.1f}', 
                    ha='left', va='center', fontsize=15, color='black', fontweight='bold')

        # Adjust y-axis limits to fit the variables properly
        ymin_value = 0.5 - (len(stat_order) - 1) * 0.3 - 0.15
        ymax_value = 0.5 + 0.15

        for x in [25, 50, 75]:
            ax.vlines(x=x, ymin=ymin_value, ymax=ymax_value, color='white', linestyle='-', linewidth=.8)

        # Set the x-axis limits to go from 0 to 100
        ax.set_xlim(0, 107)

        # Remove all the borders and ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(left=False, bottom=False)

        # Remove y-axis labels and ticks since we don't need them
        ax.yaxis.set_visible(False)

        # Remove x-axis labels
        ax.set_xticks([])

        st.pyplot(fig)

# Top Layout with two columns for placeholder charts
top_left_col, top_right_col = st.columns([1, 1], gap='large')

with top_left_col:
    if not df_selected_player_act.empty:
        plot_actual_percentiles(df_selected_player_act, selected_player, selected_act_year)
    else:
        st.write("No data available for selected player and year.")

# Right column for predicted year data
with top_right_col:
    if not df_selected_player_pred.empty:
        plot_predicted_percentiles(df_selected_player_pred, selected_player, selected_pred_year)
    else:
        st.write("No data available for selected player and year.")

#######################
st.markdown('---')  # Horizontal rule to separate the sections

# Create two columns for the bottom section
bottom_left_col, bottom_right_col = st.columns([2, 2], gap="large")

with bottom_left_col:
    st.markdown('### Model Performance Bar Chart')

    # Check if the player data is available and plot the grouped bar chart
    if not df_selected_player.empty:
        plot_grouped_bar(data, selected_player, selected_stat)
    else:
        st.write("No data available for selected player.")

with bottom_right_col:
    with st.expander("About", expanded = True):
        st.write("""
            Data was pulled from FanGraphs from 2015-2024. (8/20/24)
            Predictions were made from all seasons before predicted season.
            The minimum amount of at bats to qualify in a season for the models was 100.     

            Make sure to select Predicted Year 2025 to see the predicted bubbles for next season!

            This application is in V1 of development. Feel free to contact me on Twitter/X (BeilkeAidan3) with any issues!
            Thank you for viewing!
        """)
