# Social Media User Engagement Measurement System (SMUEMS)

Welcome to the Social Media User Engagement Measurement System (SMUEMS)! This tool helps you analyze user engagement patterns from your social media data using association rule mining techniques. 

## Overview

**SMUEMS** allows you to:
1. **Import** Excel files exported from your Facebook Page.
2. **Analyze** user engagement patterns by applying the Apriori algorithm to detect frequent itemsets and association rules.
3. **Visualize** the results and gain actionable insights for improving user engagement.

## Features

- **Data Import**: Load your Facebook Page data from Excel files.
- **Customizable Parameters**: Set minimum support and confidence levels for the analysis.
- **Frequent Itemsets**: Discover frequently occurring itemsets in your data.
- **Association Rules**: Identify meaningful association rules based on support and confidence.
- **Visualization**: View results in a user-friendly format and get suggestions for engagement actions.

## Getting Started

To get started with SMUEMS:

1. **Export Data from Facebook**:
   - In your Facebook Page profile dashboard, go to “Meta Business Suite” in the left corner.
   - Click “Insights” and then “Content.”
   - Select the date range by clicking the “arrow down” symbol, choose the first and last date, and then click “Update.”
   - Click “Export Data” and then “Generate” to download the Excel file.

2. **Run the Application**:
   - **Browse Files**: Click "Browse files" to upload your Excel file.
   - **Set Parameters**: Enter the minimum support and confidence levels for the analysis.
   - **Analyze Data**: The system will display user engagement patterns and generate association rules.

## Usage

## Requirements

- Python 3.x
- Streamlit
- Pandas
- NumPy
- mlxtend

You can install the required packages using pip:

```bash
pip install streamlit pandas numpy mlxtend
```

## Acknowledgments

- **Streamlit** for creating the beautiful web interface.
- **mlxtend** for the Apriori algorithm implementation.

---
