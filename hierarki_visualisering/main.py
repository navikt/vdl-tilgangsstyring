import streamlit as st
import graphviz

st.set_page_config(layout="wide")
st.title("Hello World")
st.write("This is a simple Streamlit app.")

conn = st.connection("snowflake").session()

@st.cache_data
def get_data():
    return conn.sql("select * from regnskap.marts.dim_artskonti").to_pandas()

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

graph = graphviz.Digraph()
for fra, til in edges:
    graph.edge(fra, til)

with st.container(height=600):
    st.graphviz_chart(graph)
