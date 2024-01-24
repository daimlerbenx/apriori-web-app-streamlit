"""
BSD 3-Clause License

Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
All rights reserved.

Copyright (c) 2011-2024, Open source contributors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import pandas as pd
"""
mlxtend documentation figures (c) by Sebastian Raschka

mlxtend documentation figures are licensed under a
Creative Commons Attribution 4.0 International License.

<https://creativecommons.org/licenses/by-sa/4.0/>.

You are free to:
================

Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material
for any purpose, even commercially.
The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
==========================

Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

"""
import numpy as np
from mlxtend.frequent_patterns import association_rules, apriori
import streamlit as st
import openpyxl
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def get_excel_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    return file_path

def save_to_excel(df, output_path):
    df.to_excel(output_path, index=False)
    print(f"Data has been saved to {output_path}")

def create_binary_matrix(df, columns):
    return pd.crosstab(df[columns[0]], df[columns[1]]).applymap(lambda x: 1 if x > 0 else 0)

def plot(data, method, control):
    if method == "scatter":
        fig, ax = plt.subplots()
        x_values = data[control[0]]
        y_values = data[control[1]]
        ax.scatter(x_values, y_values)
        ax.set_xlabel(control[0])
        ax.set_ylabel(control[1])
        ax.set_title("Scatter Plot")
        st.pyplot(fig)
    elif method == "graph":
        G = nx.Graph()
        for index, row in data.iterrows():
            G.add_edge(row['antecedents'], row['consequents'], confidence=row['confidence'])
        
        fig, ax = plt.subplots()
        pos = nx.circular_layout(G)
        
        # Draw edges
        edges = nx.draw_networkx_edges(G, pos, ax=ax)

        # Draw nodes
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax)

        # Draw labels on edges
        edge_labels = {(u, v): f"{G[u][v]['confidence']:.2f}" for u, v in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        # Draw node labels
        node_labels = {node: f"{node}" for node in G.nodes}
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax)

        ax.set_title("Network Graph (Confidence)")
        st.pyplot(fig)
    else:
        print("Unsupported plotting method")

def suggest_engagement_actions(rules, max_suggestions=5):
    suggestions = []

    # Filter rules with lift
    high_lift_rules = rules[rules['lift'] >= 1.0]

    # Get unique antecedents and consequents from high confidence rules
    unique_antecedents = high_lift_rules['antecedents'].unique()
    unique_consequents = high_lift_rules['consequents'].unique()

    # Suggest combinations of user engagement activities that tend to occur together
    for antecedent in unique_antecedents:
        for consequent in unique_consequents:
            if antecedent != consequent:
                suggestion = f"Suggest combining **{antecedent}** and **{consequent}** to boost user engagement."
                suggestions.append(suggestion)
                if len(suggestions) == max_suggestions:
                    break
        if len(suggestions) == max_suggestions:
            break

    return suggestions
