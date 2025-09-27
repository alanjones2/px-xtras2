import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import px_xtras2 as pxx

st.title("Extra Plotly Charts")

st.header("Waterfall Chart - Profit Breakdown")
wf_data = pd.DataFrame({
    "Category": ["Revenue", "COGS", "Operating Expenses", "Taxes", "Net Profit"],
    "Value": [100000, -50000, -20000, -10000, 0],
})
fig_wf = pxx.waterfall(df=wf_data, 
                   categories_col='Category',
                   values_col='Value',
                   title="Company Profit Waterfall"
                   )
st.plotly_chart(fig_wf)

st.header("Waterfall Chart - Profit Breakdown")

fig_wf = pxx.waterfall(
                   categories=["Revenue", "COGS", "Operating Expenses", "Taxes", "Net Profit"],
                   values=[100000, -50000, -20000, -10000, 0],
                   title="Company Profit Waterfall (list version)"
        )
st.plotly_chart(fig_wf)

# --- Waterfall Chart ---
st.header("Waterfall Chart")
waterfall_df = pd.DataFrame({
    'Category': ["Year beginning", "Profit1", "Loss1", "Q1", "Profit2", "Loss2", "Q2"],
    'Value': [100, 50, -20, 0, 40, -10, 0],
    'measure': ['absolute','relative', 'relative','total', 'relative','relative','total']

})
measure = ['absolute','relative', 'relative','total', 'relative','relative','total']
fig_waterfall = pxx.waterfall(df=waterfall_df, 
                             categories_col='Category', 
                             values_col='Value', 
                             measure_col='measure',
                             title="Profit/Loss",
                             color='blue'
                             )
st.plotly_chart(fig_waterfall)

st.write("---")

# --- Waffle Chart ---
st.header("Waffle Chart")
waffle_data = {'Others': 54, 'LD': 72, 'Conservative': 121, 'Labour': 403}
waffle_df = pd.DataFrame(list(waffle_data.items()), columns=['Party', 'Seats'])

fig_waffle = pxx.waffle(df=waffle_df, 
                       categories_col='Party', 
                       values_col='Seats',
                       title='Waffle Chart of MPs',
                       #local_colors=['black', 'yellow', 'blue', 'red']
                       #startcolor='yellow',
                       #endcolor='darkgreen',
                       )
st.plotly_chart(fig_waffle)

fig_waffle = pxx.waffle(df=waffle_df, 
                       categories_col='Party', 
                       values_col='Seats',
                       title='Waffle Chart of MPs',
                       local_colors=['black', 'yellow', 'blue', 'red']
                       #startcolor='yellow',
                       #endcolor='darkgreen',
                       )
st.plotly_chart(fig_waffle)

fig_waffle = pxx.waffle(df=waffle_df, 
                       categories_col='Party', 
                       values_col='Seats',
                       title='Waffle Chart of MPs',
                       #local_colors=['black', 'yellow', 'blue', 'red']
                       startcolor='yellow',
                       endcolor='darkgreen',
                       width=50
                       )
st.plotly_chart(fig_waffle)

st.write("---")

# --- Dumbbell Chart ---
st.header("Dumbbell Chart")
dumbbell_df = pd.DataFrame({
    'Country': ['USA', 'Canada', 'UK', 'Germany', 'France'],
    '2020': [10, 12, 9, 14, 11],
    '2021': [12, 15, 11, 15, 12]
})

fig_dumbbell = pxx.dumbbell(df=dumbbell_df, 
                           categories_col='Country', 
                           values1_col='2020', 
                           values2_col='2021',
                           label1='2020',
                           label2='2021',
                           title='Dumbbell Chart Example (Dark Template)',
                           template='plotly_dark')
st.plotly_chart(fig_dumbbell)

# --- Vertical Dumbbell Chart ---
st.header("Vertical Dumbbell Chart")
fig_dumbbell_v = pxx.dumbbell(df=dumbbell_df, 
                             categories_col='Country', 
                             values1_col='2020', 
                             values2_col='2021',
                             label1='2020',
                             label2='2021',
                             title='Vertical Dumbbell Chart Example',
                             orientation='v',
                             width=500)
st.plotly_chart(fig_dumbbell_v)

fig_range = pxx.line_range(df=dumbbell_df, 
                           categories_col='Country', 
                           values1_col='2020', 
                           values2_col='2021',
                           label1='2020',
                           label2='2021',
                           title='Range Chart Example')
st.plotly_chart(fig_range)


df_life = pd.read_csv('data/lifeExp.csv').round(1)

dumbbell_df = pd.DataFrame({
    'country': ['France', 'Germany', 'Greece', 'Spain'],
    '1952': [67.41, 67.5, 65.86, 64.94],
    '2002': [79.59, 78.67, 78.25, 79.78]
})


st.dataframe(df_life)

fig_dumbbell = pxx.dumbbell(df=df_life, 
                           categories_col='country', 
                           values1_col='1952', 
                           values2_col='2002',
                           label1='1952',
                           label2='2002',
                           title='Life expectancy chart',
                           )
st.plotly_chart(fig_dumbbell)

fig_dumbbell2 = pxx.dumbbell(df=df_life, 
                           categories_col='country', 
                           values1_col='1952', 
                           values2_col='2002',
                           label1='1952',
                           label2='2002',
                           title='Life expectancy chart',
                           orientation='v'
                           )
st.plotly_chart(fig_dumbbell2)

fig_range = pxx.line_range(df=df_life, 
                           categories_col='country', 
                           values1_col='1952', 
                           values2_col='2002',
                           label1='1952',
                           label2='2002',
                           title='Range Chart Example')
st.plotly_chart(fig_range)

st.write("---")

# --- Lollipop Chart ---
st.header("Lollipop Chart")
lollipop_df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': [10, 25, 15, 30, 20]
})
fig_lollipop = pxx.lollipop_chart(df=lollipop_df, 
                                 categories_col='Category', 
                                 values_col='Value', 
                                 title='Lollipop Chart Example (Custom Height)', height=350)
st.plotly_chart(fig_lollipop)

st.write("---")

# --- Metric ---
st.header("Metric")
fig_metric = pxx.metric(title="Sales", value=12345, delta=123, prefix="$")
st.plotly_chart(fig_metric)

st.write("---")

# --- Slope Chart ---
st.header("Slope Chart")
slope_df = pd.DataFrame({
    'Year': [2020, 2021],
    'USA': [10, 12],
    'Canada': [12, 15],
    'UK': [9, 11],
    'Germany': [14, 15],
    'France': [11, 12]
})
fig_slope = pxx.slope_chart(df=slope_df, categories_col='Year', values_cols=['USA', 'Canada', 'UK', 'Germany', 'France'], title='Slope Chart Example')
st.plotly_chart(fig_slope)
