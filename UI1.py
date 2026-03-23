import pickle
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crane Analyzer", layout="wide")

st.title("🏗️ Crane Load Capacity Analyzer (LR 1280)")
st.markdown("### Select configuration and get lifting capacity instantly")

# Load Data
with open("data.pkl", "rb") as f:
    data = pickle.load(f)

# Fix columns
for i in data[30]:
    data[30][i] = data[30][i].rename(columns={'Radius (m)': '0'})
for i in data[15]:
    data[15][i] = data[15][i].rename(columns={'Radius (m)': '0'})

list_angles = [i for i in data][::-1]
final_angles = list_angles[2:4] + [15, 30] + list_angles[4:]

# UI Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/main-boom.png")
    st.subheader("Main Boom")

with col2:
    st.image("images/l-boom.png")
    st.subheader("L-Boom")

with col3:
    st.image("images/luffing-jib.png")
    st.subheader("Luffing Jib")

option = st.selectbox(
    "Select Crane Type:",
    ("Main Boom", "L-Boom", "Luffing Jib"),
)

# ---------------- MAIN BOOM ----------------
if option == "Main Boom":
    df = data['main-boom']

    lengths = [float(i[:-1]) if i.endswith('m') else float(i) for i in df.columns[1:]]
    selected_length = st.selectbox("Boom Length (m)", sorted(lengths))

    radius = st.selectbox("Radius (m)", sorted(df['Radius'].unique()))

    col = df.columns[lengths.index(selected_length) + 1]
    capacity = df[df['Radius'] == radius][col].max()

    st.success(f"Capacity: {capacity} tons")

# ---------------- L-BOOM ----------------
elif option == "L-Boom":
    df = data['l-boom']

    lengths = sorted([float(i) for i in df.columns[:-1]])
    selected_length = st.selectbox("L-Boom Length (m)", lengths)

    radius = st.selectbox("Radius (m)", sorted(df['0'].unique()))

    capacity = df[df['0'] == radius][str(selected_length)].max()

    st.success(f"Capacity: {capacity} tons")

# ---------------- LUFFING JIB ----------------
else:
    angle = st.selectbox("Angle", final_angles[2:])
    df_angle = data[angle]

    main_boom = st.selectbox("Main Boom Length", sorted(df_angle.keys()))
    df_config = df_angle[main_boom]

    jib_lengths = sorted(int(c) for c in df_config.columns[1:] if c != '0')
    selected_jib = st.selectbox("Jib Length", jib_lengths)

    radius = st.selectbox("Radius", sorted(df_config['0'].unique()))

    capacity = df_config[df_config['0'] == radius][str(selected_jib)].max()

    st.success(f"Capacity: {capacity} tons")