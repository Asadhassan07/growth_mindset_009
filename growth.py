import streamlit as st
import pandas as pd
import os
from io import BytesIO  

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>   
    """,
    unsafe_allow_html=True
)

st.title("DataSweeper Sterling Integrator by Asad Ali")
st.write("Transform your data into a clean and structured format 🧹")

uploaded_files = st.file_uploader("📤 Upload your CSV or Excel files here:", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx": 
            df = pd.read_excel(file)
        else:
            st.error(f"🚫 Unsupported file type: {file_ext}")
            continue

       
        st.write("### Initial Data Overview - Preview the top rows of your dataset")
        st.dataframe(df.head())

        
        st.subheader("### Data Cleaning & Preparation 🧹")
        if st.checkbox(f"Clean the data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🚮 Remove Duplicate Entries from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates have been successfully removed!")

            with col2:
                if st.button(f"🔧 Fill Missing Data for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled with the column averages!")

            st.subheader("### Select the Columns You Want to Keep")
            columns = st.multiselect(f"Choose the columns to keep for {file.name}", df.columns, default=df.columns)
            df = df[columns]

          
            st.subheader("### Visualize Your Data 📊")
            if st.checkbox(f"Display Data Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            st.subheader("### Convert Data Format 🔄")
            conversion_type = st.radio(f"Choose which format to convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name} to {conversion_type}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)  
                    file_name = file.name.replace(file_ext, ".csv")  
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False) 
                    file_name = file.name.replace(file_ext, ".xlsx") 
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

                st.success("😍 All files processed successfully!")
