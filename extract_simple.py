# require pandas, openpyxl
# the excel file must be in the MS team format and delete the top first merge cell.

import streamlit as st
import pandas as pd


def process_file(file):
    data = pd.read_excel(file)

    # Extracting student IDs from the email addresses
    data['ID'] = data['Email Address'].apply(lambda email: email.split('@')[0])

    # Selecting the relevant columns
    relevant_columns = ['Full Name', 'ID', 'Assignments', 'Points']

    # Filtering the data
    filtered_data = data[relevant_columns]

    # Pivoting the data to have assignments as columns and their scores as values
    pivoted_data = filtered_data.pivot_table(
        index=['Full Name', 'ID'], columns='Assignments', values='Points', aggfunc='first')

    # Resetting index to make Full Name and ID as columns
    final_data = pivoted_data.reset_index()

    return final_data


st.title('Excel File Processing App')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Process the file
    df = process_file(uploaded_file)

    # Show the DataFrame in the app
    st.write(df)

    # Download link for processed file
    st.download_button(label='Download Processed Data',
                       data=df.to_csv(index=False),
                       file_name='processed_data.csv',
                       mime='text/csv')
