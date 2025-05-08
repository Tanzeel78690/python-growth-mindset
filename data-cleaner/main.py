import streamlit as st
import pandas as pd
from io import BytesIO

# Page config
st.set_page_config(page_title="📂 File Converter & Cleaner", layout="wide")
st.title("🧼📁 File Converter & Cleaner")
st.write("Upload your **CSV** or **Excel** files to clean, preview, and convert them effortlessly! 🚀")

# File uploader
files = st.file_uploader("📤 Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

# File processing
if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.markdown(f"### 📄 Preview: `{file.name}`")
        st.dataframe(df.head(), use_container_width=True)

        # Show missing value summary
        if df.isnull().values.any():
            st.warning("⚠️ Missing values detected in your file.")
            st.markdown("#### 📊 Missing Values Summary")
            st.dataframe(df.isnull().sum().to_frame("Missing Count"), use_container_width=True)

        # Fill missing values
        if st.checkbox(f"🧯 Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled with column means.")
            st.dataframe(df.head(), use_container_width=True)

        # Select columns
        st.markdown(f"#### 🧮 Select Columns to Keep - `{file.name}`")
        selected_columns = st.multiselect("Choose columns:", df.columns.tolist(), default=df.columns.tolist(), key=f"columns_{file.name}")
        df = df[selected_columns]
        st.dataframe(df.head(), use_container_width=True)

        # Show chart
        if st.checkbox(f"📊 Show Chart - {file.name}", key=f"chart_{file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Format selection
        format_choice = st.radio(f"🛠️ Convert `{file.name}` to:", ["CSV", "Excel"], key=f"format_{file.name}")

        # Download button
        if st.button(f"⬇️ Download `{file.name}` as {format_choice}", key=f"download_{file.name}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"

            output.seek(0)
            st.download_button("📥 Download File", file_name=new_name, data=output, mime=mime, key=f"dl_{file.name}")
            st.success("✅ File processed and ready for download!")

