"""
px_xtras.py v.0.1.0

A library of helper functions for creating advanced visualizations using Plotly.

MIT License

Copyright (c) 2025 Alan Jones

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import json
import math
from typing import List, Tuple, Dict, Optional

def _prepare_chart_data(df=None, data_map=None):
    """
    Prepares data for charting functions.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        data_map (list of tuples, optional): A list of tuples, where each tuple is
                                             (key, col_name, data_list).

    Returns:
        A tuple of data lists.
    """
    if df is not None:
        # Extract data from DataFrame
        data_from_df = []
        default_col_index = 0
        for _, col_name, _ in data_map:
            col_to_use = col_name or df.columns[default_col_index]
            if col_to_use not in df.columns:
                raise ValueError(f"Column '{col_to_use}' not found in DataFrame.")
            data_from_df.append(df[col_to_use].tolist())
            default_col_index += 1
        return tuple(data_from_df)
    else:
        # Use provided lists
        data_from_lists = []
        for key, _, data_list in data_map:
            if data_list is None:
                raise ValueError(f"If not using a DataFrame, you must provide '{key}'.")
            data_from_lists.append(data_list)
        return tuple(data_from_lists)

def plotly_chart(fig: go.Figure) -> str:
    """
    Converts a Plotly figure into an embeddable HTML string.

    Args:
        fig (go.Figure): The Plotly figure to convert.

    Returns:
        str: An HTML string containing the Plotly chart.
        
    Use st.component to display the chart in Streamlit, 
    e.g. st.components.v1.html(html_string, height=600)
    """
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def get_color_gradient(start_color: str, end_color: str, num_colors: int) -> List[str]:
    """
    Generate a list of colors forming a gradient between two colors.

    Args:
        start_color (str): The starting color (name, hex, or RGB tuple).
        end_color (str): The ending color (name, hex, or RGB tuple).
        num_colors (int): The number of discrete colors to generate.

    Returns:
        List[str]: A list of hex color codes forming the gradient.
    """
    start_rgb = mcolors.to_rgb(start_color)
    end_rgb = mcolors.to_rgb(end_color)
    gradient = [
        tuple(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * t for i in range(3))
        for t in [i / (num_colors - 1) for i in range(num_colors)]
    ]
    return ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for r, g, b in gradient]


def get_section_bounds(x: float = 1, y: int = 4) -> List[Tuple[float, float]]:
    """
    Returns a list of (start, end) tuples for each of the y sections of a bar of length x.

    Args:
        x (float): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[Tuple[float, float]]: List of (start, end) points for each section.
    """
    section_length = x / y
    return [(i * section_length, (i + 1) * section_length) for i in range(y)]


def find_midpoints(x: int, y: int) -> List[float]:
    """
    Returns a list of midpoints for each of the y sections of a bar of length x.

    Args:
        x (int): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[float]: Midpoints of each section.
    """
    indices = range(1, y + 1)
    return [((2 * i - 1) * x) / (2 * y) for i in indices]


def waterfall(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values_col: Optional[str] = None,
    measure_col: Optional[str] = 'measure',
    categories: Optional[List[str]] = None,
    data: Optional[List[float]] = None,
    title: str = "",
    annotation: Optional[List[str]] = None,
    icolor: str = "Green",
    dcolor: str = "Red",
    tcolor: str = "Blue",
    ccolor: str = "Dark Grey",
    color: Optional[str] = None, # Common color for all elements. Defaults to None.
    measure: Optional[List[str]] = None, # A list specifying whether each data point is 'relative' or 'total'. Defaults to None.
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    """
    Create a waterfall chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        categories_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        values_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        measure_col (str, optional): Column name for measure. Defaults to 'measure'.
        categories (List[str], optional): A list of labels for the data points. Ignored if df is provided.
        data (List[float], optional): A list of numerical values for the data points. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        annotation (List[str], optional): A list of annotations for each data point. Defaults to None.
        icolor (str, optional): Color for increasing values. Defaults to "Green".
        dcolor (str, optional): Color for decreasing values. Defaults to "Red".
        tcolor (str, optional): Color for the total value. Defaults to "Blue".
        ccolor (str, optional): Connector line color. Defaults to 'Dark Grey'.
        color (str, optional): Common color for all elements. Defaults to None.
        measure (List[str], optional): A list specifying whether each data point is 'relative' or 'total'. Defaults to None.
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.

    Returns:
        go.Figure: A Plotly Figure containing the waterfall chart.
    """
    def default_measure(cats: List[str]) -> List[str]:
        measure = ['relative'] * (len(cats))
        measure[0] = 'absolute'
        measure[-1] = 'total'
        return measure

    categories, data = _prepare_chart_data(
        df=df,
        data_map=[
            ('categories', categories_col, categories),
            ('values', values_col, data)
        ]
    )

    # Handle measure separately as it's specific to waterfall
    if df is not None and measure_col and measure_col in df.columns:
        measure = df[measure_col].tolist()
    
    if not measure:
        measure = default_measure(categories)
    
    if color:
        icolor = dcolor = tcolor = ccolor = color

    waterfall_params = {
        "orientation": "v",
        "measure": measure,
        "textposition": "outside",
        "y": data,
        "x": categories,
        "connector": {"line": {"color": ccolor}},
        "decreasing": {"marker": {"color": dcolor}},
        "increasing": {"marker": {"color": icolor}},
        "totals": {"marker": {"color": tcolor}},
    }

    if annotation is not None: # Add annotations if provided.
        waterfall_params["text"] = annotation
    

    fig = go.Figure(go.Waterfall(**waterfall_params)).update_layout(title=title, **kwargs)

    return fig


def waffle(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values_col: Optional[str] = None,
    data: Optional[Dict[str, int]] = None,
    title: str = "",
    local_colors: Optional[List[str]] = None,
    startcolor: str = 'lightblue',
    endcolor: str = 'darkblue',
    fig_height: int = 600,
    tile_gap: int = 2,
    grid_width: Optional[int] = None,
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    """
    Create a waffle chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        categories_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        values_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        data (Dict[str, int], optional): A dictionary where keys are categories and values are counts. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        local_colors (List[str], optional): A list of colors for the categories. Defaults to a gradient.
        startcolor (str, optional): Starting color for the gradient. Defaults to 'lightblue'.
        endcolor: str = 'darkblue',
        fig_height: int = 600,
        tile_gap: int = 2,
        grid_width: Optional[int] = None,
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.
    Returns:
        go.Figure: A Plotly Figure containing the waffle chart.
    """
    if df is not None:
        categories, values = _prepare_chart_data(
            df=df,
            data_map=[('categories', categories_col, None), ('values', values_col, None)]
        )
        data = dict(zip(categories, values))
    elif data is None:
        # If df is not provided, data must be.
        raise ValueError("Provide either a DataFrame or a data dictionary.")

    if local_colors is None:
        local_colors = get_color_gradient(startcolor, endcolor, len(data))

    total = sum(data.values())
    number_of_values = len(data.values())
    cat = [idx for idx, count in enumerate(data.values()) for _ in range(count)]

    width = grid_width or math.ceil(math.sqrt(total))
    height = math.ceil(total / width)

    padding_length = width * height - len(cat)
    cat = [np.nan] * padding_length + cat
    b = np.array(cat).reshape((-1, width))

    ranges = get_section_bounds(1, number_of_values)
    colorscale = []
    for i in range(number_of_values):
        colorscale.append([ranges[i][0], local_colors[i % len(local_colors)]])
        colorscale.append([ranges[i][1], local_colors[i % len(local_colors)]])

    fig = go.Figure(data=go.Heatmap(
        z=np.fliplr(b),
        xgap=tile_gap,
        ygap=tile_gap,
        colorbar=dict(
            thickness=20,
            tickvals=find_midpoints(number_of_values - 1, number_of_values),
            ticktext=list(data.keys()),
            outlinecolor='black',
            outlinewidth=0,
        ),
        colorscale=colorscale,
        autocolorscale=False,
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis_scaleanchor="x",
        height=fig_height,
        **kwargs
    )
    return fig


def dumbbell(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values1_col: Optional[str] = None,
    values2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Dumbbell Chart",
    orientation: str = 'h',
    marker_color1: str = 'blue',
    marker_color2: str = 'orange',
    line_color: str = 'gray',
    marker_size: int = 10, # Size of the markers.
    line_width: int = 2, # Width of the connecting lines.
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    """
    Draws a dumbbell chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        categories_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        values1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        values2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        marker_color1 (str, optional): Color for the first set of markers. Defaults to 'blue'.
        marker_color2 (str, optional): Color for the second set of markers. Defaults to 'orange'.
        line_color: str = 'gray',
        marker_size: int = 10,
        line_width: int = 2,
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.

    Returns:
        go.Figure: The resulting dumbbell chart.
    """
    categories, values1, values2 = _prepare_chart_data(
        df=df,
        data_map=[
            ('categories', categories_col, categories),
            ('values1', values1_col, values1),
            ('values2', values2_col, values2)
        ]
    )

    if not (len(categories) == len(values1) == len(values2)):
        raise ValueError("All input lists must have the same length.")

    fig = go.Figure()
    showlegend = bool(label1 and label2)

    
    x_markers1, y_markers1 = (values1, categories) if orientation == 'h' else (categories, values1)
    x_markers2, y_markers2 = (values2, categories) if orientation == 'h' else (categories, values2)

    for cat, val1, val2 in zip(categories, values1, values2):
        x_line_vals, y_line_vals = ([val1, val2], [cat, cat]) if orientation == 'h' else ([cat, cat], [val1, val2])
        fig.add_trace(go.Scatter(x=x_line_vals, y=y_line_vals, mode='lines', line=dict(color=line_color, width=line_width), showlegend=False))

    fig.add_trace(go.Scatter(x=x_markers1, y=y_markers1, mode='markers', marker=dict(color=marker_color1, size=marker_size), name=label1, showlegend=showlegend))
    fig.add_trace(go.Scatter(x=x_markers2, y=y_markers2, mode='markers', marker=dict(color=marker_color2, size=marker_size), name=label2, showlegend=showlegend))

    for cat, val1, val2 in zip(categories, values1, values2):
        if orientation == 'h':
            # Determine which value is smaller/larger for correct label placement
            if val1 < val2:
                xanchor1, xshift1 = 'right', -5
                xanchor2, xshift2 = 'left', 5
            else:  # val1 >= val2
                xanchor1, xshift1 = 'left', 5
                xanchor2, xshift2 = 'right', -5

            fig.add_annotation(x=val1, y=cat, text=str(val1), showarrow=False, font=dict(color=marker_color1), xanchor=xanchor1, yanchor='middle', xshift=xshift1)
            fig.add_annotation(x=val2, y=cat, text=str(val2), showarrow=False, font=dict(color=marker_color2), xanchor=xanchor2, yanchor='middle', xshift=xshift2)
        else:
            # Determine which value is smaller/larger for correct label placement
            if val1 < val2:
                yanchor1, yshift1 = 'top', -5
                yanchor2, yshift2 = 'bottom', 5
            else:  # val1 >= val2
                yanchor1, yshift1 = 'bottom', 5
                yanchor2, yshift2 = 'top', -5

            fig.add_annotation(x=cat, y=val1, text=str(val1), showarrow=False, font=dict(color=marker_color1), yanchor=yanchor1, xanchor='center', yshift=yshift1)
            fig.add_annotation(x=cat, y=val2, text=str(val2), showarrow=False, font=dict(color=marker_color2), yanchor=yanchor2, xanchor='center', yshift=yshift2)

    fig.update_layout(
        title=title,
        xaxis_title="Value" if orientation == 'h' else "Category",
        yaxis_title="Category" if orientation == 'h' else "Value",
        #template="plotly_white", # Default template
        **kwargs
    )

    return fig


def line_range(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values1_col: Optional[str] = None,
    values2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Range Chart",
    orientation: str = 'h',
    line_color: str = 'blue', # Color of the range line.
    line_width: int = 10, # Width of the range line.
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    
    """
    Draws a range chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        categories_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        values1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        values2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        line_color (str, optional): Color of the range line. Defaults to 'blue'.
        line_width (int, optional): Width of the range line. Defaults to 10.
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.

    Returns:
        go.Figure: The resulting range chart.
    """
    marker_color1 = line_color # Both markers use the same color for a range chart
    marker_color2 = line_color
    marker_size = line_width
    label1 = ""
    label2 = ""
    return dumbbell(df=df, categories_col=categories_col, values1_col=values1_col, values2_col=values2_col, categories=categories, values1=values1, values2=values2, label1=label1, label2=label2, title=title, orientation=orientation, marker_color1=marker_color1, marker_color2=marker_color2, line_color=line_color, marker_size=marker_size, line_width=line_width, **kwargs)

def lollipop_chart(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values: Optional[List[float]] = None,
    title: str = "Lollipop Chart",
    stick_color: str = 'gray',
    marker_color: str = 'blue',
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    """
    Draws a lollipop chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        categories_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        values_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values (List[float], optional): List of numerical values. Ignored if df is provided.
        title (str, optional): Chart title.
        stick_color (str, optional): Color for the lollipop sticks. Defaults to 'gray'.
        marker_color (str, optional): Color for the lollipop markers. Defaults to 'blue'.
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.

    Returns:
        go.Figure: The resulting lollipop chart.
    """
    categories, values = _prepare_chart_data(
        df=df,
        data_map=[
            ('categories', categories_col, categories),
            ('values', values_col, values)
        ]
    )

    if len(categories) != len(values):
        raise ValueError("Length of categories and values must match.")

    fig = go.Figure()

    # Add vertical lines (sticks of the lollipops)
    for i, (x, y) in enumerate(zip(categories, values)):
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[0, y],
            mode='lines',
            line=dict(color=stick_color, width=2),
            showlegend=False
        ))

    # Add markers (lollipop heads)
    fig.add_trace(go.Scatter(
        x=categories,
        y=values,
        mode='markers',
        marker=dict(color=marker_color, size=10),
        name='Value'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Category",
        yaxis_title="Value",
        #template="plotly_white",
        showlegend=False,
        **kwargs
    )

    return fig

def metric(title, value, delta=None, suffix="", prefix="", delta_suffix="", delta_prefix="",
           number_font_size=36, delta_font_size=24, title_font_size=36, 
           number_font_color="Blue", title_font_color="Black",
           paper_color="white", align="center", 
           margin=dict(l=5, r=5, t=30, b=0), width=300, height=200, **kwargs):
    """
    A function to mimic Streamlit's st.metric using Plotly.
    
    Parameters:
        title (str): Label or title of the metric.
        value (float | str): Main metric value.
        delta (float | str): Optional delta/change value.
        suffix (str): Optional suffix for the main value.
        prefix (str): Optional prefix for the main value.
        delta_suffix (str): Optional suffix for the delta.
        delta_prefix (str): Optional prefix for the delta.
        number_font_size (int): Optional font size for the main value.
        delta_font_size (int): Optional font size for the delta.
        title_font_size (int): Optional font size for the title.
        number_font_color (str): Optional color for the main value.
        title_font_color (str): Optional color for the title.
        paper_color (str): Optional background color for the chart.
        width (int): Optional width of the chart 
        - to set the width in Streamlit use , 'use_container_width=False' when plotting
        height (int): Optional height of the chart.
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.
        
    Returns:
        go.Figure: A Plotly figure representing the metric.
    """
    fig = go.Figure(go.Indicator(
        mode = "number+delta" if delta is not None else "number",
        value = float(value) if isinstance(value, (int, float)) else 0,
        align=align,
        number = {
            "valueformat": ",",
            "suffix": suffix,
            "prefix": prefix,
            "font": {"size": number_font_size, "color": number_font_color}
        },
        delta = {
            "reference": 0,
            "valueformat": ".2f",
            "relative": False,
            "suffix": delta_suffix,
            "prefix": delta_prefix,
            "font": {"size": delta_font_size}
        } if delta is not None else None,
        title = {"text": title, "font_size": title_font_size, "font_color": title_font_color, "align":align},
        domain = {"x": [0, 1], "y": [0, 1]}
    ))

    if delta is not None:
        fig['data'][0]['delta']['reference'] = float(value) - float(delta)
    
    fig.update_layout(
        margin=margin,
        height=height,
        width=width,
        paper_bgcolor = paper_color,
        **kwargs)

    return fig

def slope_chart(
    df: Optional[pd.DataFrame] = None,
    categories_col: Optional[str] = None,
    values_cols: Optional[List[str]] = None,
    x_values: Optional[List] = None,
    y_values_list: Optional[List[List[float]]] = None,
    line_names: Optional[List[str]] = None,
    title: str = "Slope Chart",
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    colors: Optional[List[str]] = None,
    text_format: str = "{:.1f}",
    show_legend: bool = False,
    template: str = 'plotly_white',
    **kwargs # Additional keyword arguments to pass to `fig.update_layout()`.
) -> go.Figure:
    """
    Creates a generic slope chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame containing the data. Must have at least two rows.
        categories_col (str, optional): The name of the column to be used for the x-axis (e.g., 'year').
        values_cols (List[str], optional): A list of column names to be plotted on the y-axis.
        x_values (List, optional): A list of values for the x-axis. Ignored if df is provided.
        y_values_list (List[List[float]], optional): A list of lists of y-values. Ignored if df is provided.
        line_names (List[str], optional): A list of names for the y-columns/lines. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to "Slope Chart".
        x_title (Optional[str], optional): The title for the x-axis. Defaults to categories_col name.
        y_title (Optional[str], optional): The title for the y-axis. Defaults to None (hidden).
        colors (Optional[List[str]], optional): A list of colors for the lines.
                                                If None, Plotly's default colors are used.
        text_format (str, optional): A format string for the data point labels. Defaults to "{:.1f}".
        show_legend (bool, optional): Whether to display the legend. Defaults to False.
        template (str, optional): The Plotly template to use. Defaults to 'plotly_white'.
        **kwargs: Additional keyword arguments to pass to `fig.update_layout()`.

    Returns:
        go.Figure: A Plotly figure object.
    """

    if df is not None:
        if categories_col and categories_col not in df.columns:
            raise ValueError(f"Column '{categories_col}' not found in DataFrame.")
        if values_cols and not all(col in df.columns for col in values_cols):
            raise ValueError("One or more columns in values_cols not found in DataFrame.")
        
        x_values = df[categories_col].tolist()
        y_values_list = [df[col].tolist() for col in values_cols]
        line_names = values_cols
    elif not (x_values and y_values_list and line_names):
        raise ValueError("Provide either a DataFrame or all three lists: x_values, y_values_list, and line_names.")

    fig = go.Figure()

    if colors is None:
        # Use plotly's default color cycle if no colors are provided
        colors = fig.layout['template']['layout']['colorway']

    color_map = {line_name: colors[i % len(colors)] for i, line_name in enumerate(line_names)}

    x_start = x_values[0]
    x_end = x_values[-1]

    for i, line_name in enumerate(line_names):
        y_values = y_values_list[i]
        y_start = y_values[0]
        y_end = y_values[-1]
        color = color_map[line_name]

        # Add the slope line
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name=line_name,
            line=dict(color=color),
            marker=dict(color=color, size=8)
        ))

        # Add annotations
        # Left side: Category name and value
        fig.add_annotation(
            x=x_start, y=y_start,
            text=f"<b>{line_name}</b><br>{text_format.format(y_start)}",
            showarrow=False,
            xanchor='right',
            align='right',
            xshift=-8
        )
        # Right side: Value
        fig.add_annotation(
            x=x_end, y=y_end,
            text=text_format.format(y_end),
            showarrow=False,
            xanchor='left',
            xshift=8
        )

    # Update layout for a clean slope chart appearance
    fig.update_layout(
        title_text=title,
        xaxis_title=x_title if x_title else (categories_col.capitalize() if categories_col else ""),
        yaxis_title=y_title,
        showlegend=show_legend,
        template=template,
        yaxis=dict(visible=False),
        xaxis=dict(tickmode='array', tickvals=x_values, showgrid=False, zeroline=False), # Added comma
        **kwargs
    )
    return fig
