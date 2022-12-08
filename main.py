import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(layout="wide")
school_data = pd.read_csv('2006_-_2012_School_Demographics_and_Accountability_Snapshot.csv')

def add_bg_from_local(image):
    with open(image, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

add_bg_from_local('background.webp')

st.header("Find the best fit for your kids & you!")


st.sidebar.header("Select the condition")
distribution = st.sidebar.selectbox(
    "School Distribution",
    options=(school_data.sort_values(by="Dist").Dist.unique()),
)
df_selection = school_data.query(
    "Dist == @distribution"
)

school_type = st.sidebar.selectbox(
    "School type",
    ["Pre-kindergarten","Kindergarten","Primary school","Middle school", "High school"]
)

if school_type == "Pre-kindergarten":
    df_selection = df_selection[df_selection["is_prek"] == True]
if school_type == "Kindergarten":
    df_selection = df_selection[df_selection["is_k"] == True]
if school_type == "Primary school":
    df_selection = df_selection[df_selection["is_primary"] == True]
if school_type == "Middle school":
    df_selection = df_selection[df_selection["is_middle"] == True]
if school_type == "High school":
    df_selection = df_selection[df_selection["is_high"] == True]

tags = st.sidebar.multiselect(
    "Info Interested",
    ["Free Lunch","Gender","Racial","Special ED"]
)

school_name = df_selection["name"]
school_name = school_name.drop_duplicates()


for item in school_name:
    with st.expander(item):
        st.subheader(item)
        new = df_selection.loc[df_selection["name"] == item]
        latest = new.iloc[-1]
        # latest
        enrollment = px.bar(new, x="year", y='total_enrollment',
                            labels=dict(year="School Year", total_enrollment="Total Enrollment Number"))
        enrollment
        if "Free Lunch" in tags:
            st.subheader("Free & Reduced lunch")
            free_lunch = px.line(new, x="year", y='free_lunch', markers=True,
                                 labels=dict(year="School Year", free_lunch="Free Lunch Percentage(%)"))
            free_lunch.update_yaxes(range=[0,100])
            free_lunch
        if "Gender" in tags:
            st.subheader("Gender Ratio")
            label = ["Male", "Female"]
            value = [latest["male_num"],latest["female_num"]]
            gender = go.Figure(data=[go.Pie(labels=label, values=value)])
            gender
        if "Racial" in tags:
            st.subheader("Racial Ratio")
            label = ["Asian","Black", "Hispanic","White"]
            value = [latest["asian_num"],latest["black_num"],latest["hispanic_num"],latest["white_num"]]
            racial = go.Figure(data=[go.Pie(labels=label, values=value)])
            racial
        if "Special ED" in tags:
            st.subheader("Special ED")
            special_ed = px.line(new, x="year", y='sped_percent', markers=True,
                                 labels=dict(year="School Year", sped_percent="Special ED Percentage(%)"))
            special_ed.update_yaxes(range=[0, 100])
            special_ed




# tags
# df_selection