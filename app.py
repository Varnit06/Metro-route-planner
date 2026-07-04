import streamlit as st
from Simulator import MetroSystem

st.title("🚇 Welcome to Metro Route Planner")

@st.cache_resource
def load_metro():
    metro = MetroSystem()
    metro.load_data("Data.txt")
    metro.build_graph()
    return metro

metro = load_metro()
stations = metro.graph.keys()

src_stn = st.selectbox("Source station", stations)
dest_stn = st.selectbox("Destination station", stations)
time = st.text_input("Current Time","09:57")


if st.button("Find Route"):
    result = metro.find_route(src_stn, dest_stn, time)
    if result["success"]:
        st.subheader("🚇 Route")

        st.write("**Next Train:**", result["next_train"])

        st.write("**Route:**")
        st.write(" → ".join(result["route"]))

        st.write("**Total Stations:**", result["station_count"])

        st.write("**Travel Time:**", f'{result["travel_time"]} minutes')

        st.write("**Expected Arrival:**", result["arrival_time"])

    else:
        st.error(result["message"])





