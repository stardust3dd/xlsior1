import os, base64, csv
from datetime import date
import pandas as pd
import streamlit as st

st.title('Excel Merger')
st.set_option('deprecation.showfileUploaderEncoding', False)

def get_table_download_link(df):
  """Generates a link allowing the data in a given panda dataframe to be downloaded
  in:  dataframe
  out: href string
  """
  csv = df.to_excel(index=False)
  # b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
  href = f'<a href="data:file/csv;base64,{b64}">Download the duplicate entries file</a>'
  return href

ws= st.file_uploader('Upload WS file here', type=['xls', 'csv', 'xlsx'], encoding= None, key= 'ws', )
if ws is not None:
  dfws= pd.read_csv(ws, names=['Time', 'Student', 'Guardian', 'PHONE', 'MailID', 'Location', 'Session', 'Class', 'Medium', 'Source', 'CollectedBy'])
  dupes= dfws[dfws.duplicated(['PHONE'], keep= False)]
  nulls= dfws[dfws['PHONE'].isna()]
  incs= dfws[dfws['PHONE'].astype(str).str.len()!=10]
  cors= dfws.drop_duplicates(subset= ['PHONE'])
  cors= cors[cors['PHONE'].notna()]
  cors= pd.concat([cors, incs, incs]).drop_duplicates(keep=False)
  st.subheader(f'{len(dfws)} rows: {len(cors)} CORRECT, {len(dupes)} DUPLICATE, {len(incs)} INCORRECT, {len(nulls)} MISSING')
  
  if st.checkbox('SHOW CORRECT ENTRIES: (All phone numbers are proper)'):
    st.dataframe(cors)
    corsx= cors.to_csv()
    b64= base64.b64encode(corsx.encode()).decode()
    filen= date.today().strftime("%d_%b_%Y")+'_Website_CORRECT.csv'
    dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download CORRECT ENTRIES</a>'
    st.markdown(dlink, unsafe_allow_html=True)

  if st.checkbox('SHOW DUPLICATE ENTRIES: (Phone number is duplicated)'):
    st.dataframe(dupes)
    dupesx= dupes.to_csv()
    b64= base64.b64encode(dupesx.encode()).decode()
    filen= date.today().strftime("%d_%b_%Y")+'_Website_DUPLICATES.csv'
    dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download DUPLICATE ENTRIES</a>'
    st.markdown(dlink, unsafe_allow_html=True)
  
  if st.checkbox('SHOW INCORRECT ENTRIES: (Phone number is not of 10 digits or not numeric)'):
    st.dataframe(incs)
    incx= incs.to_csv()
    b64= base64.b64encode(incx.encode()).decode()
    filen= date.today().strftime("%d_%b_%Y")+'_Website_INCORRECT.csv'
    dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download INCORRECT ENTRIES</a>'
    st.markdown(dlink, unsafe_allow_html=True)
  
  if st.checkbox('SHOW MISSING ENTRIES: (Phone number is missing)'):
    st.dataframe(nulls)
    nullsx= nulls.to_csv()
    b64= base64.b64encode(nullsx.encode()).decode()
    filen= date.today().strftime("%d_%b_%Y")+'_Website_MISSING.csv'
    dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download MISSING ENTRIES</a>'
    st.markdown(dlink, unsafe_allow_html=True)

jb= st.file_uploader('Upload JB file here', type=['xls', 'csv', 'xlsx'], encoding= 'UTF-8', key= 'jb')
if jb is not None:
  dfjb= pd.read_csv(jb)
  st.dataframe(dfjb)

  if st.button('Generate Merged CleanedData?'):
    b64= base64.b64encode(nullsx.encode()).decode()
    dlink= f'<a href="data:file/csv;base64,{b64}" download="Missing.csv">Download MISSING ENTRIES</a>'
    st.markdown(dlink, unsafe_allow_html=True)

hide_streamlit_style = '<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>            '
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 