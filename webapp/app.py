import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px

### Config
st.set_page_config(
    page_title="Getaround delay analysis",
    page_icon=":car:",
    layout="wide"
)

### Header 
header_left, title, header_right = st.columns([1,5,1])

with header_left:
    st.write("")

with title:
    st.title("Getaround delay analysis")

    st.markdown("""
    ------------------------
    """)

    st.markdown("""
    ### :car: Context

    When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

    Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car was not returned on time.

    ### 🎯 Goals

    In order to mitigate those issues we have decided to implement a minimum delay between two rentals. A car would not be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

    We have to solve these interrogations :

    - **Threshold** : how long should the minimum delay be?
    
    - **Scope** : should we enable the feature for all cars?, only Connect cars?

    """)


with header_right:
    st.write("")


### Body
body_left, body, body_right = st.columns([1,5,1])

with body_left:
    st.write("")

with body:
    
    # Function to add labels to delays
    def type_delay(x):
        if x < 0 :
            y = "Early arrival"
        elif x < 10 : 
            y = "Delay < 10 mins"
        elif x < 60 :
            y = "10 mins ≤ Delay < 60 mins"
        elif x >= 60 :
            y = "Delay ≥ 60 mins"
        else:
            y = "Not applicable"
        return y

    # Load data and keep them in cache for better performance when refreshing the app
    @st.cache_data
    def load_data():
        df = pd.read_excel("./data/get_around_delay_analysis.xlsx")
        df["is_delay"] = np.where(df["delay_at_checkout_in_minutes"]>=0, 1, 0)
        df["type_delay"] = df["delay_at_checkout_in_minutes"].apply(lambda x: type_delay(x))
        return df

    df = load_data()

    st.markdown("""
    ------------------------
    """)

    st.subheader("Dataset preview")

    if st.checkbox("Show data", key="checkbox1"):
        st.subheader("Overview of the 10 first rows")
        st.write(df.head(10)) 

    st.markdown("""
    ------------------------
    """)

    st.subheader("Features distribution")

    col1, col2, col3 = st.columns(3)

    with col1 :
        pie_data = df["checkin_type"].value_counts().reset_index()
        pie_data.columns = ["checkin_type", "count"]

        fig = px.pie(pie_data, values="count", names="checkin_type",
                    title="Global checkin type proportion", 
                    hover_data=["count"], 
                    hole=0.4)

        st.plotly_chart(fig, use_container_width=True)

    with col2 :
        pie_data = df["is_delay"].value_counts().reset_index()
        pie_data.columns = ["is_delay", "count"]

        fig = px.pie(pie_data, values="count", names=["Yes", "No"],
                    color_discrete_sequence=px.colors.sequential.Burg,
                    title="Global late proportion", 
                    hover_data=["count"], 
                    hole=0.4)

        st.plotly_chart(fig, use_container_width=True)

    with col3 :
        pie_data = df["state"].value_counts().reset_index()
        pie_data.columns = ["state", "count"]

        fig = px.pie(pie_data, values="count", names="state",
                    color_discrete_sequence=px.colors.sequential.Blugrn,
                    title="Global rental state proportion", 
                    hover_data=["count"], 
                    hole=0.4)

        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("We can see that majority of rentals are made via mobile checkin, just over half of rentals are late and majority of locations are not cancelled.")
    
    st.markdown("""
    ------------------------
    """)

    st.subheader("Delay analysis")

    fig = px.bar(df, x="type_delay",
                 title="Propotion of delays", 
                 color="checkin_type")
    
    st.plotly_chart(fig, use_container_width=True)

    # Mean delay time
    mean_delay = round(df.loc[:,"delay_at_checkout_in_minutes"].mean())

    # Mean delay time when late
    mask = (df["is_delay"] == 1)
    mean_delay_late = round(df.loc[mask,"delay_at_checkout_in_minutes"].mean())

    # Mean delay time by checkin type
    df_checkin = df.groupby(df["checkin_type"])["delay_at_checkout_in_minutes"].mean()
    mean_delay_connect = round(df_checkin[0])
    mean_delay_mobile = round(df_checkin[1])

    # Mean delay when late by checkin type
    mask1 = (df["is_delay"] == 1) & (df["checkin_type"] == "connect")
    mask2 = (df["is_delay"] == 1) & (df["checkin_type"] == "mobile")
    mean_delay_late_connect = round(df.loc[mask1,"delay_at_checkout_in_minutes"].mean())
    mean_delay_late_mobile = round(df.loc[mask2,"delay_at_checkout_in_minutes"].mean())

    st.subheader("Some statistics")

    st.markdown("""
        #### By rental
    """)
    
    col1, col2= st.columns(2)
    
    with col1 :
        st.metric("Average delay taking all rentals", mean_delay, "minutes")

    with col2 :
        st.metric("Average delay taking only late rentals", mean_delay_late, "minutes")
    
    st.markdown("""
        #### By rental with check-in type
    """)

    col1, col2= st.columns(2)

    with col1 :
        st.metric("Average delay taking all rentals with connect chek-in type", mean_delay_connect, "minutes")

    with col2 :
        st.metric("Average delay taking all rentals with mobile chek-in type", mean_delay_mobile, "minutes")

    st.markdown("""
    #### By late rental with check-in type
    """)
        
    col1, col2= st.columns(2)

    with col1 :
        st.metric("Average delay taking late rentals with mobile chek-in type", mean_delay_late_connect, "minutes")

    with col2 :
        st.metric("Average delay taking late rentals with mobile chek-in type", mean_delay_late_mobile, "minutes")

    st.markdown("")
    st.markdown("Considering these results, we would recommand the Product Manager to consider creating a threshold for the people that checkin by mobile.")

    mask1 = df["delay_at_checkout_in_minutes"] <= 1000
    mask2 = df["delay_at_checkout_in_minutes"] >= 0

    fig = px.histogram(df.loc[mask1&mask2,:],
                 title="Delays at checkout in minutes",
                 x="delay_at_checkout_in_minutes",
                 color="checkin_type")
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")
    st.markdown("We see that delays over 600mins are in minority, we remove these rows.")

    st.markdown("""
    ------------------------
    """)

    mask = df["delay_at_checkout_in_minutes"] <= 600
    df = df.loc[mask, :]

    # Creating new dataset to analyse consecutive rentals
    df_multiple_rentals = pd.merge(df, df, how="inner", left_on = "previous_ended_rental_id", right_on = "rental_id")

    # Removing columns we do not need
    df_multiple_rentals.drop(
        [
            "delay_at_checkout_in_minutes_x",
            "rental_id_y", 
            "car_id_y", 
            "state_y",
            "time_delta_with_previous_rental_in_minutes_y",
            "previous_ended_rental_id_y",
            "is_delay_x",
            "is_delay_y",
            "type_delay_x",
            "type_delay_y"
        ], 
        axis=1,
        inplace=True
    )

    # Keep rows where we have no missing values to analyse the delay between rentals 
    mask = (df_multiple_rentals["delay_at_checkout_in_minutes_y"].notnull())
    df_multiple_rentals = df_multiple_rentals.loc[mask, :]
    df_multiple_rentals.reset_index(drop=True, inplace=True)

    st.subheader("Consecutive rentals dataset preview")

    if st.checkbox("Show data", key="checkbox2"):
        st.subheader("Overview of the 10 first rows")
        st.write(df_multiple_rentals.head(10))
    
    st.markdown("""
    ------------------------
    """)

    st.subheader("Impact of delay on consecutive rentals")

    st.markdown("""
        #### Overview on rentals and consecutive rentals
    """)
    
    col1, col2, col3= st.columns(3)
    
    with col1 :
        st.metric("Total number of rentals", df.shape[0])

    with col2 :
        st.metric("Total number of consecutive rentals", df_multiple_rentals.shape[0])

    with col3 :
        st.metric("Percentage of consecutive rentals over total rentals", round(df_multiple_rentals.shape[0]*100/df.shape[0],2), "%")
    
    # Compute the delay between rentals
    df_multiple_rentals["delay_between_rentals"] = df_multiple_rentals["time_delta_with_previous_rental_in_minutes_x"] - df_multiple_rentals["delay_at_checkout_in_minutes_y"]
    df_multiple_rentals.sort_values(by ="delay_between_rentals")
    df_multiple_rentals.head()

    # Computations
    mask1 = df_multiple_rentals["delay_between_rentals"] < 0
    mean_delay_between_rentals = df_multiple_rentals.loc[mask1, "delay_between_rentals"].mean()
    nb_rentals_impacted = df_multiple_rentals.loc[mask1, "delay_between_rentals"].count()

    mask2 = mask1 & (df_multiple_rentals["checkin_type_x"] == "mobile")
    nb_mobile_rentals = df_multiple_rentals.loc[mask2, "delay_between_rentals"].count()

    mask3 = mask1 & (df_multiple_rentals["state_x"] == "canceled")
    nb_canceled_rentals = df_multiple_rentals.loc[mask3, "delay_between_rentals"].count()

    st.markdown("""
        #### Statics on consecutive rentals after computing the delay (free time) between two rentals
    """)
    
    col1, col2= st.columns(2)
    
    with col1 :
        st.metric("Mean delay (free time) between late rentals", round(mean_delay_between_rentals), "minutes")

    with col2 :
        st.metric("Number of locations impacted by the late between rentals", nb_rentals_impacted,)
    
    col1, col2= st.columns(2)

    with col1 :
        st.metric("Number of mobile locations impacted by the late between rentals", nb_mobile_rentals)

    with col2 :
        st.metric("Number of locations canceled because of the delay", nb_canceled_rentals)
    
    st.metric("Percentage of consecutive locations impacted by the late over the total locations", round(nb_rentals_impacted*100/df.shape[0],2), "%")

    st.markdown("""
    ------------------------
    """)

    st.markdown("""
    ## Summary
    - Majority of rentals are made via mobile checkin
    - Just over half of rentals are late
    - Majority of locations are not cancelled
    - Mobile rentals have more delay than connect ones
    - Average delay time on all rentals is 60 mins
    - Average delay time is 200mins if only late rentals are counted
    - About 1% of rentals are affected by a delay between two consecutive rentals, this does not necessarily lead to cancellation


    ## Conclusion 
    - Delays are mostly present for mobile rentals, we can recommend to the Product Manager to establish a threshold for this rental scope.
    - Rentals impacted by a delay between two consecutive rentals are a minority (about 1% in our study), and they do not necessarily lead to cancellation. We can inform the Product Manager that it is not necessary to set up a threshold because it would generate more losses than profits for the company and the vehicle owner.
    - If the implementation of a threshold is still validated, knowing that the average duration of a delay between 2 rentals is 44 mins, we anticipate a threshold of 1h between 2 rentals. 
    """)
    
    st.markdown("""
    ------------------------
    """)
    
    st.markdown("")

with body_right:
    st.write("")

### Footer 
empty_space, footer, = st.columns([1,2])

with empty_space:
    st.write("")

with footer:
    st.write(":fire: If you want to learn more, check out [my Github](https://github.com/morganeberrod) :fire:")

