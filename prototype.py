import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data  
df = pd.read_csv('Image.csv')
df['Well_ID'] = df['FileName_Orig_grey'].str.extract(r'_(\d{5})_')
df['Day'] = df['FileName_Orig_grey'].str.extract(r'(day_\d+)')

# Extract some consistent columns from DataFrame  
images = df['FileName_Orig_grey'].to_list()

# Tabs for different visualizations  
# st.title("Cell Count Visualization")
tabs = st.tabs(["Line Plot", "Violin Plot", "Scatter Plot"])

with tabs[0]:
    st.subheader("Line Plot of Cell Counts")

    # Extract unique Well IDs for selection  
    well_ids = df['Well_ID'].unique()
    selected_well_id = st.selectbox("Select Well ID", well_ids)

    # Filter data based on selected Well ID  
    filtered_df = df[df['Well_ID'] == selected_well_id]
    red_cells = filtered_df['Count_RedCellsInWell'].to_list()
    green_cells = filtered_df['Count_GreenCells'].to_list()
    all_cells = filtered_df['Count_AllCellsInWell_sepparate'].to_list()
    images = filtered_df['FileName_Orig_grey'].to_list()
    
    cols = st.columns(5)  # Create 5 columns for side-by-side image display  

    for i, filename in enumerate(images):
        with cols[i]:
            img_path = os.path.join('test_img', filename[:-4] + '_overlay.tiff')
            st.image(img_path, caption=filename[3:8], use_column_width=True)

    dates = [0, 2, 3, 6, 7]

    # Create DataFrame for plotting  
    time_series_df = pd.DataFrame({
        'Date': dates * 3,
        'Count': red_cells + green_cells + all_cells,
        'Type': ['Red Cells'] * 5 + ['Green Cells'] * 5 + ['All Cells'] * 5
    })  
    fig = px.line(time_series_df, x='Date', y='Count', color='Type', markers=True)
    fig.update_layout(xaxis_title='Date', yaxis_title='Count')
    st.plotly_chart(fig)

with tabs[1]:
    st.subheader("Violin Plot of Green Cell Counts")
    
    selected_field = st.selectbox("Select Field", ['Count_RedCellsInWell', 'Count_GreenCells', 'Count_AllCellsInWell_sepparate', 'Threshold_FinalThreshold_AllCellsInWell_sepparate', 'Threshold_FinalThreshold_RedCells'])
    # Create DataFrame for plotting
    violin_df = pd.DataFrame(df[selected_field].values.reshape(102, 5), columns=df['Day'].unique() )
    violin_df = violin_df.melt(var_name='Day', value_name=selected_field)
    fig = px.violin(violin_df, y=selected_field, x='Day', box=True, points="all")
    st.plotly_chart(fig)

with tabs[2]:
    days = df['Day'].unique()
    selected_day = st.selectbox("Select Day", days)
    
    st.subheader("Scatter Plot of Red vs Green Cells")
    
    # Create DataFrame for plotting
    filtered_df = df[df['Day'] == selected_day]
    scatter_df = pd.DataFrame({
        'Red Cells': filtered_df['Count_RedCellsInWell'],
        'Green Cells': filtered_df['Count_GreenCells']
    })  
    fig = px.scatter(scatter_df, x='Red Cells', y='Green Cells')
    fig.update_layout(xaxis_title='Count of Red Cells', yaxis_title='Count of Green Cells')
    st.plotly_chart(fig)
    
    st.subheader("Scatter Plot of Threshold")
    # Create DataFrame for plotting  
    scatter_df = pd.DataFrame({
        'AllCells Threshold': df['Threshold_FinalThreshold_AllCellsInWell_sepparate'][::5],
        'RedCells Threshold': df['Threshold_FinalThreshold_RedCells'][::5]
    })
    fig = px.scatter(scatter_df, x='AllCells Threshold', y='RedCells Threshold')
    fig.update_layout(xaxis_title='AllCells Threshold', yaxis_title='RedCells Threshold')
    st.plotly_chart(fig)