import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import os
print(os.getcwd())

@st.cache_data
def load_benchmark_data():
    file_path = os.path.join(os.path.dirname(__file__), "../data/preqin_vc_benchmark_data_2015_2016.xlsx")
    benchmark_data = pd.read_excel(file_path)
    return benchmark_data

data = load_benchmark_data()

st.sidebar.image("../static/ML_logo.png", use_container_width = True)

# UI components
st.title("Fund Performance Benchmarking")

# Input fields
st.sidebar.title("Fund Details")
st.sidebar.info("Input your VC fund details to compare against industry benchmarks.")

with st.sidebar.expander("🎯 Fund Details", expanded = True):
    fund_name = st.text_input("Enter Fund Name")
    vintage = st.selectbox("Select Vintage", options = [2015, 2016])

# Input fields for performance metrics
with st.sidebar.expander("📊 Performance Metrics"):
    net_irr = st.sidebar.number_input("Net IRR (%)", step = 0.01)
    net_tvpi = st.sidebar.number_input("Net TVPI (X)", min_value = 0.0, step = 0.01)
    net_dpi = st.sidebar.number_input("Net DPI (X)", min_value = 0.0, step = 0.01)

if st.sidebar.button("Submit"):
    selected_vintage_col = vintage
    
    # Rows for each metric
    metric_rows = {
        "Net IRR (%)": [
            "Top Decile (90%) IRR",
            "Top Quartile (75%) IRR",
            "Average IRR"
        ],
        "Net TVPI (X)": [
            "Top Decile (90%) TVPI",
            "Top Quartile (75%) TVPI",
            "Average TVPI"
        ],
        "Net DPI (X)": [
            "Top Decile (90%) DPI",
            "Top Quartile (75%) DPI",
            "Average DPI"
        ]
    }
    
    # Bar charts for each metric
    metrics = {
        "Net IRR (%)": net_irr,
        "Net TVPI (X)": net_tvpi,
        "Net DPI (X)": net_dpi
    }
    
    for metric_name, user_value in metrics.items():
        row_labels = metric_rows[metric_name]
        benchmark_values = data[data["Unnamed: 0"].isin(row_labels)][selected_vintage_col].values
        
        categories = ["Top Decile (90%)", "Top Quartile (75%)", "Average", fund_name]
        values = list(benchmark_values) + [user_value]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = categories,
            y = values,
            marker_color = ["#4E79A7", "#76B7B2", "#F28E2B", "#E15759"],
            text = [f"{v:.2f}" for v in values],
            textposition = 'auto',
        ))
        
        fig.update_layout(
            title = {
                'text': f"{metric_name} Benchmark",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title = "Categories",
            yaxis_title = metric_name,
            font = dict(family = "Arial, sans-serif", size = 14, color = "Black"),
            plot_bgcolor = 'white',
            bargap = 0.2,
            xaxis = dict(showgrid = False),
            yaxis = dict(showgrid = True, gridcolor = 'lightgrey')
        )
        
        st.plotly_chart(fig)