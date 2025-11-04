import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("students_data.csv")  # 👈 Put your CSV file name here

# Title and Header
st.title("🎓 Student Performance Dashboard")
st.header("📊 Overview of Student Data")

# Show complete data
st.dataframe(df)

# Sidebar Filters
st.sidebar.header("🔍 Filter Students")

courses = df["Course"].unique().tolist() if "Course" in df.columns else []
selected_course = st.sidebar.selectbox("Select Course", ["All"] + courses)

cities = df["City"].unique().tolist() if "City" in df.columns else []
selected_cities = st.sidebar.multiselect("Select City", cities, default=cities)

if "Marks" in df.columns:
    min_marks = int(df["Marks"].min())
    max_marks = int(df["Marks"].max())
    marks_filter = st.sidebar.slider("Minimum Marks", min_marks, max_marks, min_marks)
else:
    marks_filter = 0

if "Gender" in df.columns:
    gender_option = st.sidebar.radio("Select Gender", ["All", "Male", "Female"])
else:
    gender_option = "All"

# Filtering Logic
filtered_df = df.copy()

if selected_course != "All":
    filtered_df = filtered_df[filtered_df["Course"] == selected_course]

if selected_cities:
    filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

filtered_df = filtered_df[filtered_df["Marks"] >= marks_filter]

if gender_option != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_option]

# Display Filtered Data
st.subheader("🎯 Filtered Student Data")
st.dataframe(filtered_df)

# Metrics and Insights
if not filtered_df.empty:
    avg_marks = filtered_df["Marks"].mean()
    avg_attendance = filtered_df["Attendance"].mean() if "Attendance" in df.columns else 0
    total_students = len(filtered_df)

    st.metric("Average Marks", f"{avg_marks:.2f}")
    st.metric("Average Attendance", f"{avg_attendance:.2f}%")
    st.metric("Total Students", total_students)

    # ✅ Fixed Indentation here
    if avg_marks > 85:
        st.success("Excellent performance! 🌟")
    elif avg_marks >= 70:
        st.info("Good performance.")
    else:
        st.warning("Needs improvement.")
else:
    st.error("No students match the filters!")

# Search Student
st.subheader("🔎 Search Student by Name")
name_search = st.text_input("Enter Student Name:")

if name_search:
    result = df[df["Name"].str.contains(name_search, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("No student found with that name.")

# Buttons for quick actions
col1, col2 = st.columns(2)

with col1:
    if st.button("Show Top Performers (Marks > 90)"):
        top_students = df[df["Marks"] > 90]
        st.subheader("🏆 Top Performers")
        st.dataframe(top_students)

with col2:
    if st.button("Show All Data"):
        st.subheader("📋 All Student Data")
        st.dataframe(df)

# Charts and Visualizations
st.header("📈 Charts and Visualizations")

if "Marks" in df.columns and "Name" in df.columns:
    st.bar_chart(filtered_df.set_index("Name")["Marks"])

if "Attendance" in df.columns:
    st.line_chart(filtered_df.set_index("Name")["Attendance"])

if "Marks" in df.columns:
    fig, ax = plt.subplots()
    ax.hist(filtered_df["Marks"], bins=10)
    st.pyplot(fig)

# Add Streamlit Logo
st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=250)
