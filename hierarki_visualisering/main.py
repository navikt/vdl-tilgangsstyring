import streamlit as st
import graphviz

st.set_page_config(layout="wide")
st.title("Hello World")
st.write("This is a simple Streamlit app.")

conn = st.connection("snowflake").session()

@st.cache_data
def get_data():
    return conn.sql("select * from regnskap.marts.dim_artskonti where artskonti_segment_kode_niva_4 is not null").to_pandas()

artskontoer = get_data()


nivaer = {
    "nivå 1": {
        "koder": artskontoer["ARTSKONTI_SEGMENT_KODE_NIVA_1"].unique(),
        "kolonne": "ARTSKONTI_SEGMENT_KODE_NIVA_1",
    },
    "nivå 2": {
        "koder": artskontoer["ARTSKONTI_SEGMENT_KODE_NIVA_2"].unique(),
        "kolonne": "ARTSKONTI_SEGMENT_KODE_NIVA_2",
    },
    "nivå 3": {
        "koder": artskontoer["ARTSKONTI_SEGMENT_KODE_NIVA_3"].unique(),
        "kolonne": "ARTSKONTI_SEGMENT_KODE_NIVA_3",
    },
    "nivå 4": {
        "koder": artskontoer["ARTSKONTI_SEGMENT_KODE_NIVA_4"].unique(),
        "kolonne": "ARTSKONTI_SEGMENT_KODE_NIVA_4",
    },
}

selected_niva = st.selectbox("Velg artskonto nivå", nivaer.keys())

selected_koder = st.multiselect("Velg artskontoer", nivaer[selected_niva]["koder"])
display = artskontoer[
    artskontoer[nivaer[selected_niva]["kolonne"]].isin(selected_koder)
]

edges = set()
for k, v in display.iterrows():
    #    edges.add((v["ARTSKONTI_SEGMENT_KODE_NIVA_0"], v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]))
    edges.add((v["ARTSKONTI_SEGMENT_KODE_NIVA_1"], v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]))
    edges.add((v["ARTSKONTI_SEGMENT_KODE_NIVA_2"], v["ARTSKONTI_SEGMENT_KODE_NIVA_3"]))
    edges.add((v["ARTSKONTI_SEGMENT_KODE_NIVA_3"], v["ARTSKONTI_SEGMENT_KODE_NIVA_4"]))

graph = graphviz.Digraph(graph_attr={"rankdir": "LR"}, node_attr={"shape": "box"})
for fra, til in edges:
    graph.edge(fra, til)

with st.container(height=600):
    st.graphviz_chart(graph)

@st.cache_data
def construct_tree():
    artskonto_tre = {}
    for _, v in artskontoer.iterrows():
        if v["ARTSKONTI_SEGMENT_KODE_NIVA_0"] not in artskonto_tre:
            artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]] = {}
        if v["ARTSKONTI_SEGMENT_KODE_NIVA_1"] not in artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]]:
            artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]] = {}
        if v["ARTSKONTI_SEGMENT_KODE_NIVA_2"] not in artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]]:
            artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]] = {}
        if v["ARTSKONTI_SEGMENT_KODE_NIVA_3"] not in artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]]:
            artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_3"]] = {}
        if v["ARTSKONTI_SEGMENT_KODE_NIVA_4"] not in artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_3"]]:
            artskonto_tre[v["ARTSKONTI_SEGMENT_KODE_NIVA_0"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_1"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_2"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_3"]][v["ARTSKONTI_SEGMENT_KODE_NIVA_4"]] = {}
    return artskonto_tre

artskonto_tre = construct_tree()
st.write(artskonto_tre)
