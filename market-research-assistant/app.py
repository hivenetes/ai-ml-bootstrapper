import streamlit as st
import pandas as pd
import json
from crew_flow import MarketResearchAssistant
from comparison_report import ComparisonList

def display_comparison_table(comparison_list):
    try:
        # Convert the ComparisonList to a DataFrame
        comparisons = []
        for comp in comparison_list.comparisons:
            comparisons.append({
                'Category': comp.Category,
                'My_Product': comp.My_Product,
                "Competitor1": comp.Competitor1,
                "Competitor2": comp.Competitor2
            })
        
        # Create DataFrame
        df = pd.DataFrame(comparisons)
        df.set_index('Category', inplace=True)
        
        # Rename columns using session state values
        df.rename(columns={
            'My_Product': st.session_state.my_product,
            'Competitor1': st.session_state.competitor1,
            'Competitor2': st.session_state.competitor2
        }, inplace=True)
        
        # Add title
        st.write("")
        st.subheader(f" {st.session_state.my_product} Vs {st.session_state.competitor1} Vs {st.session_state.competitor2}")
                
        # Display the filtered DataFrame
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
        )
        
        # Add download button
        csv = df.to_csv()
        st.download_button(
            label="Download comparison as CSV",
            data=csv,
            file_name="comparison.csv",
            mime="text/csv",
        )

        # Display individual category details
        st.subheader("Category Details")
        for Category in df.index:
            with st.expander(Category):
                category_data = df.loc[Category]
                for column, value in category_data.items():
                    if column in df.columns:
                        st.write(f"**{column}:** {value}")
                        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        st.write("Raw data for debugging:", comparison_list)

# Usage
if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.title("Product Comparison Analysis")
    
    # Add competitor input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        my_product = st.text_input("My product name", "Narsi")
    with col2:
        competitor1 = st.text_input("Enter first competitor name", "GitHub Copilot")
    with col3:
        competitor2 = st.text_input("Enter second competitor name", "Cursor")
    
    if st.button("Generate Comparison"):
        if not my_product or not competitor1 or not competitor2:
            st.error("Please fill in all product names before generating comparison.")
        else:
            st.session_state.my_product = my_product
            st.session_state.competitor1 = competitor1
            st.session_state.competitor2 = competitor2

            with st.spinner('Generating Product Comparison Analysis Report'):
                flow = MarketResearchAssistant()
                comparison_data = flow.kickoff()  
                comparison_list = ComparisonList(comparisons=comparison_data["comparisons"])
                display_comparison_table(comparison_list) 


