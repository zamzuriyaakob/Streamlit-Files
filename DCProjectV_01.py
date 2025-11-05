import streamlit as st
import pandas as pd
import numpy as np
import io   
import csv


# Page setup
st.set_page_config(page_title="CLEAR-Data Cleaning Station", layout="wide", page_icon="📊")
st.title("📊 Data Cleaning Station V1.0 - by zamzuri")
st.write("Upload your CSV or Excel file to begin exploring and cleaning your data.")

# Detect separator from sample
def detect_separator(file_obj):
    sample = file_obj.read(2048).decode('utf-8', errors='ignore')
    file_obj.seek(0)  # Reset pointer
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except csv.Error:
        return ','  # Default fallback

# Upload and detect separator
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_name = uploaded_file.name
    st.write(f"✅ File uploaded: `{file_name}`")

    if file_name.endswith('.csv'):
        separator = detect_separator(uploaded_file)
        st.write(f"🔍 Detected Separator: (`{separator}`)")

        try:
            df = pd.read_csv(uploaded_file, sep=separator)
            st.success("CSV file loaded.")
        except Exception as e:
            st.error(f"❌ Failed to load with `{separator}`: {e}")
            st.info("Trying fallback separator `,`...")
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=',')
            st.success("CSV loaded with fallback separator.")
    else:
        df = pd.read_excel(uploaded_file)
        st.success("Excel file loaded.")

    # Continue with EDA and Cleaning modules...

    # --- Section 1: Data Summary ---
    st.header("📋 Data Summary")
    st.write("### 🔍 Preview")
    st.dataframe(df.head())

    st.write("### 📐 Dimensions")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    st.write("### ❓ Missing & Duplicate Info")
    st.write(f"**Missing Values (Total):** {df.isnull().sum().sum()}")
    st.write(f"**Duplicate Rows:** {df.duplicated().sum()}")

    st.write("### 🧬 Data Types")
    st.dataframe(df.dtypes.reset_index().rename(columns={'index':'Column', 0:'Type'}))

    st.write("### 📊 Statistical Summary")
    st.dataframe(df.describe())

    st.write("### 🔤 Non-Numeric Summary")
    st.dataframe(df.describe(include='object'))

    # --- Section 2: Data Cleaning ---
    st.header("🧹 Data Cleaning Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧽 Remove Missing Values"):
            cleaned_df = df.dropna()
            st.success("Missing values removed.")
            st.download_button("📥 Download Cleaned CSV", cleaned_df.to_csv(index=False), file_name="cleaned_missing_removed.csv")

    with col2:
        if st.button("🔧 Handle Missing (fillna/interpolate)"):
            filled_df = df.copy()
            for col in filled_df.select_dtypes(include='object'):
                filled_df[col] = filled_df[col].fillna("Unknown")
            for col in filled_df.select_dtypes(include=np.number):
                filled_df[col] = filled_df[col].interpolate()
            st.success("Missing values handled.")
            st.download_button("📥 Download Filled CSV", filled_df.to_csv(index=False), file_name="cleaned_missing_handled.csv")

    with col3:
        if st.button("🧹 Remove Duplicates"):
            dedup_df = df.drop_duplicates()
            st.success("Duplicate rows removed.")
            st.download_button("📥 Download Deduplicated CSV", dedup_df.to_csv(index=False), file_name="cleaned_duplicates_removed.csv")



 # --- Section 2: Data Cleaning ---
    st.header("📍 Drop and Mapping Data")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗑️ Drop Columns from Dataset")

        # Multiselect remove columns
        drop_cols = st.multiselect("Select Drop Column", df.columns.tolist())

        # Butang untuk sahkan pembuangan
        if st.button("🚮 Drop Selected Column"):
            if drop_cols:
                df_dropped = df.drop(columns=drop_cols)
                st.success(f"{len(drop_cols)} Column dropped.")
                st.write("📋 Generade new dataset :")
                st.dataframe(df_dropped.head())

                # Butang untuk muat turun dataset baru
                st.download_button("📥 Download New Dataset", df_dropped.to_csv(index=False), file_name="dataset_dropped_columns.csv")
            else:
                st.info("Column Drop Not Selected.")
    with col2:
        st.subheader("🔢 Map Categorical Values to Numbers")

        # Step 1: Filter columns with < 5 unique values
        eligible_cols = [
            col for col in df.select_dtypes(include='object').columns
            if len(df[col].dropna().unique()) < 5
        ]

        selected_col = st.selectbox("Select a column to map (max 4 unique values)", eligible_cols)

        if selected_col:
            unique_vals = df[selected_col].dropna().unique()
            st.write(f"📌 Unique values in `{selected_col}`:")
            st.write(unique_vals)

            # Step 2: Manual mapping input
            st.write("🧮 Assign numeric values to each category:")
            mapping_dict = {}
            for val in unique_vals:
                num = st.number_input(f"Value for '{val}'", min_value=0, step=1, key=f"{selected_col}_{val}")
                mapping_dict[val] = num

            st.write("📋 Mapping preview:")
            st.json(mapping_dict)

            # Step 3: Apply mapping
            if st.button("✅ Apply Mapping"):
                df_mapped = df.copy()
                df_mapped[selected_col] = df_mapped[selected_col].map(mapping_dict)
                st.success(f"Column `{selected_col}` has been mapped to numeric values.")
                st.dataframe(df_mapped[[selected_col]].head())

                st.download_button("📥 Download Mapped Dataset", df_mapped.to_csv(index=False), file_name=f"{selected_col}_mapped.csv")





    st.subheader("🔍 Select Columns to Explore Further")

    # Multiselect for column selection
    columns = st.multiselect("Choose columns to preview", df.columns.tolist())

    # Radio button for preview mode
    preview_mode = st.radio("Select preview mode", ["Head only", "Tail only", "Head & Tail"])

    st.subheader("📊 Preview Data")

    # Apply logic based on selection
    if columns:
        if preview_mode == "Head only":
            st.dataframe(df[columns].head())
        elif preview_mode == "Tail only":
            st.dataframe(df[columns].tail())
        else:  # Head & Tail
            st.dataframe(pd.concat([df[columns].head(), df[columns].tail()]))
    else:
        st.info("No columns selected. Previewing entire dataset.")
        if preview_mode == "Head only":
            st.dataframe(df.head())
        elif preview_mode == "Tail only":
            st.dataframe(df.tail())
        else:
            st.dataframe(pd.concat([df.head(), df.tail()]))




    # --- Section 3: Visualization ---
    st.header("📈 Data Visualization")

    x_axis = st.selectbox("Select X-axis column", df.columns)
    y_axis = st.selectbox("Select Y-axis column", df.columns)

    col4, col5 = st.columns(2)

    with col4:
        if st.button("📉 Click Here For Line Graph"):
            st.line_chart(df[[x_axis, y_axis]].dropna())

    with col5:
        if st.button("📊 Click Here For Bar Chart"):
            st.bar_chart(df[[x_axis, y_axis]].dropna())

