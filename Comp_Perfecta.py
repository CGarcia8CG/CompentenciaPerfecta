from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
from sympy import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

print(1+1)
P,Q,Qs,Qd = symbols("P,Q,Qs,Qd")
#python -m streamlit run Comp_Perfecta.py
#conn = psycopg2.connect(
#    host="localhost",
#    database="Alumnos_08_2022",
#    user="postgres",
#    password="Axia307032@")

#cur = conn.cursor()
#print('PostgreSQL database version:')

#sql0 = '''SELECT LOWER(nombres1) as nombres1, correos1 FROM public.lista_oficial
#ORDER BY nombres1 ASC'''
#data0 = pd.read_sql_query(sql0, conn)
#print(data0)

# Space out the maps so the first one is 2x the size of the other three
st.set_page_config(layout="wide")
#col1, col2, col3= st.columns((1, 2, 2))
#col1, col2, col3 = st.columns(3)

# Using object notation

# Using "with" notation
with st.sidebar:
    st.header("Información relevante: ")
    st.write("Hola soy una app para calcular ejercicos de Competencia Perfecta")
    st.write("Creado con Python y Streamlit")
    st.write("Elaborado por Carlos David García Hernández")
    



#col1, col2, col3= st.columns((1, 2, 2))
col1, col2, col3 = st.columns(3)
with col1:

    st.header("Ingresar coeficientes del Costo Total")
    number0 = st.number_input('Coeficiente cúbico',disabled=False)
    st.write('The current number is ', number0)

    number1 = st.number_input('Coeficiente cuadrático',disabled=False)
    st.write('The current number is ', number1)

    number2 = st.number_input('Coeficiente lineal')
    st.write('The current number is ', number2)

    number3 = st.number_input('Coeficiente escalar')
    st.write('The current number is ', number3)

with col2:
    st.header("Tu función de Costo Total es: ")
    CT = number0*Q**3 + number1*Q**2 + number2*Q + number3
    st.write(CT)

with col3:
    st.header("Tu función de Costo Marginal es: ")
    Cmg = diff(CT)
    st.write(Cmg)


#col4, col5, col6= st.columns((3, 2, 2))
col4, col5, col6 = st.columns(3)
with col4:
    st.header("Ingresar coeficientes de la función de Demanda")
    number4 = st.number_input('Coeficiente Demanda cuadrático',disabled=True)
    st.write('The current number is ', number4)

    number5 = st.number_input('Coeficiente Demanda lineal', max_value=0)
    st.write('The current number is ', number5)

    number6 = st.number_input('Coeficiente Demanda escalar')
    st.write('The current number is ', number6)

with col5:
    st.header("Tu función de Demanda es: ")
    Qdem = number4*P**2 + number5*P + number6
    st.write(Qdem)

with col6:
    pass
    #st.header("Tu función de Costo Marginal es: ")
    #Qdemm = diff(Qdem)
    #st.write(Qdemm)


col7, col8, col9 = st.columns(3)
with col7:
    st.header("Ingresar coeficientes de la función de Oferta")
    number7 = st.number_input('Coeficiente Oferta cuadrático',disabled=True)
    st.write('The current number is ', number7)

    number8 = st.number_input('Coeficiente Oferta lineal', min_value=0)
    st.write('The current number is ', number8)

    number9 = st.number_input('Coeficiente Oferta escalar')
    st.write('The current number is ', number9)

with col8:
    st.header("Tu función de Oferta es: ")
    Qofe = number7*P**2 + number8*P + number9
    st.write(Qofe)

with col9:
    pass
    #st.header("Tu función de Costo Marginal es: ")
    #Cmg = diff(CT)
    #st.write(Cmg)

col10, col11 = st.columns(2)
with col10:
    #Qs1 = 20*P - 2000
    #Qd1 = 10000-10*P
    #P1 = 20*P-2000 - 10000 +10*P
    st.header("Igualand Oferta y Demanda")
    P1 = (Qofe +(-1*Qdem))
    Peq = solve(P1,P)
    st.write(P1)
    st.write(Peq[-1])

with col11:
    #st.experimental_rerun()
    st.header("Igualando Precio con Costo Marginal")
    CmgP = Cmg + float(Peq[-1])*-1
    #CmgP = solve(Cmg + (-1*solve(P1,P)), Q)
    Sol =  solve(CmgP,Q)
    st.write(CmgP)
    st.write(Sol[-1])

col12, col13 = st.columns((5,1))
with col12:
    l1 = list(range(int(Sol[-1])-10, int(Sol[-1])+10))
    l6 = []
    l7 = []
    Precio = [None] * len(l1)
    for ele in range(0,len(Precio),1):
        Precio[ele]=float(Peq[-1])

    
    for v in l1:
        ct = float(number0*v**3 + number1*v**2 +number2*v + number3)
        s2= float(number0*3*v**2 + number1*2*v + number2*1)
        Ing = float(Peq[-1]*v - ct)
        l6.append(s2)
        l7.append(Ing)

    #list_of_lists = [l1,Precio,l6,l7]
    #numpy_array = np.array(list_of_lists).T

    chart_data = pd.DataFrame([l1,Precio,l6,l7]).T
    chart_data.columns=['Q',"P", 'Costo Marginal', 'Utilidad']

    #st.line_chart(chart_data.T)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
          x=l1,
          y=l6,
          name = "Cmg", # Style name/legend entry with html tags,
          mode='lines+markers',
      ),
     secondary_y=False)

    fig.add_trace(go.Scatter(
          x=l1,
          y=l7,
          name = "Utilidad", # Style name/legend entry with html tags,
          mode='lines+markers',
      ),
     secondary_y=True)

    fig.add_trace(go.Scatter(
          x=l1,
          y=Precio,
          name = "Precio", # Style name/legend entry with html tags,
          mode='lines+markers',
      ),
     secondary_y=False)


    fig.update_layout(title = 'Solución Óptima',xaxis = dict(title = 'Q'),
                   yaxis = dict(title = 'Cmg, Precio y Beneficio'),
                   bargap = 0.1, width=1200, height=1200)

    st.header("Grafico de resultados")
    st.plotly_chart(fig, use_container_width=True)