import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="​🇩​​🇦​​🇹​​🇦​ ​🇸​​🇨​​🇮​​🇪​​🇳​​🇨​​🇪​ ​🇪​​🇩​​🇦​ ​🇦​​🇵​​🇵​",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            color: #1f77b4;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .section-header {
            color: #ff7f0e;
            font-size: 1.5em;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #ff7f0e;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>📊 🇩​​🇦​​🇹​​🇦​ ​🇸​​🇨​​🇮​​🇪​​🇳​​🇨​​🇪​ ​🇪​​🇩​​🇦​ ​🇦​​🇵​​🇵</div>", unsafe_allow_html=True)

# Sidebar - File Upload
st.sidebar.markdown("### 📁 Upload Data")
uploaded_file = st. sidebar.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: CSV, XLSX, XLS"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state. df = None

if uploaded_file is not None:
    # Read file based on type
    try:
        if uploaded_file. name.endswith('.csv'):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {e}")
        st.session_state.df = None

# Main App Logic
if st.session_state. df is None:
    st.info("👈 ​🇵​​🇱​​🇪​​🇦​​🇸​​🇪​ ​🇺​​🇵​​🇱​​🇴​​🇦​​🇩​ ​🇦​ ​🇨​​🇸​​🇻​ ​🇴​​🇷​ ​🇪​​🇽​​🇨​​🇪​​🇱​ ​🇫​​🇮​​🇱​​🇪​ ​🇹​​🇴​ ​🇬​​🇪​​🇹​ ​🇸​​🇹​​🇦​​🇷​​🇹​​🇪​​🇩​❗")
