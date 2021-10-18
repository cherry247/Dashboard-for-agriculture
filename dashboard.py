import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
items=['Apples','Wheat','Barley','Maize',"Tomatoes","Sugar cane","Potatoes","Olives"]
def load_cropData():
     data=pd.read_csv('.\data\FAOSTAT_data_10-16-2021.csv')
     return data
st.title("Data-Visualisation For Agriculture")
st.sidebar.title('Parameters')

#working with crop dataset
st.sidebar.subheader('Crop production')
if st.checkbox("Show  Crop Data"):
    st.write(load_cropData().head(20))
if not st.sidebar.checkbox("Yield quantities based on region", True, key='1'):
    select_region=st.sidebar.selectbox('region',['India','Morocco','Russian Federation'],key=1)
    select_item=st.sidebar.selectbox('Item',items,key=1)
    data=load_cropData()
    x=data[data["Item"]==select_item]
    y=x[x["Element"]=="Area harvested"] 
    n=x[x["Element"]=="Production"] 
    z=y[y["Area"]==select_region]
    z1=n[n["Area"]==select_region]
    string="Production/Yield quantities of "+select_item+" in "+select_region
    fig=go.Figure()
    fig.add_trace( go.Scatter(name="Area Harvested",x=z["Year"], y=z["Value"]))
    fig.add_trace(go.Scatter(name="Production",x=z1["Year"], y=z1["Value"] ))
    fig.update_layout(
    title=string,
    xaxis_title="years",
    yaxis_title="value",
    legend_title="element",)
    st.plotly_chart(fig)


if not st.sidebar.checkbox("Most Produced Commodities", True, key='1'):
    select_region=st.sidebar.radio('region',('India','Morocco','Russian Federation'))
    data=load_cropData()
    region=data[data["Area"]==select_region]
    region=region[region["Element"]=="Production"]
    region=region.groupby(["Item"]).mean()
    region=region.sort_values(by=["Value"],ascending=False)
    region=region[:15]
    st.markdown("Most Produced Commodities in "+select_region)
    fig=px.pie(region,names=region.index,values=region['Value'])
    st.plotly_chart(fig)

