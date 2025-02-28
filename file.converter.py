import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files for conversion and cleaning")

files = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split('.')[-1]
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df.drop_duplicates(inplace=True)  # Fix for inplace issue
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include='number').mean(), inplace=True)  # Corrected method
            st.success("Missing values filled with mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])  # Fixed 'iloc' typo

        format_choice = st.radio(f"Convert {file.name} to", ['csv', 'xlsx'])

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == 'csv':
                df.to_csv(output, index=False)
                mime = 'text/csv'  # Fixed variable name
                new_name = file.name.replace(ext, 'csv')
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                new_name = file.name.replace(ext, 'xlsx')

            output.seek(0)
            st.download_button(label=f"Download {new_name}", data=output, file_name=new_name, mime=mime)

            st.success(f"{file.name} has been converted to {format_choice}")
