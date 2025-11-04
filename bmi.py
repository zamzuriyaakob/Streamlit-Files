import streamlit as st
import pandas as pd
import altair as alt
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️",layout="centered") 

st.title("⚖️ BMI Calculator")
st.write("Calculate your Body Mass Index (BMI) to assess your weight category.")

st.header("🧍🏽‍♂️Enter your details:")
weight = st.number_input("Weight (kg):", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
height = st.number_input("Height (cm):", min_value=30.0, max_value=300.0, value=170.0, step=0.1)

st.write("📏Your Height in meters is:", height,"cm" )
st.write("🏋🏾‍♂️Your Weight in kilograms is:", weight,"kg" )


#layout




if st.button("Calculate BMI"):
    height_m = height / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    st.success(f"Your BMI **{bmi:.2f}**")

    #bmi categorization
    if bmi<18.5:
        category="Underweight 🙁"
        color="#27DAF5"
    elif 18.5 <= bmi <25:
        category="Normal weight 🙂"
        color="#2CE12C"
    elif 25 <= bmi <30:
        category="Overweight 🤨"
        color="#F5E327"
    else:
        category="Obesity 😟"
        color="#F52727"

    st.markdown(
        f"""
        <div style='background-color:{color};padding:15px;border-radius:10px;text-align:center'>
        <h3>Your BMI Category : {category}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
 



st.header("📊 BMI Range Charts")
bmi_data = pd.DataFrame({
    "Category": ["Underweight", "Normal weight", "Overweight", "Obesity"],
    "BMI Range": [18.5,24.9,29.9,40]
})  

st.bar_chart(bmi_data.set_index("Category"))







st.header("📊 BMI Range Charts")

# Define the data
bmi_data = pd.DataFrame({
    "Category": ["Underweight", "Normal weight", "Overweight", "Obesity"],
    "BMI Range": [18.5, 24.9, 29.9, 40],
    "Color": ["#27DAF5", "#2CE12C", "#F5E327", "#F52727"]  # Custom colors
})

# Create the chart
chart = alt.Chart(bmi_data).mark_bar().encode(
    x=alt.X("Category", sort=None),
    y="BMI Range",
    color=alt.Color("Category", scale=alt.Scale(
        domain=bmi_data["Category"],
        range=bmi_data["Color"]
    ))
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)
