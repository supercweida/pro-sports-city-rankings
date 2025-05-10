import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

if 'show_all' not in st.session_state:
    st.session_state.show_all = False

# Title
st.title("Major Sports League Rankings")

league_list = ["NFL", "MLB", "NBA", "NHL", "MLS"]

# Sidebar dropdown to select plot
plot_choice = st.selectbox(
    "Choose a League:",
    league_list
)

league_df = pd.read_csv(f'league_rankings/{plot_choice.lower()}_rankings.csv')

# Add sorting functionality
sort_column = st.selectbox(
    "Sort the table by:",
    options=league_df.columns
)

if st.button("Show All Leagues"):
    st.session_state.show_all = True

# Button logic to show all leagues
if st.session_state.show_all:
    
    # Load all league dataframes
    all_dfs = []
    for league in league_list:
        df = pd.read_csv(f'league_rankings/{league.lower()}_rankings.csv')
        df["League"] = league  # Add league name as a column
        all_dfs.append(df)
    league_df = pd.concat(all_dfs, ignore_index=True)

    # Get sorted unique regions
    unique_regions = sorted(league_df["Region"].dropna().unique())

    # Add "All" option at the top
    region_options = ["All"] + unique_regions

    # Single select dropdown
    selected_region = st.selectbox("Select a Region:", region_options)

    # Filter the DataFrame if a specific region is selected
    if selected_region != "All":
        league_df = league_df[league_df["Region"] == selected_region]

    # Let user pick sort column from combined data
    sort_column = st.selectbox("Sort the combined table by:", options=league_df.columns)

    # Sort and display
    league_df_sorted = league_df.sort_values(by=sort_column, ascending=False)

    st.subheader("All Leagues Combined")
    st.dataframe(league_df_sorted)
    
    if st.button("Back to Single League View"):
        st.session_state.show_all = False
        st.experimental_rerun()
        
else:
    # Load single selected league
    league_df = pd.read_csv(f'league_rankings/{plot_choice.lower()}_rankings.csv')

    # Sort the DataFrame based on the selected column
    league_df_sorted = league_df.sort_values(by=sort_column, ascending=False)

    # Plotting logic (unchanged)
    fig, ax = plt.subplots()
    ax.axis('off')

    table = ax.table(cellText=league_df_sorted.values, colLabels=league_df_sorted.columns, loc='center')

    # Color logic (unchanged)
    if plot_choice == 'NFL':
        header_color = '#2C3E50'
        cell_color = '#ECF6FD'
        header_text_color = 'white'
    elif plot_choice == 'MLB':
        header_color = '#3A6B35'
        cell_color = '#E9F7EF'
        header_text_color = 'white'
    elif plot_choice == 'NBA':
        header_color = '#7D5A50'
        cell_color = '#F5F0EB'
        header_text_color = 'white'
    elif plot_choice == 'NHL':
        header_color = '#C0392B'
        cell_color = '#FDEDEC'
        header_text_color = 'white'
    elif plot_choice == 'MLS':
        header_color = '#2C3E50'
        cell_color = '#F2F4F4'
        header_text_color = 'white'
    else:
        header_color = '#2C3E50'
        cell_color = '#ECF6FD'
        header_text_color = 'white'

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor(header_color)
            cell.get_text().set_color(header_text_color)
            cell.set_text_props(weight='bold')
        else:
            cell.set_facecolor(cell_color)

    st.subheader(f'{plot_choice}')
    st.pyplot(fig)

