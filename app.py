
import streamlit as st
import pandas as pd

# Step 1: Page configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 04",
    page_icon="🎓",
    layout="wide"
)

# Step 2: Initialize Session State
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

# Step 3: Load student data from CSV
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. "
            "Please place it in the same folder as app.py."
        )
        st.stop()

student_df = load_student_data()

# Step 4: Risk classification function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Step 5: Add Risk Level column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# Step 6: Sidebar navigation
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

# Step 7: Home Page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Student Risk Monitoring System")

    st.write("Welcome to Lab 04.")

    st.write(
        "This application uses student data to monitor academic "
        "performance and identify students who may need support."
    )

    st.success("Lab 04 app is running successfully!")

# Step 8: Dashboard Page
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard provides an overview of student performance "
        "using data loaded from students.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()

    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric(
            "Average Attendance",
            f"{round(average_attendance, 2)}%"
        )

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.dataframe(student_df)

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

# Step 9: Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write("Inspect the dataset loaded from students.csv.")

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

# Step 10: Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Student Risk Checker")

    st.write(
        "Enter student information to check the risk level "
        "based on score and attendance."
    )

    # Create a form
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")

        input_score = st.number_input(
            "Score",
            min_value=0,
            max_value=100,
            value=50
        )

        input_attendance = st.number_input(
            "Attendance",
            min_value=0,
            max_value=100,
            value=50
        )

        submitted = st.form_submit_button("Check Risk")

    # Validate and process form submission
    if submitted:

        if input_name.strip() == "":
            st.error("Please enter the student name.")

        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )

            # Supportive feedback
            if risk_result == "Low Risk":
                feedback = "Student appears on track."
                st.success(f"Risk Level: {risk_result}")

            elif risk_result == "Medium Risk":
                feedback = "Monitor progress and provide guidance."
                st.warning(f"Risk Level: {risk_result}")

            else:
                feedback = "Student may need additional support."
                st.error(f"Risk Level: {risk_result}")

            st.write("Student Name:", input_name)
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)
            st.info(feedback)

            # Save result in Session State
            st.session_state["risk_history"].append({
                "Student Name": input_name,
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result,
                "Feedback": feedback
            })

    # Recent Risk Checks
    st.subheader("Recent Risk Checks")

    if st.session_state["risk_history"]:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )

        st.dataframe(history_df, use_container_width=True)

        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.rerun()

    else:
        st.info("No risk checks have been recorded yet.")

# Step 11: About Page
else:
    st.title("About EduRisk Analytics")

    st.write("This application is part of Lab 04.")

    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Forms, Validation, and Session State")

    st.info(
        "This application uses Streamlit forms, input validation, "
        "and Session State to manage student risk-check results."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used "
        "responsibly to support learning and student success."
    )
