# require pandas, openpyxl
# the excel file must be in the MS team format and delete the top first merge cell.

import streamlit as st
import pandas as pd


def clean_file(file):
    data = pd.read_excel(file)

    # Extracting student IDs from the email addresses
    data['ID'] = data['Email Address'].apply(lambda email: email.split('@')[0])

    # Selecting the relevant columns
    relevant_columns = ['Full Name', 'ID',
                        'Assignments', 'Points', 'Max Points']

    # Filtering the data
    filtered_data = data[relevant_columns]
    filtered_data['percent_point'] = filtered_data['Points'] / \
        filtered_data['Max Points'] * 100

    st.write("Clean data")
    pivoted_data = filtered_data.pivot_table(
        index=['Full Name', 'ID'], columns='Assignments', values='Points', aggfunc='first')
    st.dataframe(pivoted_data.reset_index())

    pivoted_data = filtered_data.pivot_table(
        index=['Full Name', 'ID'], columns='Assignments', values='percent_point', aggfunc='first')

    # Resetting index to make Full Name and ID as columns
    final_data = pivoted_data.reset_index()

    return final_data


# Streamlit UI
st.title("MS Teams Student Score and Grade Calculator")


uploaded_file = st.file_uploader(
    "Choose a file", type=['xlsx'], accept_multiple_files=False)
st.write("The excel file must be in the MS team format and delete the top first merge cell."
         )


if uploaded_file is not None:

    # Load the data (replace this with the actual loading code)
    data = clean_file(uploaded_file)

    # Display data
    st.write("Student Data:")
    st.dataframe(data)

    # User inputs for assignment weights
    st.write("Enter the weights for each assignment:")
    weights = {}
    # Assuming assignment columns start from the 4th column
    for assignment in data.columns[2:]:
        weights[assignment] = st.number_input(
            f"Weight for {assignment} (%):", 0, 100, 10)

    # Calculate weighted scores
    if st.button("Calculate Weighted Scores"):
        for assignment in weights:
            data[f'{assignment} Weighted'] = data[assignment] * \
                weights[assignment] / 100
        data['Final Weighted Score'] = data[[
            f'{a} Weighted' for a in weights]].sum(axis=1)
        st.write("Weighted Scores:")
        st.dataframe(data)

    # # User inputs for grade ranges
    # st.write("Enter the grade ranges:")
    # grades = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
    # grade_ranges = {}
    # for grade in grades:
    #     grade_ranges[grade] = st.number_input(
    #         f"Minimum score for {grade}:", 0, 100, 90 if grade == 'A' else 0)

    # # Assign grades
    # if st.button("Assign Grades"):
    #     def assign_grade(score):
    #         for grade, min_score in grade_ranges.items():
    #             if score >= min_score:
    #                 return grade
    #         return 'F'

    #     data['Grade'] = data['Final Weighted Score'].apply(assign_grade)
    #     st.write("Final Grades:")
    #     st.dataframe(data)
