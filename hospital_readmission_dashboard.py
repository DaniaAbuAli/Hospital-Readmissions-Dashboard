import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(
    page_title="Hospital Readmission Dashboard",
    page_icon="🏥",
    layout="wide"
)
st.title("Hospital Readmission Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv('data/hospital_readmission_clean.csv')

def variable_distribution_by_age():

    columns_dict={
    'Time in hospital': 'time_in_hospital',
    'Number of lab procedures': 'n_lab_procedures',
    'Number of procedures': 'n_procedures',
    'Number of medications': 'n_medications',
    'Number of outpatient visits': 'n_outpatient',
    'Number of inpatient visits': 'n_inpatient',
    'Number of emergency visits': 'n_emergency',
    'Medical specialty': 'medical_specialty',
    'Primary diagnosis': 'diag_1',
    'Secondary diagnosis': 'diag_2',
    'Tertiary diagnosis': 'diag_3',
    'glucose test': 'glucose_test',
    'A1C test': 'A1Ctest',
    'Change in medication': 'change',
    'Diabetes medication': 'diabetes_med',
    'Readmission status': 'readmitted'
}
    
    selectbox1,selectbox2,selectbox3=st.columns(3)

    with selectbox1:
      variable=st.selectbox(label="",options=list(columns_dict.keys()),index=0)
    
    with selectbox2:
        age=st.selectbox(label="",options=['All ages']+sorted(df['age'].unique()),index=0)
    
    with selectbox3:
        chart_type=st.selectbox(label="",options=['Histogram','Pie'])
    
    if chart_type=='Histogram':
        if age=='All ages':
            fig_histogram=px.histogram(df,x=columns_dict[variable],color_discrete_sequence=['rgb(143, 36, 62)'])
            fig_histogram.update_layout(bargap=0.2,xaxis_title=variable,yaxis_title='Count')
            st.plotly_chart(fig_histogram)
        else :
            df_age=df[df['age']==age]
            fig_histogram=px.histogram(df_age,x=columns_dict[variable],color_discrete_sequence=['rgb(143, 36, 62)'])
            fig_histogram.update_layout(bargap=0.2,xaxis_title=variable,yaxis_title='Count')
            st.plotly_chart(fig_histogram)
    
    elif chart_type=='Pie':
         if age=='All ages':
            fig_pie=px.pie(df,names=columns_dict[variable],color_discrete_sequence=['rgb(143, 36, 62)'])
            fig_pie.update_layout(xaxis_title=variable,yaxis_title='Count')
            st.plotly_chart(fig_pie)
         else :
            df_age=df[df['age']==age]
            fig_pie=px.pie(df_age,names=columns_dict[variable],color_discrete_sequence=['rgb(143, 36, 62)'])
            fig_pie.update_layout(xaxis_title=variable,yaxis_title='Count')
            st.plotly_chart(fig_pie)

def analyze_length_of_stay():
    factors={
    'Number of lab procedures': 'n_lab_procedures',
    'Number of procedures': 'n_procedures',
    'Number of medications': 'n_medications',
    'Number of outpatient visits': 'n_outpatient',
    'Number of inpatient visits': 'n_inpatient',
    'Number of emergency visits': 'n_emergency',
    }

    variable=st.selectbox(label="",options=list(factors.keys()),index=0)

    fig_scatter=px.scatter(df,x=factors[variable],y='time_in_hospital',color_discrete_map={
    'yes': 'rgb(143, 36, 62)',
    'no': 'rgb(64, 64, 64)'
     } ,color='readmitted')
    fig_scatter.update_layout(xaxis_title=variable,yaxis_title='Time in hospital')
    st.plotly_chart(fig_scatter)

def length_of_stay_by_diagnosis():
    fig_box=px.box(df,x='diag_1',y='time_in_hospital',color='readmitted',color_discrete_sequence=['rgb(143, 36, 62)','rgb(64, 64, 64)'])
    fig_box.update_layout(xaxis_title='Primary diagnosis',yaxis_title='Time in hospital')
    st.plotly_chart(fig_box)

def age_readmission_analysis():
    procedure_map={
    'Number of lab procedures': 'n_lab_procedures',
    'Number of procedures': 'n_procedures',
    'Number of medications': 'n_medications',
    }
    procedure_type=st.selectbox(label="",options=list(procedure_map.keys()),index=0)
    selected_proc_avg=df.groupby(['age','readmitted'])[procedure_map[procedure_type]].mean().reset_index()
    fig_bar=px.bar(selected_proc_avg,x='age',y=procedure_map[procedure_type],color_discrete_sequence=['rgb(143, 36, 62)'])
    fig_bar.update_layout(xaxis_title='age',yaxis_title=procedure_map[procedure_type])
    st.plotly_chart(fig_bar)



df=load_data()

col1,col2,col3,col4,col5,col6 = st.columns(6, border=True)

st.markdown('''
<style>

[data-testid="stMetricLabel"] > div  {
    text-align: center;
}

/*center metric value*/
[data-testid="stMetricValue"] > div {
    text-align: center;
}

</style>
''', unsafe_allow_html=True)

with col1:
    total_patients=df.shape[0]
    st.metric(value=total_patients,label='Total Patients')
with col2: 
    avg_stay=round(df['time_in_hospital'].mean(),2)
    st.metric(value=avg_stay,label='Avg. Stay (days)')
with col3:
    readmission_rate=round((df['readmitted']=='yes').mean()*100,2)
    st.metric(value=f"{readmission_rate}%",label='Readmission Rate')
with col4:
    avg_procedures=round(df['n_procedures'].mean(),2)
    st.metric(value=avg_procedures,label='Avg. Procedures')
with col5:
    avg_lab_tests=round(df['n_lab_procedures'].mean(),2)
    st.metric(value=avg_lab_tests,label='Avg. Lab Tests')
with col6:
    avg_medications=round(df['n_medications'].mean(),2)
    st.metric(value=avg_medications,label='Avg. Medications')

row1_col1,row1_col2=st.columns(2, border=True)

with row1_col1:
    st.write('###### Variable Distribution by Age Group')
    variable_distribution_by_age()

with row1_col2:
    st.write('###### Factors Influencing Length of Stay')
    analyze_length_of_stay()

row2_col1,row2_col2=st.columns(2, border=True)

with row2_col1:
    st.write('###### Length of Stay by Primary Diagnosis')
    length_of_stay_by_diagnosis()

with row2_col2:
    st.write('###### Medical Interventions by Age and Readmission')
    age_readmission_analysis()

st.markdown('''
<style>

 .stColumn {
    background-color:#fdfdfd
}

</style>
''', unsafe_allow_html=True)











