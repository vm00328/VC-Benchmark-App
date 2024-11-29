import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout = "wide")

@st.cache_data
def load_benchmark_data(sheet_name):
    file_path = os.path.join(os.path.dirname(__file__), "../data/benchmark_data.xlsx")
    benchmark_data = pd.read_excel(file_path, sheet_name = sheet_name)
    return benchmark_data

logo_path = os.path.join(os.path.dirname(__file__), "static/ML_logo.png")
st.sidebar.image(logo_path, use_container_width = True)

# UI components
st.title("Fund Performance Benchmarking")

# Input fields
st.sidebar.title("Fund Details")
st.sidebar.info("Input your VC fund details to compare against industry benchmarks.")

with st.sidebar.expander("🎯 Fund Details", expanded = True):
    fund_name = st.text_input("Enter Fund Name")
    vintage = st.selectbox("Select Vintage", options = [2015, 2016])
    geography = st.selectbox("Fund Manager Location", options = ["Europe (25 funds)", "US (95 funds)", "Europe & US (120 funds)"])

# Input fields for performance metrics
with st.sidebar.expander("📊 Performance Metrics", expanded = True):
    net_irr = st.number_input("Net IRR (%)", step = 0.01)
    net_tvpi = st.number_input("Net TVPI (X)", min_value = 0.0, step = 0.01)
    net_dpi = st.number_input("Net DPI (X)", min_value = 0.0, step = 0.01)

if st.sidebar.button("Submit"):

    # Map geography selection to the appropriate benchmark sheet
    sheet_mapping = {
        "Europe (25 funds)": "VC EU Benchmark",
        "US (95 funds)": "VC US Benchmark",
        "Europe & US (120 funds)": "VC EU & US Benchmark"
    }

    selected_sheet = sheet_mapping.get(geography)
    data = load_benchmark_data(selected_sheet)
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
    
    col1, col2, col3 = st.columns(3)

    for i, (metric_name, user_value) in enumerate(metrics.items()):
        row_labels = metric_rows[metric_name]
        benchmark_values = data[data["Metrics"].isin(row_labels)][selected_vintage_col].values
        
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

        # Assign each chart to a column
        if i == 0:
            col1.plotly_chart(fig, use_container_width=True)
        elif i == 1:
            col2.plotly_chart(fig, use_container_width=True)
        elif i == 2:
            col3.plotly_chart(fig, use_container_width=True)

    # Footer Section
    st.markdown("---")  # Horizontal line for separation

    # Dynamic data insights
    footer_text = f"""
    <div style='text-align: center; font-size: 12px; color: grey; padding-top: 10px;'>
        <b>Data Source:</b> Preqin | 
        <b>Vintage Years Covered:</b> 2015 & 2016 | 
        <b>Sector</b>: Sector-Agnostic | 
        <b>Geography</b>: Europe & US<br>
    </div>
    """

    st.markdown(footer_text, unsafe_allow_html = True)