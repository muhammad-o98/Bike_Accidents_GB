# app.py - Industry-Grade Bicycle Accidents Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any

# Import local modules
from src.dashboard_utils import (
    filter_dataframe, calculate_kpis, group_rare_categories,
    prepare_time_series_data, prepare_stacked_bar_data,
    prepare_severity_analysis, format_large_numbers,
    get_unique_values_for_filters, calculate_accident_rates,
    extract_hour_from_time, prepare_severity_speed_heatmap,
    prepare_temporal_analysis, prepare_demographic_severity_analysis,
    calculate_correlation_matrix, prepare_severity_trends_data,
    prepare_environmental_analysis, create_sankey_data
)

# Page configuration
st.set_page_config(
    page_title="GB Bicycle Accidents Dashboard",
    page_icon="🚴‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #262730;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #64748b;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #262730;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the preprocessed data from Parquet file."""
    parquet_path = "processed/bicycle_accidents.parquet"
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    else:
        st.error(f"Processed data file not found at {parquet_path}. Please run main.py first to process the data.")
        st.stop()

def display_kpis(kpis: Dict[str, Any]):
    """Display KPIs in a formatted grid."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['total_accidents'])}</div>
                <div class="kpi-label">Total Accidents</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['total_casualties'])}</div>
                <div class="kpi-label">Total Casualties</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['total_vehicles'])}</div>
                <div class="kpi-label">Vehicles Involved</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{kpis['avg_casualties_per_accident']:.2f}</div>
                <div class="kpi-label">Avg Casualties/Accident</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Additional KPIs row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['fatal_accidents'])}</div>
                <div class="kpi-label">Fatal Accidents</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['serious_accidents'])}</div>
                <div class="kpi-label">Serious Accidents</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col7:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_large_numbers(kpis['slight_accidents'])}</div>
                <div class="kpi-label">Slight Accidents</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col8:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-value">{kpis['year_range']}</div>
                <div class="kpi-label">Year Range</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

def create_sidebar_filters(df: pd.DataFrame, unique_values: Dict):
    """Create sidebar filters for the dashboard."""
    st.sidebar.header("` Data Filters")
    
    # Year range filter
    if 'year' in df.columns:
        min_year, max_year = int(df['year'].min()), int(df['year'].max())
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1
        )
    else:
        year_range = None
    
    # Severity filter
    severity_options = unique_values.get('severity', [])
    severity_filter = st.sidebar.multiselect(
        "Accident Severity",
        options=severity_options,
        default=severity_options
    )
    
    # Gender filter
    gender_options = unique_values.get('gender', [])
    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=gender_options,
        default=gender_options
    )
    
    # Age group filter
    age_options = unique_values.get('age_grp', [])
    age_filter = st.sidebar.multiselect(
        "Age Group",
        options=age_options,
        default=age_options
    )
    
    # Road conditions filter
    road_cond_options = unique_values.get('road_conditions', [])
    road_cond_filter = st.sidebar.multiselect(
        "Road Conditions",
        options=road_cond_options,
        default=road_cond_options
    )
    
    # Weather conditions filter
    weather_options = unique_values.get('weather_conditions', [])
    weather_filter = st.sidebar.multiselect(
        "Weather Conditions",
        options=weather_options,
        default=weather_options
    )
    
    # Light conditions filter
    light_options = unique_values.get('light_conditions', [])
    light_filter = st.sidebar.multiselect(
        "Light Conditions",
        options=light_options,
        default=light_options
    )
    
    return {
        'year_range': year_range,
        'severity': severity_filter,
        'gender': gender_filter,
        'age_groups': age_filter,
        'road_conditions': road_cond_filter,
        'weather_conditions': weather_filter,
        'light_conditions': light_filter
    }

def create_time_series_chart(df: pd.DataFrame):
    """Create interactive time series chart."""
    st.markdown('<div class="section-header"> Accidents Over Time</div>', unsafe_allow_html=True)
    
    # Time series by year
    yearly_data = prepare_time_series_data(df, 'year')
    
    fig = px.line(
        yearly_data, 
        x='year', 
        y='count',
        title="Bicycle Accidents by Year",
        labels={'count': 'Number of Accidents', 'year': 'Year'},
        markers=True
    )
    fig.update_layout(height=400, showlegend=False)
    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    
    st.plotly_chart(fig, width="stretch")

def create_severity_charts(df: pd.DataFrame):
    """Create severity analysis charts."""
    st.markdown('<div class="section-header"> Severity Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Severity distribution
        if 'severity' in df.columns:
            severity_counts = df['severity'].value_counts()
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title="Accident Severity Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        # Severity by weather conditions
        if 'severity' in df.columns and 'weather_conditions' in df.columns:
            # Group rare weather conditions
            df_temp = df.copy()
            df_temp['weather_conditions'] = group_rare_categories(df_temp['weather_conditions'], min_count=50)
            
            severity_weather = prepare_severity_analysis(df_temp, 'weather_conditions')
            if not severity_weather.empty:
                fig = px.bar(
                    severity_weather.reset_index(),
                    x='weather_conditions',
                    y=['Slight', 'Serious', 'Fatal'],
                    title="Accident Severity by Weather Conditions (%)",
                    labels={'value': 'Percentage', 'weather_conditions': 'Weather Conditions'},
                    barmode='stack'
                )
                fig.update_layout(height=400, xaxis_tickangle=45)
                st.plotly_chart(fig, width="stretch")

def create_demographic_charts(df: pd.DataFrame):
    """Create demographic analysis charts."""
    st.markdown('<div class="section-header">👥 Demographics Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        if 'gender' in df.columns:
            gender_counts = calculate_accident_rates(df, 'gender')
            fig = px.bar(
                gender_counts,
                x='gender',
                y='count',
                title="Accidents by Gender",
                text='percentage',
                labels={'count': 'Number of Accidents', 'gender': 'Gender'}
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        # Age group distribution
        if 'age_grp' in df.columns:
            age_counts = calculate_accident_rates(df, 'age_grp')
            fig = px.bar(
                age_counts,
                x='age_grp',
                y='count',
                title="Accidents by Age Group",
                text='percentage',
                labels={'count': 'Number of Accidents', 'age_grp': 'Age Group'}
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=45)
            st.plotly_chart(fig, width="stretch")

def create_conditions_analysis(df: pd.DataFrame):
    """Create road and environmental conditions analysis."""
    st.markdown('<div class="section-header"> Road & Environmental Conditions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Road conditions
        if 'road_conditions' in df.columns:
            df_temp = df.copy()
            df_temp['road_conditions'] = group_rare_categories(df_temp['road_conditions'], min_count=50)
            road_counts = calculate_accident_rates(df_temp, 'road_conditions')
            
            fig = px.bar(
                road_counts,
                x='road_conditions',
                y='count',
                title="Accidents by Road Conditions",
                text='percentage',
                labels={'count': 'Number of Accidents', 'road_conditions': 'Road Conditions'}
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=45)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        # Light conditions
        if 'light_conditions' in df.columns:
            df_temp = df.copy()
            df_temp['light_conditions'] = group_rare_categories(df_temp['light_conditions'], min_count=50)
            light_counts = calculate_accident_rates(df_temp, 'light_conditions')
            
            fig = px.bar(
                light_counts,
                x='light_conditions',
                y='count',
                title="Accidents by Light Conditions",
                text='percentage',
                labels={'count': 'Number of Accidents', 'light_conditions': 'Light Conditions'}
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=45)
            st.plotly_chart(fig, width="stretch")

def create_temporal_analysis(df: pd.DataFrame):
    """Create temporal patterns analysis."""
    st.markdown('<div class="section-header"> Temporal Patterns</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week analysis
        if 'day_of_week' in df.columns:
            dow_data = prepare_time_series_data(df, 'day_of_week')
            fig = px.bar(
                dow_data,
                x='day_of_week',
                y='count',
                title="Accidents by Day of Week",
                labels={'count': 'Number of Accidents', 'day_of_week': 'Day of Week'}
            )
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=45)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        # Monthly patterns
        if 'month' in df.columns:
            month_counts = df['month'].value_counts().sort_index()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            fig = px.line(
                x=month_names,
                y=[month_counts.get(i, 0) for i in range(1, 13)],
                title="Accidents by Month",
                labels={'x': 'Month', 'y': 'Number of Accidents'},
                markers=True
            )
            fig.update_layout(height=400, showlegend=False)
            fig.update_traces(line=dict(width=3), marker=dict(size=6))
            st.plotly_chart(fig, width="stretch")

def create_data_explorer(df: pd.DataFrame):
    """Create interactive data explorer section."""
    st.markdown('<div class="section-header">📊 Data Explorer</div>', unsafe_allow_html=True)
    
    # Data summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dataset Summary:**")
        st.write(f"- Total Records: {len(df):,}")
        st.write(f"- Date Range: {df['year'].min()} - {df['year'].max()}")
        st.write(f"- Unique Accidents: {df['accident_index'].nunique():,}" if 'accident_index' in df.columns else "")
        st.write(f"- Missing Data: {df.isnull().sum().sum():,} values")
    
    with col2:
        st.write("**Top Categories:**")
        if 'road_type' in df.columns:
            top_road_types = df['road_type'].value_counts().head(3)
            for road_type, count in top_road_types.items():
                st.write(f"- {road_type}: {count:,} accidents")
    
    # Raw data viewer
    st.subheader("📋 Raw Data Viewer")
    
    # Select columns to display
    available_columns = df.columns.tolist()
    display_columns = st.multiselect(
        "Select columns to display:",
        options=available_columns,
        default=available_columns[:10]  # Default to first 10 columns
    )
    
    if display_columns:
        # Pagination
        rows_per_page = st.select_slider("Rows per page:", [10, 25, 50, 100], value=25)
        
        total_rows = len(df)
        total_pages = (total_rows - 1) // rows_per_page + 1
        
        page = st.number_input(
            f"Page (1 to {total_pages}):",
            min_value=1,
            max_value=total_pages,
            value=1
        )
        
        start_idx = (page - 1) * rows_per_page
        end_idx = min(start_idx + rows_per_page, total_rows)
        
        st.dataframe(
            df[display_columns].iloc[start_idx:end_idx],
            width="stretch",
            hide_index=True
        )
        
        st.write(f"Showing rows {start_idx + 1} to {end_idx} of {total_rows}")
        
        # Download filtered data
        if st.button("Download Filtered Data as CSV"):
            csv = df[display_columns].to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="filtered_bicycle_accidents.csv",
                mime="text/csv"
            )

def create_advanced_severity_analysis(df: pd.DataFrame):
    """Create advanced severity analysis visualizations."""
    st.markdown('<div class="section-header">Advanced Severity Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Severity vs Speed Limit Distribution")
        st.markdown("**Analysis:** Shows how accident severity varies with speed limits. Higher speeds generally correlate with more severe accidents.")
        
        heatmap_data = prepare_severity_speed_heatmap(df)
        if not heatmap_data.empty:
            fig = px.imshow(
                heatmap_data.values,
                labels=dict(x="Severity", y="Speed Limit (mph)", color="Percentage"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                title="Accident Severity by Speed Limit (%)",
                color_continuous_scale="Reds"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Insufficient data for speed limit vs severity analysis")
    
    with col2:
        st.subheader("Severity Trends Over Time")
        st.markdown("**Analysis:** Tracks how the distribution of accident severities has changed over the decades, indicating improvements in road safety.")
        
        severity_trends = prepare_severity_trends_data(df)
        if not severity_trends.empty:
            fig = px.area(
                severity_trends,
                x='year',
                y=['Slight', 'Serious', 'Fatal'],
                title="Accident Severity Trends by Year",
                labels={'value': 'Number of Accidents', 'year': 'Year'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Insufficient data for severity trends analysis")

def create_environmental_conditions_analysis(df: pd.DataFrame):
    """Create environmental conditions analysis."""
    st.markdown('<div class="section-header">Environmental Conditions Analysis</div>', unsafe_allow_html=True)
    
    env_data = prepare_environmental_analysis(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weather Conditions vs Severity")
        st.markdown("**Analysis:** Reveals which weather conditions lead to more severe accidents. Poor weather often increases accident severity.")
        
        if 'weather_severity' in env_data:
            weather_data = env_data['weather_severity']
            fig = px.bar(
                weather_data.reset_index(),
                x='weather_conditions',
                y=['Slight', 'Serious', 'Fatal'],
                title="Accident Severity by Weather Conditions (%)",
                labels={'value': 'Percentage', 'weather_conditions': 'Weather Conditions'},
                barmode='stack'
            )
            fig.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Weather vs severity data not available")
    
    with col2:
        st.subheader("Light Conditions vs Severity")
        st.markdown("**Analysis:** Compares accident severity between different lighting conditions. Darkness often increases severity risk.")
        
        if 'light_severity' in env_data:
            light_data = env_data['light_severity']
            fig = px.imshow(
                light_data.values,
                labels=dict(x="Severity", y="Light Conditions", color="Percentage"),
                x=light_data.columns,
                y=light_data.index,
                title="Accident Severity by Light Conditions (%)",
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Light conditions vs severity data not available")
    
    # Road Type vs Severity
    st.subheader("Road Type Impact on Severity")
    st.markdown("**Analysis:** Different road types have varying risk profiles. Motorways and major roads often have different severity patterns than local roads.")
    
    if 'road_type_severity' in env_data:
        road_data = env_data['road_type_severity']
        fig = px.bar(
            road_data.reset_index(),
            x='road_type',
            y=['Slight', 'Serious', 'Fatal'],
            title="Accident Count by Road Type and Severity",
            labels={'value': 'Number of Accidents', 'road_type': 'Road Type'},
            barmode='group'
        )
        fig.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Road type vs severity data not available")

def create_temporal_patterns_analysis(df: pd.DataFrame):
    """Create temporal patterns analysis."""
    st.markdown('<div class="section-header">Temporal Patterns Analysis</div>', unsafe_allow_html=True)
    
    temporal_data = prepare_temporal_analysis(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hourly Accident Distribution")
        st.markdown("**Analysis:** Shows peak accident hours throughout the day. Rush hours typically show higher accident rates.")
        
        if 'hourly' in temporal_data:
            hourly_data = temporal_data['hourly']
            
            # Create polar chart for hourly distribution
            fig = px.line_polar(
                hourly_data,
                r='count',
                theta='hour',
                line_close=True,
                title="24-Hour Accident Distribution"
            )
            fig.update_traces(fill='toself')
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Hourly distribution data not available")
    
    with col2:
        st.subheader("Weekday vs Weekend Severity")
        st.markdown("**Analysis:** Compares accident severity patterns between weekdays and weekends. Different activity patterns can affect severity.")
        
        if 'weekend_vs_weekday' in temporal_data:
            weekend_data = temporal_data['weekend_vs_weekday'].reset_index()
            fig = px.bar(
                weekend_data,
                x='day_type',
                y=['Slight', 'Serious', 'Fatal'],
                title="Accident Severity: Weekday vs Weekend (%)",
                labels={'value': 'Percentage', 'day_type': 'Day Type'},
                barmode='group'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Weekday vs weekend data not available")
    
    # Monthly trends with rolling average
    st.subheader("Seasonal Patterns with Rolling Averages")
    st.markdown("**Analysis:** Shows monthly accident counts with 3-month rolling averages to identify seasonal trends and long-term patterns.")
    
    if 'monthly_trends' in temporal_data:
        monthly_data = temporal_data['monthly_trends']
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_data['month'],
            y=monthly_data['count'],
            mode='lines',
            name='Monthly Accidents',
            line=dict(width=1, color='lightblue'),
            opacity=0.6
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_data['month'],
            y=monthly_data['rolling_avg'],
            mode='lines',
            name='3-Month Rolling Average',
            line=dict(width=3, color='darkblue')
        ))
        
        fig.update_layout(
            title="Monthly Accident Trends with Rolling Average",
            xaxis_title="Month",
            yaxis_title="Number of Accidents",
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Monthly trends data not available")

def create_demographics_analysis(df: pd.DataFrame):
    """Create demographics analysis."""
    st.markdown('<div class="section-header">Demographics Analysis</div>', unsafe_allow_html=True)
    
    demo_data = prepare_demographic_severity_analysis(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Age Group vs Severity Risk")
        st.markdown("**Analysis:** Heat map showing severity risk by age group. Young and elderly cyclists may show different risk patterns.")
        
        if 'age_severity_heatmap' in demo_data:
            age_data = demo_data['age_severity_heatmap']
            fig = px.imshow(
                age_data.values,
                labels=dict(x="Severity", y="Age Group", color="Percentage"),
                x=age_data.columns,
                y=age_data.index,
                title="Accident Severity by Age Group (%)",
                color_continuous_scale="Oranges"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Age vs severity data not available")
    
    with col2:
        st.subheader("Gender vs Road Conditions")
        st.markdown("**Analysis:** Shows how different genders experience accidents across various road conditions.")
        
        if 'gender_road_conditions' in demo_data:
            gender_data = demo_data['gender_road_conditions']
            fig = px.bar(
                gender_data.reset_index(),
                x='gender',
                y=gender_data.columns,
                title="Road Conditions by Gender (%)",
                labels={'value': 'Percentage', 'gender': 'Gender'},
                barmode='group'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Gender vs road conditions data not available")
    
    # Age and Gender time patterns
    st.subheader("Time Patterns by Gender")
    st.markdown("**Analysis:** Shows how accident timing varies by gender, revealing different travel patterns and risk exposure.")
    
    if 'age_gender_time' in demo_data:
        time_data = demo_data['age_gender_time']
        fig = px.line(
            time_data,
            x='hour',
            y='count',
            color='gender',
            title="Accident Timing by Gender",
            labels={'count': 'Number of Accidents', 'hour': 'Hour of Day'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Time patterns by gender data not available")

def create_multidimensional_analysis(df: pd.DataFrame):
    """Create multi-dimensional analysis."""
    st.markdown('<div class="section-header">Multi-Dimensional Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Correlation Matrix")
        st.markdown("**Analysis:** Shows relationships between numerical variables. Strong correlations can indicate important risk factors.")
        
        corr_data = calculate_correlation_matrix(df)
        if not corr_data.empty:
            fig = px.imshow(
                corr_data.values,
                labels=dict(x="Variables", y="Variables", color="Correlation"),
                x=corr_data.columns,
                y=corr_data.index,
                title="Correlation Matrix of Key Variables",
                color_continuous_scale="RdBu",
                range_color=[-1, 1]
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Correlation matrix data not available")
    
    with col2:
        st.subheader("Accident Flow Analysis")
        st.markdown("**Analysis:** Sankey diagram showing the flow from road types through weather conditions to accident severity.")
        
        sankey_data = create_sankey_data(df)
        if sankey_data and len(sankey_data.get('nodes', [])) > 0:
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=sankey_data['nodes'],
                    color="blue"
                ),
                link=dict(
                    source=sankey_data['sources'],
                    target=sankey_data['targets'],
                    value=sankey_data['values']
                )
            )])
            
            fig.update_layout(
                title_text="Accident Flow: Road Type → Weather → Severity",
                font_size=10,
                height=400
            )
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Insufficient data for accident flow analysis")
    
    # Risk Factor Analysis
    st.subheader("Risk Factor Analysis")
    st.markdown("**Analysis:** Comprehensive view of how multiple factors combine to influence accident severity.")
    
    # Create a risk score analysis
    if all(col in df.columns for col in ['speed_limit', 'severity_numeric', 'number_of_casualties']):
        df_risk = df.copy()
        df_risk = df_risk.dropna(subset=['speed_limit'])
        
        # Create risk categories
        speed_bins = [0, 30, 50, 70, 100]
        speed_labels = ['Low Speed (≤30)', 'Medium Speed (31-50)', 'High Speed (51-70)', 'Very High Speed (>70)']
        
        try:
            df_risk['speed_category'] = pd.cut(df_risk['speed_limit'], bins=speed_bins, labels=speed_labels, include_lowest=True)
            
            risk_analysis = df_risk.groupby('speed_category').agg({
                'severity_numeric': 'mean',
                'number_of_casualties': 'mean',
                'accident_index': 'count'
            }).round(2)
            
            risk_analysis.columns = ['Avg Severity Score', 'Avg Casualties', 'Total Accidents']
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(
                    x=risk_analysis.index,
                    y=risk_analysis['Total Accidents'],
                    name="Total Accidents",
                    marker_color='lightblue'
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=risk_analysis.index,
                    y=risk_analysis['Avg Severity Score'],
                    mode='lines+markers',
                    name="Avg Severity Score",
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=True
            )
            
            fig.update_xaxes(title_text="Speed Category")
            fig.update_yaxes(title_text="Number of Accidents", secondary_y=False)
            fig.update_yaxes(title_text="Average Severity Score", secondary_y=True)
            fig.update_layout(title_text="Risk Analysis by Speed Category", height=400)
            
            st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.info("Risk factor analysis not available due to data limitations")

def main():
    """Main dashboard application."""
    # Title and description
    st.markdown('<div class="main-header">🚴‍♂️ Great Britain Bicycle Accidents Dashboard (1979-2018)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This dashboard provides an interactive analysis of bicycle accidents in Great Britain from 1979 to 2018. 
    Use the filters in the sidebar to explore different aspects of the data and identify patterns in accident occurrence, 
    severity, and contributing factors.
    """)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    # Get unique values for filters
    unique_values = get_unique_values_for_filters(df)
    
    # Create sidebar filters
    filters = create_sidebar_filters(df, unique_values)
    
    # Apply filters to data
    filtered_df = filter_dataframe(df, **filters)
    
    # Check if filtered data is empty
    if len(filtered_df) == 0:
        st.warning("No data matches the current filters. Please adjust your selections.")
        return
    
    # Calculate and display KPIs
    kpis = calculate_kpis(filtered_df)
    display_kpis(kpis)
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Time Trends", 
        "Severity", 
        "Demographics", 
        "Conditions", 
        "Advanced Analysis",
        "Data Explorer"
    ])
    
    with tab1:
        create_time_series_chart(filtered_df)
        create_temporal_analysis(filtered_df)
    
    with tab2:
        create_severity_charts(filtered_df)
    
    with tab3:
        create_demographic_charts(filtered_df)
    
    with tab4:
        create_conditions_analysis(filtered_df)
    
    with tab5:
        # Advanced Analysis Tab
        create_advanced_severity_analysis(filtered_df)
        create_environmental_conditions_analysis(filtered_df)
        create_temporal_patterns_analysis(filtered_df)
        create_demographics_analysis(filtered_df)
        create_multidimensional_analysis(filtered_df)
    
    with tab6:
        create_data_explorer(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source:** [Great Britain Bicycle Accidents Dataset (1979–2018)](https://www.kaggle.com/datasets/johnharshith/bicycle-accidents-in-great-britain-1979-to-2018?resource=download&select=Accidents.csv)  
    **Tech Stack:** Streamlit, Plotly, Pandas
""")

if __name__ == "__main__":
    main()
