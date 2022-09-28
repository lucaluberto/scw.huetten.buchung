
#----------------------------
# Import Stuff
#----------------------------
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import calendar
import numpy as np
from openpyxl import Workbook


#-----------------
# Plotting Stuff
#-----------------
import plotly.graph_objects as go
from plotly.colors import n_colors, hex_to_rgb,label_rgb
import plotly.figure_factory as ff 


#-----------------
# Colors
#-----------------
scw_blau_1=label_rgb(hex_to_rgb('#2b5db2'))
scw_blau_2=label_rgb(hex_to_rgb('#EFF2F9'))

#----------------------------
# Read excel....
#----------------------------
df = pd.read_excel(

    io = 'huettenbelegung.xlsx',
    engine = 'openpyxl',
    sheet_name = 'Buchungen',
    usecols = 'A:O',
    skiprows = 1,
    nrows = 1000,
)



#:::::::::::::::::::::::::::::::::::::::::::::::
# Layout Dashboard - INPUT
#:::::::::::::::::::::::::::::::::::::::::::::::
st.set_page_config(page_title = "Buchung"
                  )

# Default Werte
today    = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

start_date = st.date_input('Anreise', today)
end_date   = st.date_input('Abreise', tomorrow)

if start_date > end_date:
    st.error('Error: Abreisedatum muss hinter Anreisedatum liegen!')

#st.write(df)    
  
df_zeitraum = df.query(
    "Datum >= @start_date & Datum <= @end_date"
)

#st.dataframe(df_zeitraum)

with st.form('form'):
    sel_column = st.multiselect('Zimmer auswählen:', df_zeitraum.columns[1:],
       help='In Zeile klicken um weitere Zimmer zur Auswahl hinzufügen. Drück "Zimmer frei?" um Auwahl.')
    #drop_na = st.checkbox('Drop rows with missing value', value=True)
    submitted = st.form_submit_button("Zimmer frei?")
    
if submitted:
    dfnew = df_zeitraum[sel_column]
    
    
    #if drop_na:
    #    dfnew = dfnew.dropna()

    st.write('Zimmer')
    dfnew = dfnew.fillna('frei')
    
    idx = (dfnew != 'frei')
    dfnew[idx] = 'Besetzt'
    
    result = pd.concat([df_zeitraum["Datum"],dfnew], axis=1)

    fig1 =  ff.create_table(result)
    
    st.plotly_chart(fig1)

#dfnew.replace(to_replace = 'frei', value = 'Besetzt', inplace=True)








    
 
    
    
    
 