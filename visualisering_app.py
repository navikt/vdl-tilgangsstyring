import streamlit as st
import plotly.graph_objects as go
import random

# Generate example data
def generate_org_data():
    departments = ['Engineering', 'Marketing', 'Sales', 'Finance']
    org_data = []
    
    for dept in departments:
        org_data.append(('CEO', dept))
        
        for _ in range(random.randint(2, 4)):
            manager = f'{dept} Manager {random.randint(1, 5)}'
            org_data.append((dept, manager))
            
            for _ in range(random.randint(3, 6)):
                team_lead = f'{dept} Team Lead {random.randint(1, 10)}'
                org_data.append((manager, team_lead))
                
                for _ in range(random.randint(2, 5)):
                    employee = f'{dept} Employee {random.randint(1, 50)}'
                    org_data.append((team_lead, employee))
    
    return org_data

org_data = generate_org_data()
st.markdown(org_data)

# Create the organizational chart
def create_org_chart(org_data):
    nodes = set()
    for parent, child in org_data:
        nodes.add(parent)
        nodes.add(child)
    
    node_ids = {node: i for i, node in enumerate(nodes)}
    
    node_labels = list(nodes)
    node_parents = [''] * len(nodes)
    
    for parent, child in org_data:
        node_parents[node_ids[child]] = node_ids[parent]
    
    fig = go.Figure(go.Treemap(
        labels=node_labels,
        parents=[node_labels[i] if i != '' else '' for i in node_parents],
        root_color="lightgrey"
    ))
    
    fig.update_layout(
        title="Organizational Hierarchy",
        width=800,
        height=600,
        margin=dict(t=50, l=0, r=0, b=0)
    )
    
    return fig

# Streamlit app
st.title("Hierarki visualisering")

# Generate data and create chart
org_data = generate_org_data()
fig = create_org_chart(org_data)

# Display the chart
st.plotly_chart(fig)

# Display the raw data
if st.checkbox("Vis rådata"):
    st.write(org_data)