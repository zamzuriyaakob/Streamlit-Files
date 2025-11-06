import streamlit as st
import pandas as pd
import numpy as np
import io 
import csv

st.set_page_config(
    page_title="Analyze My Data",
    layout="wide",
    page_icon="☄️")

st.title("📊 Analyze My Data")
st.write("Upload your CSV file and explore your data interactively.")


#uploading csv file
#st.file_uploader("📂Upload your CSV file", type=["csv"]) then assign variable

uploaded_file = st.file_uploader("📂Upload your CSV file", type=["csv"])


#



#PART 02: Data Exploration
if uploaded_file is not None:
    try:
        #if using separator other than comma
        '''sample = uploaded_file.read(1024).decode('utf-8')
       
        uploaded_file.seek(0)  # Reset pointer to start
        dialect = csv.Sniffer().sniff(sample)
        separator = dialect.delimiter
        df = pd.read_csv(uploaded_file, sep=separator)'''
        df=pd.read_csv(uploaded_file)

        #converting boolean columns as string to avoid issues
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(str)
        #check data separator if issues arise
        
        
        #if want to change column names to other names
        #df[xxx_cols] = df[bool_cols].astype(str)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        st.stop()
    st.success("File uploaded successfully!")
   #st.write("### 🧩 File Name :",uploaded_file.name," uploaded using seperator type -> (",separator,")")
    st.write("### Data Preview (H3 font here)")
    st.dataframe(df.head())
    
    st.write("### Data Overview")
    st.write(f"**Number of Rows:** {df.shape[0]}")
    st.write("**Number of Columns:**",df.shape[1])
    st.write("**Number of missing values per column:**",int(df.isnull().sum().sum()))  
    #st.write("**Number of missing values per column:**",df.isnull().sum())
    st.write("**Number of duplicate rows:**",df.duplicated().sum())

    st.subheader("ℹ️Complete summary of dataset")
    #st.dataframe(df.info()describe(include='all').T) info does not return any values
    buffer=io.StringIO()
    df.info(buf=buffer)
    s=buffer.getvalue()
    st.text(s)
    
    st.write("### 📊Statistical Summary")
    st.dataframe(df.describe())

    st.write("### 🔍Statistic Summary Non-Numerical Feature")
    st.dataframe(df.describe(include='object'))

    st.subheader("🔍Select Columns to Explore Further Analysis")
    #multiselect box
    columns=st.multiselect("Choose columns",df.columns.tolist())

    st.subheader("📈Preview Data")

    

    if columns: 
        st.dataframe(df[columns].head())
    else:
        st.info("Select NONE, previewing entire dataset")
        st.dataframe(df.head())


    
        