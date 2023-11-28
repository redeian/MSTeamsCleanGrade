# require pandas, openpyxl
# the excel file must be in the MS team format and delete the top first merge cell.


# import streamlit as st

# st.title('Uber pickups in NYC')
import pandas as pd

# Load the CSV file
file_path = 'rawx.xlsx'
data = pd.read_excel(file_path)

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

# Previewing the final data
final_data.head()

# Saving the final data to a CSV file
output_file_path = 'clean.csv'
final_data.to_csv(output_file_path, index=False)
