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
  dfws= pd.read_csv(ws, names=['Date', 'Student', 'Guardian', 'PHONE', 'MailID', 'Location', 'Session', 'Class', 'Medium', 'Source', 'CollectedBy'])
  dupes= dfws[dfws.duplicated(['PHONE'], keep= False)]
  nulls= dfws[dfws['PHONE'].isna()]
  incs= dfws[dfws['PHONE'].astype(str).str.len()!=10]
  cors= dfws.drop_duplicates(subset= ['PHONE'])
  cors= cors[cors['PHONE'].notna()]
  cors= pd.concat([cors, incs, incs]).drop_duplicates(keep=False)
  st.subheader(f'{len(dfws)} rows: {len(cors)} CORRECT, {len(dupes)} DUPLICATE, {len(incs)} INCORRECT, {len(nulls)} MISSING')
  
  if st.checkbox('SHOW ME DETAILS:', key= 'ws'):
    if st.checkbox('SHOW CORRECT ENTRIES: (All phone numbers are proper)'):
      st.dataframe(cors)
      corsx= cors.to_csv()
      b64= base64.b64encode(corsx.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_Website_CORRECT.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download CORRECT ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)

    if st.checkbox('SHOW DUPLICATE ENTRIES: (Phone number is duplicated)'):
      st.dataframe(dupes)
      dupesx= dupes.to_csv()
      b64= base64.b64encode(dupesx.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_Website_DUPLICATES.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download DUPLICATE ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)
    
    if st.checkbox('SHOW INCORRECT ENTRIES: (Phone number is not of 10 digits or not numeric)'):
      st.dataframe(incs)
      incx= incs.to_csv()
      b64= base64.b64encode(incx.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_Website_INCORRECT.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download INCORRECT ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)
    
    if st.checkbox('SHOW MISSING ENTRIES: (Phone number is missing)'):
      st.dataframe(nulls)
      nullsx= nulls.to_csv()
      b64= base64.b64encode(nullsx.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_Website_MISSING.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download MISSING ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)

jb= st.file_uploader('Upload JB file here', type=['xls', 'csv', 'xlsx'], encoding= None, key= 'jb')
if jb is not None:
  dfjb= pd.read_csv(jb)
  dfjb['PHONE']= dfjb['PHONE'].str.replace(' ', '')
  cors2= dfjb[dfjb['PHONE'].astype(str).str.len()==10]
  cors2= cors2.append(dfjb[dfjb['PHONE'].astype(str).str.len()==21], ignore_index= False)
  # cors2= cors2.append(dfjb[dfjb['PHONE'].astype(str).str.len()==23], ignore_index= False)
  dupes2= dfjb[dfjb.duplicated(['PHONE'], keep= False)].dropna()
  nulls2= dfjb[dfjb['PHONE'].isna()]  
  incs2= dfjb[dfjb['PHONE'].astype(str).str.len()!=10]
  incs2= incs2.append(dfjb[dfjb['PHONE'].astype(str).str.len()!=21], ignore_index= False)
  incs2= incs2.append(dfjb[dfjb['PHONE'].astype(str).str.len()!=23], ignore_index= False)
  incs2= incs2.dropna()
  st.subheader(f'{len(dfjb)} rows: {len(cors2)} CORRECT, {len(dupes2)} DUPLICATE, {len(incs2)} INCORRECT, {len(nulls2)} MISSING')

  if st.checkbox('SHOW ME DETAILS:', key= 'jb'):
    if st.checkbox('SHOW CORRECT ENTRIES: (All phone numbers are proper)', key= 'jbcor'):
      st.dataframe(cors2)
      corsx2= cors2.to_csv()
      b64= base64.b64encode(corsx2.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_External_CORRECT.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download CORRECT ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)

    if st.checkbox('SHOW DUPLICATE ENTRIES: (Phone number is duplicated)', key= 'jbdup'):
      st.dataframe(dupes2)
      dupesx2= dupes2.to_csv()
      b64= base64.b64encode(dupesx2.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_External_DUPLICATES.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download DUPLICATE ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)
  
    if st.checkbox('SHOW INCORRECT ENTRIES: (Phone number is not of 10 digits or not numeric)', key= 'jbinc'):
      st.dataframe(incs2)
      incx2= incs2.to_csv()
      b64= base64.b64encode(incx2.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_External_INCORRECT.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download INCORRECT ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)
    
    if st.checkbox('SHOW MISSING ENTRIES: (Phone number is missing)', key= 'jbmis'):
      st.dataframe(nulls2)
      nullsx2= nulls2.to_csv()
      b64= base64.b64encode(nullsx2.encode()).decode()
      filen= date.today().strftime("%d_%b_%Y")+'_ZWS_External_MISSING.csv'
      dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download MISSING ENTRIES</a>'
      st.markdown(dlink, unsafe_allow_html=True)

  if st.button('Generate Merged MASTER DATA?'):
    master= cors.append(cors2, ignore_index= True)
    st.subheader(f'Integrated MASTER File has {len(master)} entries.')
    st.dataframe(master)
    mastercsv= master.to_csv()
    b64= base64.b64encode(mastercsv.encode()).decode()
    filen= date.today().strftime("%d_%b_%Y")+'_ZWS_MASTER.csv'
    dlink= f'<a href="data:file/csv;base64,{b64}" download="{filen}">Download MASTER FILE</a>'
    st.markdown(dlink, unsafe_allow_html=True)

    name1= 'TUMPA_'+date.today().strftime("%d_%b_%Y")+'_ZWS_MASTER.csv'
    name2= 'NABANITA_'+date.today().strftime("%d_%b_%Y")+'_ZWS_MASTER.csv'
    split= int(len(master)/2)
    # for file1
    file1= master.iloc[:split]
    mastercsv1= file1.to_csv()
    b641= base64.b64encode(mastercsv1.encode()).decode()
    filen1= 'TUMPA_'+date.today().strftime("%d_%b_%Y")+'_ZWS_MASTER.csv'
    dlink1= f'<a href="data:file/csv;base64,{b641}" download="{filen1}">Download MASTER FILE FOR TUMPA</a>'
    st.markdown(dlink1, unsafe_allow_html=True)
    # for file2
    file2= master.iloc[split:]
    mastercsv2= file2.to_csv()
    b642= base64.b64encode(mastercsv2.encode()).decode()
    filen2= 'NABANITA_'+date.today().strftime("%d_%b_%Y")+'_ZWS_MASTER.csv'
    dlink2= f'<a href="data:file/csv;base64,{b642}" download="{filen2}">Download MASTER FILE FOR NABANITA</a>'
    st.markdown(dlink2, unsafe_allow_html=True)

hide_streamlit_style = '<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>            '
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 