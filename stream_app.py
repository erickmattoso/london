import datetime
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def place_go_today(day):
    fig = plot_figure(go_today[day], values)
    st.plotly_chart(fig, use_container_width=True)
    st.write(to_go[['title']])


def plot_figure(my_df, ranges):
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        hovertext=["Home"],
        hoverinfo='text',
        lon=my_df[my_df['title'] == 'Home']['lng'].to_list(),
        lat=my_df[my_df['title'] == 'Home']['lat'].to_list(),
        marker={"size": 20}))
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        hovertext=list(df.iloc[ranges[0]:ranges[1]].title),
        hoverinfo='text',
        lon=df.iloc[ranges[0]:ranges[1]].lng,
        lat=df.iloc[ranges[0]:ranges[1]].lat,
        marker={"size": 5}))
    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        hovertext=list(my_df.title),
        hoverinfo='text',
        lon=my_df.lng,
        lat=my_df.lat,
        marker={
            'color': 'green',
            'size': 15,
            'opacity': 0.9
        }))
    fig.update_layout(
        showlegend=False,
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": my_df["lng"].mean(), "lat": my_df["lat"].mean()},
            "style": "stamen-terrain",
            "zoom": 11.8})
    try:
        fig.add_trace(go.Scattermapbox(
            lon=[result.get("GET_LOCATION")["lon"]],
            lat=[result.get("GET_LOCATION")["lat"]],
            marker={"size": 15})
        )
    except:
        pass
    fig.update_layout(
        showlegend=False,
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": my_df["lng"].mean(), "lat": my_df["lat"].mean()},
            "style": "stamen-terrain",
            "zoom": 11.8})
    return fig


st.title('Trip to London')
loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    override_height=40,
    debounce_time=0)
csv_csv = pd.read_csv('minha_london.csv')
df = pd.read_csv('all_london.csv')
MYHOME = [["Home", 51.4865817, -0.1024488, 0]]
home = pd.DataFrame(MYHOME)
home.columns = ["title", "lat", "lng", "price"]
values = st.slider('Select a range of values', 0, len(df), (0, len(df)))
fig = plot_figure(csv_csv, values)
st.plotly_chart(fig, use_container_width=True)
st.write(csv_csv[["title", "lat", "lng", "price"]])

i = j = 0
go_today = []
i = j = 0
for n in range(5):
    i = j
    j = i+5
    to_go = pd.concat([home, csv_csv.iloc[i:j], home])
    go_today.append(to_go)

st.title("21/03/2022 - Thursday")
place_go_today(3)

st.title("22/03/2022 - Friday")
place_go_today(4)

st.title("23/03/2022 - Saturday")
place_go_today(1)

st.title("24/03/2022 - Sunday")
place_go_today(2)

st.title("25/03/2022 - Monday")
place_go_today(0)