else:
    df = st.session_state.df
    
    # Create Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Basic EDA", "📊 Visualizations", "🔍 Advanced Queries", "📥 Data Export"]
    )
    
    # ======================== TAB 1: BASIC EDA ========================
    with tab1:
        st.markdown("<div class='section-header'>Basic Exploratory Data Analysis</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Rows", len(df))
        with col2:
            st.metric("📋 Total Columns", len(df.columns))
        with col3:
            st.metric("🔴 Duplicate Records", df.duplicated().sum())
        with col4:
            st. metric("⚠️ Missing Values", df.isnull().sum().sum())
        
        # Data Preview
        st.markdown("#### 👀 Data Preview")
        preview_rows = st.slider("Select number of rows to preview", 1, len(df), 5)
        st.dataframe(df.head(preview_rows), use_container_width=True)
        
        # Data Info
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("#### 📋 Dataset Info")
            info_data = {
                "Column": df.columns,
                "Data Type": df.dtypes,
                "Non-Null Count": df.count(),
                "Null Count": df.isnull().sum()
            }
            st.dataframe(
                pd.DataFrame(info_data),
                use_container_width=True,
                hide_index=True
            )
        
        with col_info2:
            st. markdown("#### 🔍 Missing Values Details")
            missing_df = pd.DataFrame({
                "Column": df.columns,
                "Missing Count": df.isnull().sum(),
                "Missing %": (df.isnull(). sum() / len(df) * 100).round(2)
            })
            missing_df = missing_df[missing_df["Missing Count"] > 0]
            
            if len(missing_df) > 0:
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No missing values found!")
        
        # Statistical Description
        st.markdown("#### 📊 Statistical Description")
        st.dataframe(df.describe(). T, use_container_width=True)
        
        # Duplicate Records
        st.markdown("#### 🔴 Duplicate Records Analysis")
        col_dup1, col_dup2 = st.columns(2)
        
        with col_dup1:
            total_duplicates = df.duplicated().sum()
            st.metric("Total Duplicates", total_duplicates)
        
        with col_dup2:
            if total_duplicates > 0:
                col_dup_option = st.selectbox(
                    "View duplicate records based on:",
                    ["All Columns"] + list(df.columns)
                )
                
                if col_dup_option == "All Columns":
                    duplicates = df[df.duplicated(keep=False)].sort_index()
                else:
                    duplicates = df[df.duplicated(subset=[col_dup_option], keep=False)].sort_values(col_dup_option)
                
                st.dataframe(duplicates, use_container_width=True)
    
    # ======================== TAB 2: VISUALIZATIONS ========================
    with tab2:
        st.markdown("<div class='section-header'>Data Visualizations</div>", unsafe_allow_html=True)
        
        # Column Selection
        st.markdown("#### 📌 Select Columns for Visualization")
        selected_columns = st.multiselect(
            "Choose columns to visualize",
            df.columns. tolist(),
            default=df.columns.tolist()[:3] if len(df.columns) >= 3 else df.columns.tolist(),
            help="Select multiple columns for analysis"
        )
        
        if selected_columns:
            df_selected = df[selected_columns]
            
            # Visualization Type Selection
            viz_col1, viz_col2, viz_col3 = st.columns(3)
            
            with viz_col1:
                st.markdown("#### 📊 Visualization Types")
                viz_type = st.radio(
                    "Select visualization type",
                    ["Distributions", "Correlations", "Categorical", "Box Plots", "Pair Plots"],
                    label_visibility="collapsed"
                )
            
            # Distribution Plots
            if viz_type == "Distributions":
                st.markdown("#### 📈 Distribution Analysis")
                
                numeric_cols = df_selected.select_dtypes(include=[np.number]). columns. tolist()
                
                if numeric_cols:
                    col_to_plot = st.selectbox("Select numeric column", numeric_cols)
                    
                    col_hist, col_kde = st.columns(2)
                    
                    with col_hist:
                        fig, ax = plt.subplots(figsize=(8, 5))
                        sns.histplot(df[col_to_plot]. dropna(), kde=True, bins=30, ax=ax, color='skyblue')
                        ax. set_title(f"Distribution of {col_to_plot}", fontsize=14, fontweight='bold')
                        ax.set_xlabel(col_to_plot)
                        ax.set_ylabel("Frequency")
                        st.pyplot(fig)
                    
                    with col_kde:
                        fig, ax = plt.subplots(figsize=(8, 5))
                        df[col_to_plot].dropna().plot(kind='density', ax=ax, color='coral', linewidth=2)
                        ax.set_title(f"Density Plot of {col_to_plot}", fontsize=14, fontweight='bold')
                        ax.set_xlabel(col_to_plot)
                        st.pyplot(fig)
                else:
                    st.warning("No numeric columns available for distribution plots")
            
            # Correlation Heatmap
            elif viz_type == "Correlations":
                st.markdown("#### 🔗 Correlation Analysis")
                
                numeric_df = df_selected.select_dtypes(include=[np.number])
                
                if len(numeric_df.columns) > 1:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    corr_matrix = numeric_df. corr()
                    sns. heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                               center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
                    ax.set_title("Correlation Heatmap", fontsize=14, fontweight='bold')
                    st.pyplot(fig)
                else:
                    st. warning("Need at least 2 numeric columns for correlation analysis")
            
            # Categorical Plots
            elif viz_type == "Categorical":
                st.markdown("#### 🏷️ Categorical Analysis")
                
                categorical_cols = df_selected.select_dtypes(include=['object']).columns.tolist()
                numeric_cols = df_selected.select_dtypes(include=[np. number]).columns.tolist()
                
                if categorical_cols:
                    col_cat = st.selectbox("Select categorical column", categorical_cols)
                    
                    if numeric_cols:
                        col_num = st.selectbox("Select numeric column (optional)", [None] + numeric_cols)
                        
                        if col_num:
                            fig, ax = plt.subplots(figsize=(10, 6))
                            sns.barplot(data=df, x=col_cat, y=col_num, ax=ax, palette='Set2')
                            ax.set_title(f"{col_num} by {col_cat}", fontsize=14, fontweight='bold')
                            plt.xticks(rotation=45)
                            st.pyplot(fig)
                        else:
                            fig, ax = plt.subplots(figsize=(10, 6))
                            value_counts = df[col_cat].value_counts()
                            sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette='husl')
                            ax.set_title(f"Count of {col_cat}", fontsize=14, fontweight='bold')
                            plt.xticks(rotation=45)
                            st.pyplot(fig)
                    else:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        value_counts = df[col_cat].value_counts()
                        sns.barplot(x=value_counts. index, y=value_counts. values, ax=ax, palette='viridis')
                        ax. set_title(f"Count of {col_cat}", fontsize=14, fontweight='bold')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                else:
                    st.warning("No categorical columns available")
            
            # Box Plots
            elif viz_type == "Box Plots":
                st. markdown("#### 📦 Box Plot Analysis")
                
                numeric_cols = df_selected.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = df_selected.select_dtypes(include=['object']).columns.tolist()
                
                if numeric_cols:
                    col_num = st. selectbox("Select numeric column", numeric_cols)
                    
                    if categorical_cols:
                        col_cat = st.selectbox("Select categorical column (optional)", [None] + categorical_cols)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        if col_cat:
                            sns.boxplot(data=df, x=col_cat, y=col_num, ax=ax, palette='Set2')
                            ax.set_title(f"{col_num} by {col_cat}", fontsize=14, fontweight='bold')
                            plt.xticks(rotation=45)
                        else:
                            sns.boxplot(data=df[col_num], ax=ax, palette='Set2')
                            ax.set_title(f"Box Plot of {col_num}", fontsize=14, fontweight='bold')
                        
                        st.pyplot(fig)
                    else:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.boxplot(data=df[col_num], ax=ax, palette='Set2')
                        ax.set_title(f"Box Plot of {col_num}", fontsize=14, fontweight='bold')
                        st.pyplot(fig)
                else:
                    st.warning("No numeric columns available for box plots")
            
            # Pair Plots
            elif viz_type == "Pair Plots":
                st.markdown("#### 🔀 Pair Plot Analysis")
                
                numeric_cols = df_selected.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    n_cols = st.slider("Select number of columns to include", 2, len(numeric_cols), 2)
                    cols_to_plot = numeric_cols[:n_cols]
                    
                    fig = sns.pairplot(df[cols_to_plot], diag_kind='hist', plot_kws={'alpha': 0.6})
                    st.pyplot(fig)
                else:
                    st.warning("Need at least 2 numeric columns for pair plots")
        else:
            st.info("👈 Please select at least one column to visualize")
    
    # ======================== TAB 3: ADVANCED QUERIES ========================
    with tab3:
        st.markdown("<div class='section-header'>Advanced Data Queries</div>", unsafe_allow_html=True)
        
        query_type = st.radio(
            "Select Query Type",
            ["Top N Categories", "Conditional Filtering", "Aggregation", "Custom Query"],
            horizontal=True
        )
        
        # Top N Categories
        if query_type == "Top N Categories":
            st.markdown("#### 🏆 Top N Categories")
            
            categorical_cols = df. select_dtypes(include=['object']).columns.tolist()
            
            if categorical_cols:
                col_top = st.selectbox("Select categorical column", categorical_cols)
                n = st.slider("Select N (top records)", 1, 20, 5)
                
                top_categories = df[col_top].value_counts().head(n). reset_index()
                top_categories.columns = [col_top, 'Count']
                
                st.markdown(f"#### Top {n} Categories in {col_top}")
                st.dataframe(top_categories, use_container_width=True, hide_index=True)
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=top_categories, x=col_top, y='Count', ax=ax, palette='rocket')
                ax.set_title(f"Top {n} {col_top}", fontsize=14, fontweight='bold')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("No categorical columns available")
        
        # Conditional Filtering
        elif query_type == "Conditional Filtering":
            st.markdown("#### 🔍 Filter Records")
            
            numeric_cols = df.select_dtypes(include=[np.number]). columns.tolist()
            
            if numeric_cols:
                col_filter = st.selectbox("Select numeric column to filter", numeric_cols)
                filter_type = st.selectbox("Select filter condition", ["Greater than (>)", "Less than (<)", 
                                                                       "Equal to (=)", "Greater/Equal (>=)", 
                                                                       "Less/Equal (<=)"])
                filter_value = st.number_input(f"Enter value to compare", value=0.0)
                
                # Apply filter
                if filter_type == "Greater than (>)":
                    filtered_df = df[df[col_filter] > filter_value]
                elif filter_type == "Less than (<)":
                    filtered_df = df[df[col_filter] < filter_value]
                elif filter_type == "Equal to (=)":
                    filtered_df = df[df[col_filter] == filter_value]
                elif filter_type == "Greater/Equal (>=)":
                    filtered_df = df[df[col_filter] >= filter_value]
                else:  # Less/Equal (<=)
                    filtered_df = df[df[col_filter] <= filter_value]
                
                st.markdown(f"#### Results: Found {len(filtered_df)} records")
                st.dataframe(filtered_df, use_container_width=True)
                
                # Statistics
                col_stat1, col_stat2, col_stat3 = st. columns(3)
                with col_stat1:
                    st.metric("Records Found", len(filtered_df))
                with col_stat2:
                    st.metric("Percentage", f"{len(filtered_df)/len(df)*100:.2f}%")
                with col_stat3:
                    st.metric("Excluded", len(df) - len(filtered_df))
            else:
                st.warning("No numeric columns available for filtering")
        
        # Aggregation
        elif query_type == "Aggregation":
            st.markdown("#### 📊 Data Aggregation")
            
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=[np.number]). columns.tolist()
            
            if categorical_cols and numeric_cols:
                col_group = st.selectbox("Group by column", categorical_cols)
                col_agg = st.selectbox("Aggregate column", numeric_cols)
                agg_func = st.selectbox("Aggregation function", ["Sum", "Mean", "Count", "Min", "Max", "Std"])
                
                # Perform aggregation
                agg_dict = {
                    "Sum": "sum",
                    "Mean": "mean",
                    "Count": "count",
                    "Min": "min",
                    "Max": "max",
                    "Std": "std"
                }
                
                result_df = df.groupby(col_group)[col_agg]. agg(agg_dict[agg_func]). reset_index()
                result_df.columns = [col_group, f'{agg_func} of {col_agg}']
                
                st.markdown(f"#### {agg_func} of {col_agg} grouped by {col_group}")
                st.dataframe(result_df, use_container_width=True, hide_index=True)
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=result_df, x=col_group, y=result_df. columns[1], ax=ax, palette='muted')
                ax.set_title(f"{agg_func} of {col_agg} by {col_group}", fontsize=14, fontweight='bold')
                plt.xticks(rotation=45)
                st. pyplot(fig)
            else:
                st.warning("Need both categorical and numeric columns for aggregation")
        
        # Custom Query
        elif query_type == "Custom Query":
            st.markdown("#### 🛠️ Custom Query Builder")
            
            st.info("Use Python pandas syntax to query your data.  Example: `df[(df['Age'] > 25) & (df['City'] == 'New York')]`")
            
            custom_query = st.text_area(
                "Enter your pandas query:",
                value="df[df['column_name'] > value]",
                height=100
            )
            
            try:
                if st.button("Execute Query"):
                    result = eval(custom_query)
                    st.markdown(f"#### Results: Found {len(result)} records")
                    st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Query Error: {e}")
    
    # ======================== TAB 4: DATA EXPORT ========================
    with tab4:
        st.markdown("<div class='section-header'>Export & Download</div>", unsafe_allow_html=True)
        
        col_export1, col_export2, col_export3 = st. columns(3)
        
        with col_export1:
            st.markdown("#### 📥 Download Full Dataset")
            
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="data_export.csv",
                mime="text/csv"
            )
        
        with col_export2:
            st.markdown("#### 📊 Download Excel")
            
            output = BytesIO()
            with pd. ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
            
            st.download_button(
                label="📥 Download as Excel",
                data=output.getvalue(),
                file_name="data_export. xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col_export3:
            st.markdown("#### 📋 Download Statistics")
            
            stats_df = df.describe().T
            csv_stats = stats_df.to_csv()
            st.download_button(
                label="📥 Download Statistics",
                data=csv_stats,
                file_name="statistics.csv",
                mime="text/csv"
            )
        
        # Dataset Summary
        st.markdown("#### 📈 Dataset Summary")
        summary_col1, summary_col2, summary_col3, summary_col4 = st. columns(4)
        
        with summary_col1:
            st.metric("Total Rows", len(df))
        with summary_col2:
            st.metric("Total Columns", len(df.columns))
        with summary_col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        with summary_col4:
            st.metric("Data Types", len(df.dtypes. unique()))

# Footer
st.markdown("""
    ---
    <div style='text-align: center; color: #888; margin-top: 50px;'>
        <p>📊 🇩​​🇦​​🇹​​🇦​ ​🇸​​🇨​​🇮​​🇪​​🇳​​🇨​​🇪​ ​🇪​​🇩​​🇦​ ​🇦​​🇵​​🇵 | Built by Faiz Rao</p>
        <p>Upload your data and start exploring!</p>
    </div>
""", unsafe_allow_html=True)