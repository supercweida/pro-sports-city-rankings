import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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

# # Button
# if st.button("Show All Leagues"):
#     st.success(f"Showing All Leagues!")

# # Sort the DataFrame based on the selected column
# league_df_sorted = league_df.sort_values(by=sort_column, ascending=False)

# fig, ax = plt.subplots()
# ax.axis('off')

# table = ax.table(cellText=league_df_sorted.values, colLabels=league_df_sorted.columns, loc='center')

# if plot_choice == 'NFL':
#     header_color = '#2C3E50'      # Deep navy blue
#     cell_color = '#ECF6FD'        # Very light blue
#     header_text_color = 'white'
# elif plot_choice == 'MLB':
#     header_color = '#3A6B35'      # Forest green
#     cell_color = '#E9F7EF'        # Mint cream
#     header_text_color = 'white'
# elif plot_choice == 'NBA':
#     header_color = '#7D5A50'      # Cocoa brown
#     cell_color = '#F5F0EB'        # Off-white with warmth
#     header_text_color = 'white'
# elif plot_choice == 'NHL':
#     header_color = '#C0392B'      # Strong red
#     cell_color = '#FDEDEC'        # Blush pink
#     header_text_color = 'white'
# elif plot_choice == 'MLS':
#     header_color = '#2C3E50'      # Dark gray-blue
#     cell_color = '#F2F4F4'        # Soft gray
#     header_text_color = 'white'
# else:
#     header_color = '#2C3E50'      # Deep navy blue
#     cell_color = '#ECF6FD'        # Very light blue
#     header_text_color = 'white'

# # Apply colors
# for (row, col), cell in table.get_celld().items():
#     if row == 0:  # Header row
#         cell.set_facecolor(header_color)
#         cell.get_text().set_color(header_text_color)
#         cell.set_text_props(weight='bold')  # Optional: bold header text
#     else:
#         cell.set_facecolor(cell_color)

# st.subheader(f'{plot_choice}')
# st.pyplot(fig)


# Button logic to show all leagues
if st.button("Show All Leagues"):
    # Load all league dataframes
    all_dfs = []
    for league in league_list:
        df = pd.read_csv(f'league_rankings/{league.lower()}_rankings.csv')
        df["League"] = league  # Add league name as a column
        all_dfs.append(df)
    league_df = pd.concat(all_dfs, ignore_index=True)

    # --- INIT ---
    regions_key_prefix = "region_"
    unique_regions = sorted(league_df["Region"].dropna().unique())

    # --- SELECT/DESELECT ALL TOGGLE BUTTONS ---
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Select All Regions"):
            for region in unique_regions:
                st.session_state[regions_key_prefix + region] = True
    with col2:
        if st.button("Deselect All Regions"):
            for region in unique_regions:
                st.session_state[regions_key_prefix + region] = False

    # --- REGION CHECKBOXES ---
    st.markdown("### Filter by Region(s):")
    selected_regions = []
    for region in unique_regions:
        if region not in st.session_state:
            st.session_state[regions_key_prefix + region] = True  # Default selected

        if st.checkbox(region, value=st.session_state[regions_key_prefix + region], key=regions_key_prefix + region):
            selected_regions.append(region)

    # --- FILTER LOGIC ---
    if selected_regions:
        league_df = league_df[league_df["Region"].isin(selected_regions)]
    else:
        st.warning("No regions selected. Showing no data.")
        league_df = league_df.iloc[0:0]

    # Let user pick sort column from combined data
    sort_column = st.selectbox("Sort the combined table by:", options=league_df.columns)

    # Sort and display
    league_df_sorted = league_df.sort_values(by=sort_column, ascending=False)

    st.subheader("All Leagues Combined")
    st.dataframe(league_df_sorted)

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

