import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random

def generate_org_data():
    departments = ['Engineering', 'Marketing', 'Sales', 'Finance']
    org_data = []
    
    for dept in departments:
        org_data.append(('CEO', dept))
        
        for i in range(random.randint(2, 3)):
            manager = f'{dept} Manager {i+1}'
            org_data.append((dept, manager))
            
            for j in range(random.randint(2, 3)):
                team_lead = f'{dept} Team Lead {i+1}-{j+1}'
                org_data.append((manager, team_lead))
                
                employees = [f'{dept} Employee {i+1}-{j+1}-{k+1}' for k in range(random.randint(5, 10))]
                org_data.append((team_lead, employees))
    
    return org_data

def create_org_chart(org_data):
    nodes = []
    edges = []
    node_ids = set()
    
    def add_node(id, label, level, employees=None):
        if id not in node_ids:
            title = f"Employees: {', '.join(employees)}" if employees else None
            nodes.append(Node(id=id, label=label, size=25, shape="circle", 
                              title=title, level=level))
            node_ids.add(id)

    add_node('CEO', 'CEO', 0)
    
    for item in org_data:
        if isinstance(item[1], list):  # Team lead with employees
            parent = item[0]
            employees = item[1]
            if parent not in node_ids:
                department, role, numbers = parent.split(' ', 2)
                add_node(parent, f"{role}\n{numbers}", 3, employees)
        else:
            parent, child = item
            if parent == 'CEO':
                add_node(child, child, 1)
            elif 'Manager' in child:
                add_node(child, child.split(' ', 1)[1], 2)
            elif 'Team Lead' in child:
                department, role, numbers = child.split(' ', 2)
                add_node(child, f"{role}\n{numbers}", 3)
            
            edges.append(Edge(source=parent, target=child))

    config = Config(width=800,
                    height=600,
                    directed=True,
                    physics=False,
                    hierarchical=True,
                    hierarchical_sort_method="directed",
                    nodeHighlightBehavior=True, 
                    highlightColor="#F7A7A6",
                    collapsible=False)

    return nodes, edges, config

st.title("Organizational Hierarchy Visualization")

org_data = generate_org_data()
nodes, edges, config = create_org_chart(org_data)

agraph(nodes=nodes, edges=edges, config=config)

if st.checkbox("Show raw data"):
    st.write(org_data)