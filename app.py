import streamlit as st
import pandas as pd
import io
st.set_page_config(
    page_title="Laptop Recommendation System",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, portfolio-ready appearance
st.markdown("""
    <style>
        /* Main container styling */
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #4B5563;
            margin-bottom: 2rem;
        }
        /* Custom card styling for laptop recommendations */
        .laptop-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .laptop-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #3B82F6;
        }
        .laptop-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        .laptop-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1E3A8A;
        }
        .laptop-price {
            font-size: 1.4rem;
            font-weight: 800;
            color: #10B981;
        }
        .spec-label {
            font-weight: 600;
            color: #4B5563;
        }
        .spec-value {
            color: #1F2937;
        }
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #6B7280;
            font-size: 0.9rem;
            border-top: 1px solid #E5E7EB;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING FUNCTION
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    Loads the laptop dataset from a CSV file, enforces specific encodings, 
    and handles basic data clean-up for accurate filtering.
    """
    try:
        # Load data with the specified encoding
        df = pd.read_csv("laptop_price.csv", encoding="latin1")
        
        # Strip string values to prevent whitespace mismatch errors in filtering
        string_cols = ['Company', 'Product', 'TypeName', 'Ram', 'Cpu', 'Gpu', 'OpSys', 'Memory']
        for col in string_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                  
        return df
    except FileNotFoundError:
        st.error("Error: 'laptop_price.csv' file not found. Please ensure it is in the same directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading data: {e}")
        return pd.DataFrame()

# -----------------------------------------------------------------------------
# 3. FILTERING LOGIC FUNCTION
# -----------------------------------------------------------------------------
def filter_laptops(df, company, laptop_type, ram, opsys, max_budget, search_query):
    """
    Applies conditional logic to filter down the main dataframe 
    based on sidebar filter criteria and search parameters.
    """
    filtered_df = df.copy()

    # Apply Dropdown selections (Only filter if a specific choice is made instead of "All")
    if company != "All":
        filtered_df = filtered_df[filtered_df['Company'] == company]
        
    if laptop_type != "All":
        filtered_df = filtered_df[filtered_df['TypeName'] == laptop_type]
        
    if ram != "All":
        filtered_df = filtered_df[filtered_df['Ram'] == ram]
        
    if opsys != "All":
        filtered_df = filtered_df[filtered_df['OpSys'] == opsys]

    # Apply Slider budget boundary
    filtered_df = filtered_df[filtered_df['Price_euros'] <= max_budget]

    # Apply Text search match on the Product column
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]

    return filtered_df

# -----------------------------------------------------------------------------
# 4. SORTING LOGIC FUNCTION
# -----------------------------------------------------------------------------
def sort_laptops(df, sort_option):
    """
    Sorts the data according to the option chosen in the main application area.
    """
    if sort_option == "Lowest Price":
        return df.sort_values(by='Price_euros', ascending=True)
    elif sort_option == "Highest Price":
        return df.sort_values(by='Price_euros', ascending=False)
    elif "Company A-Z" in sort_option:
        return df.sort_values(by='Company', ascending=True)
    elif "Company Z-A" in sort_option:
        return df.sort_values(by='Company', ascending=False)
    elif "Newest First" in sort_option:
        return df.sort_values(by='laptop_ID', ascending=True)
    return df

# -----------------------------------------------------------------------------
# 5. STATISTICS DISPLAY FUNCTION
# -----------------------------------------------------------------------------
def display_statistics(df):
    """
    Calculates key overview analytics dynamically matching the currently active filter scope.
    """
    if df.empty:
        total_laptops = 0
        unique_companies = 0
        avg_price = 0.0
        max_price = 0.0
        min_price = 0.0
    else:
        total_laptops = len(df)
        unique_companies = df['Company'].nunique()
        avg_price = float(df['Price_euros'].mean())
        max_price = float(df['Price_euros'].max())
        min_price = float(df['Price_euros'].min())

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Laptops 📊", value=f"{total_laptops}")
    with col2:
        st.metric(label="Unique Companies 🏢", value=f"{unique_companies}")
    with col3:
        st.metric(label="Average Price 💶", value=f"€{avg_price:,.2f}")
    with col4:
        st.metric(label="Maximum Price 📈", value=f"€{max_price:,.2f}")
    with col5:
        st.metric(label="Minimum Price 📉", value=f"€{min_price:,.2f}")

# -----------------------------------------------------------------------------
# 6. RECOMMENDATION CARD RENDERING FUNCTION
# -----------------------------------------------------------------------------
def display_cards(df):
    """
    Iterates through the filtered/sorted rows to render uniform, structured 
    HTML component layout panels for desktop displays.
    """
    for index, row in df.iterrows():
        with st.container():
            # Injecting HTML dynamically into a standard container block
            st.markdown(f"""
                <div class="laptop-card">
                    <div class="laptop-header">
                        <div class="laptop-title">🏢 {row['Company']} - {row['Product']}</div>
                        <div class="laptop-price">€{row['Price_euros']:,.2f}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.8rem;">
                        <div><span class="spec-label">💻 Type:</span> <span class="spec-value">{row['TypeName']}</span></div>
                        <div><span class="spec-label">💾 RAM:</span> <span class="spec-value">{row['Ram']}</span></div>
                        <div><span class="spec-label">⚙️ CPU:</span> <span class="spec-value">{row['Cpu']}</span></div>
                        <div><span class="spec-label">🎮 GPU:</span> <span class="spec-value">{row['Gpu']}</span></div>
                        <div><span class="spec-label">🗄️ Storage:</span> <span class="spec-value">{row['Memory']}</span></div>
                        <div><span class="spec-label">💿 OS:</span> <span class="spec-value">{row['OpSys']}</span></div>
                        <div><span class="spec-label">📏 Screen:</span> <span class="spec-value">{row['Inches']}" ({row['ScreenResolution']})</span></div>
                        <div><span class="spec-label">⚖️ Weight:</span> <span class="spec-value">{row['Weight']}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. EXPORT DATA PREPARATION FUNCTION
# -----------------------------------------------------------------------------
def download_csv(df):
    """
    Converts DataFrame into a raw binary CSV standard string compatible with standard downloads.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()

# -----------------------------------------------------------------------------
# 8. APPLICATION ENTRYPOINT MAIN METHOD
# -----------------------------------------------------------------------------
def main():
    # Load dataset
    df = load_data()
    
    if df.empty:
        st.error("Data loading failed. Application cannot proceed.")
        return

    # --- MAIN PAGE HEADER ---
    st.markdown('<div class="main-title">Laptop Recommendation System 💻</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Find your perfect computing companion based on customized spec parameters</div>', unsafe_allow_html=True)
    st.markdown("---")

    # --- SIDEBAR INTERFACE ---
    st.sidebar.header("🛠️ Selection Preferences")
    st.sidebar.write("Configure details to track exact feature targets:")
    
    # Generate interactive selection scopes dynamically from data distributions
    company_options = ["All"] + sorted(df['Company'].unique().tolist())
    type_options = ["All"] + sorted(df['TypeName'].unique().tolist())
    ram_options = ["All"] + sorted(df['Ram'].unique().tolist(), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 0)
    opsys_options = ["All"] + sorted(df['OpSys'].unique().tolist())
    
    min_price_dataset = float(df['Price_euros'].min())
    max_price_dataset = float(df['Price_euros'].max())

    # Build dropdown and numeric inputs
    selected_company = st.sidebar.selectbox("Company 🏢", options=company_options, index=0)
    selected_type = st.sidebar.selectbox("Laptop Type 💻", options=type_options, index=0)
    selected_ram = st.sidebar.selectbox("RAM (Memory Size) 💾", options=ram_options, index=0)
    selected_opsys = st.sidebar.selectbox("Operating System 💿", options=opsys_options, index=0)
    
    selected_budget = st.sidebar.slider(
        "Maximum Budget (In Euros) 💶",
        min_value=min_price_dataset,
        max_value=max_price_dataset,
        value=max_price_dataset,
        step=50.0,
        format="€%.2f"
    )

    st.sidebar.markdown("---")
    search_query = st.sidebar.text_input("Search by Product Name 🔍", placeholder="e.g. MacBook, ThinkPad...")

    # --- DATA EXPLORATION PANEL (DATASET PREVIEW) ---
    with st.expander("📂 View Source Data Sample (First 10 Rows)", expanded=False):
        st.write("Below is a sample overview of the foundational attributes from `laptop_price.csv`:")
        st.dataframe(df.head(10), use_container_width=True)

    # --- PROCESS AND MUTATE USER QUERY SELECTIONS ---
    filtered_data = filter_laptops(
        df, 
        selected_company, 
        selected_type, 
        selected_ram, 
        selected_opsys, 
        selected_budget, 
        search_query
    )

    # --- ANALYTICS AND METRICS METADATA BLOCK ---
    st.subheader("📊 Operational Analytics Dashboard")
    display_statistics(filtered_data)
    st.markdown("---")

    # --- PERFORMANCE RESULTS SECTION ---
    col_results_header, col_sort_action = st.columns([2, 1])
    
    with col_results_header:
        st.subheader("🎯 Tailored Laptop Recommendations")
        
    with col_sort_action:
        sort_choice = st.selectbox(
            "Sort Results By:",
            options=["Lowest Price", "Highest Price", "Company A-Z", "Company Z-A", "Newest First (Laptop ID)"],
            index=0
        )

    # Apply structural sorting logic
    final_data = sort_laptops(filtered_data, sort_choice)

    # Visual Output Rendering Decision Tree
    if final_data.empty:
        st.warning("No laptops found. Try changing filters.")
    else:
        st.success(f"Successfully matched **{len(final_data)}** configuration models meeting all defined boundaries!")
        
        # Download data element handling
        csv_data = download_csv(final_data)
        st.download_button(
            label="📥 Download Filtered Recommendations as CSV",
            data=csv_data,
            file_name="recommended_laptops.csv",
            mime="text/csv"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate custom layout display cards
        display_cards(final_data)

    # --- FOOTER ---
    st.markdown(
        """
        <div class="footer">
            <p>Developed by <b>G. Chandra Mani Shankar</b></p>
            <p>💡 DecodeLabs AI Internship Project 3 — Portfolio Build</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()