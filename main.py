from library import *

st.set_page_config(page_title="SMUEMS", page_icon="icon.png")

title = "Social Media User Engagement Measurement System"
developer = "Developed by Daimler Benz Alebaba, Dr. Suaini Sura, and Dr. Nooralisa Mohd Tuah"
about = "Data Mining Web Application"

st.markdown(
    f'<div style="text-align: center; font-size: xxx-large; font-weight: bold;">{title}</div>'
    f'<div style="text-align: center; font-size: medium;">{developer}</div>'
    f'<div style="text-align: center; font-size: medium; font-weight: bolder;">{about}</div>',
    unsafe_allow_html=True
)

# Read data from Excel file
def get_excel_file_path():
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file is not None:
        return uploaded_file

    return None

# Define a function to format frozensets
def format_frozenset(frozenset_obj):
    return ', '.join(map(str, frozenset_obj))

def main():

    # Read data from Excel file
    excel_file = get_excel_file_path()

    if excel_file is not None:
        df = pd.read_excel(excel_file)
        df.replace(0, np.nan, inplace=True)
    else:
        st.write("No file selected.")
        return

    # Get the name of the first column and rename it to 'content_id'
    first_column_name = df.columns[0]
    df.rename(columns={first_column_name: 'content_id'}, inplace=True)

    # Get the 'content_id' column and rename field into content_(n)
    df['content_id'] = 'content_' + (df['content_id'].index + 1).astype(str)

    # Transform into frequency data
    melted_df = pd.melt(df, id_vars=['content_id'], var_name='ugc', value_name='frequency')
    melted_df = melted_df.dropna(subset=['frequency'])
    melted_df = melted_df.sort_values(by=['content_id', 'ugc'])

    melted_df['content_number'] = pd.to_numeric(melted_df['content_id'], errors='coerce', downcast='integer')
    melted_df = melted_df.sort_values(by=['content_number', 'ugc'])
    melted_df = melted_df.drop(columns=['content_number'])

    # Create binary matrix
    binary_matrix = create_binary_matrix(melted_df, ['content_id', 'ugc'])

    # Get user input for minimum support and confidence
    input_min_support = st.number_input("Enter minimum support:", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    input_min_confidence = st.number_input("Enter minimum confidence:", min_value=0.0, max_value=1.0, value=1.00, step=0.01)

    # Perform Apriori algorithm
    frequent_itemsets = apriori(binary_matrix, min_support=input_min_support, use_colnames=True)
    sorted_frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)

    # Perform association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=input_min_confidence)
    
    if 'antecedents' in rules.columns:
        sorted_rules = rules.sort_values(by=['confidence', 'support'], ascending=[False, False])

        # Apply formatting function to antecedents and consequents columns
        sorted_frequent_itemsets['itemsets'] = sorted_frequent_itemsets['itemsets'].apply(format_frozenset)
        sorted_rules['antecedents'] = sorted_rules['antecedents'].apply(format_frozenset)
        sorted_rules['consequents'] = sorted_rules['consequents'].apply(format_frozenset)

        # Display frequent itemsets
        selected_columns_frequent = ['support', 'itemsets']
        st.write("Frequent Itemsets:")
        st.dataframe(sorted_frequent_itemsets[selected_columns_frequent], width=800)

        # Display association rules
        selected_columns = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
        st.write("Association Rules:")
        st.dataframe(sorted_rules[selected_columns], width=800)

        # Display plot
        plot(sorted_rules, method="graph", control=['antecedents', 'consequents'])

        # Get suggestions based on association rules
        engagement_suggestions = suggest_engagement_actions(sorted_rules)

        # Display suggestions
        st.write("Engagement Suggestions:")
        engagement_suggestions = suggest_engagement_actions(sorted_rules, max_suggestions=3)
        for suggestion in engagement_suggestions:
            st.write(suggestion)

if __name__ == '__main__':
    main()
