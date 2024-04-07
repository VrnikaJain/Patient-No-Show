import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df=pd.read_csv('KaggleV2-May-2016.csv')
    return df

data=load_data()

st.title("PATIENT NO-SHOW ANALYSIS")

bar_palette = "Spectral"
#Make choice between following options
st.sidebar.header('Choose the interest option: ')

analysis_options = [
    "Gender and No Show Rate",
    "Age and No Show Rate",
    "No Shows in a particular Doctor Neighbor",
    "Month, Date and Day wise Rate of No Show",
    "No Show after sending SMS",
    "Rate of No Show after granting a scholarship",
    "Diseases and Their Relationship to No Shows",
    "Appointment day difference VS No Show"
]

selected_analysis = st.sidebar.selectbox("Select Analysis", analysis_options)

#Apply filters
if selected_analysis == "Gender and No Show Rate":
    gender_filter = st.sidebar.selectbox("Select Gender", ["All"] + data['Gender'].unique().tolist())
elif selected_analysis == "Age and No Show Rate":
    age_min = int(data['Age'].min())
    age_max = int(data['Age'].max())
    age_filter_min, age_filter_max = st.sidebar.slider("Select Age Range", age_min, age_max, (age_min, age_max))
elif selected_analysis == "No Shows in a particular Doctor Neighbor":
    doctor_neighbor_filter = st.sidebar.selectbox("Select Doctor Neighbor", ["All"] + data['Neighbourhood'].unique().tolist())
elif selected_analysis == "Month, Date and Day wise Rate of No Show":
    pass  # No specific filter needed
elif selected_analysis == "No Show after sending SMS":
    pass  # No specific filter needed
elif selected_analysis == "Rate of No Show after granting a scholarship":
    pass  # No specific filter needed
elif selected_analysis == "Diseases and Their Relationship to No Shows":
    pass  # No specific filter needed
elif selected_analysis == "Appointment day difference VS No Show":
    pass  # No specific filter needed

#Filter Data based on selected options
filtered_df = data.copy()
if selected_analysis == "Gender and No Show Rate" and gender_filter != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]
elif selected_analysis == "Age and No Show Rate":
    filtered_df = filtered_df[(filtered_df['Age'] >= age_filter_min) & (filtered_df['Age'] <= age_filter_max)]
elif selected_analysis == "No Shows in a particular Doctor Neighbor" and doctor_neighbor_filter != "All":
    filtered_df = filtered_df[filtered_df['Neighbourhood'] == doctor_neighbor_filter]


#Selection and filtering
if selected_analysis == "Gender and No Show Rate":
    st.subheader('Gender and No Show Rate')

    # Calculate total counts by gender
    total_counts_by_gender = filtered_df['Gender'].value_counts()

    # Calculate No Show counts by gender
    no_show_counts_by_gender = filtered_df[filtered_df['No-show'] == 'Yes']['Gender'].value_counts()

    # Calculate percentage of no-shows by gender
    no_show_percentage_by_gender = (no_show_counts_by_gender / total_counts_by_gender) * 100

    # Plot No Show Rates by Gender
    fig, ax = plt.subplots()
    sns.barplot( x=no_show_percentage_by_gender.values, y=no_show_percentage_by_gender.index, ax=ax, palette=bar_palette)
    
    ax.set_xlabel('Gender')
    ax.set_ylabel('Percentage of No Shows')
    ax.set_title('No Show Percentage by Gender')
    ax.set_xticklabels(no_show_percentage_by_gender.index, fontsize=8)
    
    # Adding percentage labels to the bars
    for i, v in enumerate(no_show_percentage_by_gender.values):
        ax.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom', fontsize=8, color='black')

    st.pyplot(fig)


elif selected_analysis == "Age and No Show Rate":
    st.subheader('Age and No Show Rate')

    # Calculate total counts by age group
    total_counts_by_age_group = filtered_df['Age'].value_counts()

    # Calculate No Show counts by age group
    no_show_counts_by_age_group = filtered_df[filtered_df['No-show'] == 'Yes']['Age'].value_counts()

    # Calculate percentage of no-shows by age group
    no_show_percentage_by_age_group = (no_show_counts_by_age_group / total_counts_by_age_group) * 100

    # Plot No Show Rates by Age Group
    fig, ax = plt.subplots()
    sns.barplot(x=no_show_percentage_by_age_group.values, y=no_show_percentage_by_age_group.index, ax=ax, palette=bar_palette)
    
    ax.set_xlabel('Age Group')
    ax.set_ylabel('No Shows Percentage')
    ax.set_title('No Show Percentage by Age Group')
    ax.set_ylim(bottom=0)
    ax.set_xticklabels(no_show_percentage_by_age_group.index, rotation=90, fontsize=4)
    ax.set_yticklabels([]) 
    
    # Ensure no_show_percentage_by_age_group is a DataFrame before iterating over rows
    if isinstance(no_show_percentage_by_age_group, pd.DataFrame):
        for i, (index, row) in enumerate(no_show_percentage_by_age_group.iterrows()):
            for j, value in enumerate(row):
                ax.text(value, i, f"{value:.2f}%", ha='center', va='center', fontsize=12, color='grey')
    
    st.pyplot(fig)


elif selected_analysis == "No Shows in a particular Doctor Neighbor":
    st.subheader('No Shows in a particular Doctor Neighbor')

    # Filter Options
    doctor_neighbor_filter = st.sidebar.selectbox("Select Doctor Neighbor", filtered_df['Neighbourhood'].unique().tolist())

    # Filter Data based on selected doctor neighbor
    if doctor_neighbor_filter != "All":
        filtered_df = filtered_df[filtered_df['Neighbourhood'] == doctor_neighbor_filter]

    # Calculate total counts by doctor neighbor
    total_counts_by_doctor_neighbor = filtered_df['Neighbourhood'].value_counts()

    # Calculate No Show counts by doctor neighbor
    no_show_counts_by_doctor_neighbor = filtered_df[filtered_df['No-show'] == 'Yes']['Neighbourhood'].value_counts()

    # Calculate percentage of no-shows by doctor neighbor
    no_show_percentage_by_doctor_neighbor = (no_show_counts_by_doctor_neighbor / total_counts_by_doctor_neighbor) * 100

    # Plot No Show Rates by Doctor Neighbor
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=no_show_percentage_by_doctor_neighbor.values, y=no_show_percentage_by_doctor_neighbor.index, ax=ax, palette=bar_palette)

    ax.set_xlabel('Percentage of No Shows')
    ax.set_ylabel('Doctor Neighbor')
    ax.set_title('No Show Percentage by Doctor Neighbor')
    ax.set_xlim(left=0)
    
    # Adding percentage labels to the bars
    for i, v in enumerate(no_show_percentage_by_doctor_neighbor.values):
        ax.text(v, i, f"{v:.2f}%", ha='center', va='center', fontsize=10, color='grey')

    st.pyplot(fig)


elif selected_analysis == "Month, Date and Day wise Rate of No Show":
    st.subheader('Month, Date and Day wise Rate of No Show')

    # Convert ScheduledDay and AppointmentDay columns to datetime
    filtered_df['ScheduledDay'] = pd.to_datetime(filtered_df['ScheduledDay'])
    filtered_df['AppointmentDay'] = pd.to_datetime(filtered_df['AppointmentDay'])

    # Extract Month and Date
    filtered_df['ScheduledMonth'] = filtered_df['ScheduledDay'].dt.month
    filtered_df['ScheduledDate'] = filtered_df['ScheduledDay'].dt.day

    # Calculate No Show rates by Scheduled Month
    no_show_percentage_by_month = filtered_df.groupby(['ScheduledMonth', 'No-show']).size().unstack().fillna(0)
    no_show_percentage_by_month['No Show Percentage'] = (no_show_percentage_by_month['Yes'] / (no_show_percentage_by_month['Yes'] + no_show_percentage_by_month['No'])) * 100

    # Plot No Show Rates by Scheduled Month
    st.write("No Show Rates by Scheduled Month:")
    fig, ax = plt.subplots()
    no_show_percentage_by_month['No Show Percentage'].plot(kind='line', marker='o', ax=ax, color=bar_palette)
    ax.set_xlabel('Scheduled Month')
    ax.set_ylabel('Percentage of No Shows')
    ax.set_title('No Show Rates by Scheduled Month')
    ax.set_xticks(no_show_percentage_by_month.index)
    ax.set_xticklabels(no_show_percentage_by_month.index)
    st.pyplot(fig)

    # Calculate No Show rates by Scheduled Date
    no_show_percentage_by_date = filtered_df.groupby(['ScheduledDate', 'No-show']).size().unstack().fillna(0)
    no_show_percentage_by_date['No Show Percentage'] = (no_show_percentage_by_date['Yes'] / (no_show_percentage_by_date['Yes'] + no_show_percentage_by_date['No'])) * 100

    # Plot No Show Rates by Scheduled Date
    st.write("No Show Rates by Scheduled Date:")
    fig, ax = plt.subplots()
    no_show_percentage_by_date['No Show Percentage'].plot(kind='line', marker='o', ax=ax, color=bar_palette)
    ax.set_xlabel('Scheduled Date')
    ax.set_ylabel('Percentage of No Shows')
    ax.set_title('No Show Rates by Scheduled Date')
    ax.set_xticks(no_show_percentage_by_date.index)
    ax.set_xticklabels(no_show_percentage_by_date.index)
    st.pyplot(fig)


elif selected_analysis == "No Show after sending SMS":
    st.subheader('No Show after sending SMS')

    # Count the occurrences of SMS received and no-shows
    sms_no_show_count = filtered_df.groupby(['SMS_received', 'No-show']).size().unstack(fill_value=0)

    # Plot the relationship between SMS received and no-show
    fig, ax = plt.subplots(figsize=(8, 6))
    sms_no_show_count.plot(kind='bar', ax=ax,  color=['#6495ED', '#98FB98'])
    for i, (index, row) in enumerate(sms_no_show_count.iterrows()):
        for j, value in enumerate(row):
            ax.text(i, value, str(value), ha='center', va='bottom', fontsize=10, color='grey')
    ax.set_xlabel('No-show')
    #ax.set_ylabel('Count of SMS Received')
    ax.set_title('No Show after sending SMS')
    ax.set_yticklabels(sms_no_show_count.index)
    st.pyplot(fig)


elif selected_analysis == "Rate of No Show after granting a scholarship":
    st.subheader('Rate of No Show after granting a scholarship')

    # Count the occurrences of scholarship and no-shows
    scholarship_no_show_count = filtered_df.groupby(['Scholarship', 'No-show']).size().unstack(fill_value=0)

    # Plot the relationship between scholarship and no-show
    fig, ax = plt.subplots(figsize=(8, 6))
    scholarship_no_show_count.plot(kind='bar', ax=ax,  color=['#6495ED', '#98FB98'])
    for i, (index, row) in enumerate(scholarship_no_show_count.iterrows()):
        for j, value in enumerate(row):
            ax.text(i, value, str(value), ha='center', va='bottom', fontsize=10, color='grey')
    ax.set_xlabel('No-show')
    ax.set_ylabel('Count')
    ax.set_title('Rate of No Show after granting a scholarship')
    ax.set_yticklabels(scholarship_no_show_count.index)
    st.pyplot(fig)


elif selected_analysis == "Diseases and Their Relationship to No Shows":
    st.subheader('Diseases and Their Relationship to No Shows')

    # Create a dataframe to store the presence of diseases for each patient
    diseases_df = filtered_df[['PatientId', 'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']]
    
    # Melt the dataframe to have a single column for disease type and another column for disease presence
    diseases_df_melted = diseases_df.melt(id_vars=['PatientId'], var_name='Disease', value_name='Presence')

    # Filter out rows where disease presence is True
    diseases_present_df = diseases_df_melted[diseases_df_melted['Presence'] == 1]

    # Count the number of occurrences of each disease for each patient
    diseases_count_df = diseases_present_df.groupby(['PatientId', 'Disease']).size().unstack(fill_value=0)

    # Plot the presence of diseases for each patient
    fig, ax = plt.subplots(figsize=(10, 6))
    diseases_count_df.plot(kind='bar', stacked=True, ax=ax, color=['#6495ED', '#98FB98', '#FFA07A', '#9370DB'])
    ax.set_xlabel('Patient ID')
    ax.set_ylabel('Count of Disease')
    ax.set_title('Diseases and Their Relationship to No Shows')
    ax.legend(title='Disease')
    st.pyplot(fig)

    # Count the number of patients with each disease
    diabetes_count = filtered_df['Diabetes'].sum()
    hypertension_count = filtered_df['Hipertension'].sum()
    alcoholism_count = filtered_df['Alcoholism'].sum()
    handicap_count = filtered_df['Handcap'].sum()
    total_patients = len(filtered_df)

    # Display the counts as cards
    st.subheader('Diseases Information')
    st.write(f"Total Patients: {total_patients}")
    st.write(f"Patients with Diabetes: {diabetes_count}")
    st.write(f"Patients with Hypertension: {hypertension_count}")
    st.write(f"Patients with Alcoholism: {alcoholism_count}")
    st.write(f"Patients with Handicap: {handicap_count}")


elif selected_analysis == "Appointment day difference VS No Show":
    st.subheader('Appointment day difference VS No Show')

    # Convert 'AppointmentDay' and 'ScheduledDay' to datetime type
    filtered_df['AppointmentDay'] = pd.to_datetime(filtered_df['AppointmentDay'])
    filtered_df['ScheduledDay'] = pd.to_datetime(filtered_df['ScheduledDay'])

    # Check the data types and missing values before calculating the difference
    st.write(filtered_df[['AppointmentDay', 'ScheduledDay']].dtypes)
    st.write(filtered_df[['AppointmentDay', 'ScheduledDay']].isnull().sum())

    # Drop rows with missing values in 'AppointmentDay' or 'ScheduledDay'
    filtered_df.dropna(subset=['AppointmentDay', 'ScheduledDay'], inplace=True)

    # Calculate the difference between AppointmentDay and ScheduledDay
    filtered_df['Appointment_Scheduled_Difference'] = (filtered_df['AppointmentDay'] - filtered_df['ScheduledDay']).dt.days

    # Define the mapping for y-tick labels
    no_show_mapping = {'Yes': 'No Show', 'No': 'Showed Up'}

    # Plot the relationship between the difference and no-show
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=filtered_df, x='Appointment_Scheduled_Difference', y='No-show', estimator=None, ax=ax, palette=bar_palette)
    
    ax.set_xlabel('Appointment Day - Scheduled Day Difference (Days)')
    ax.set_ylabel('No Show')
    ax.set_yticks([0, 1])  # Set y-ticks to correspond to the 'No-show' values
    ax.set_yticklabels([no_show_mapping[val] for val in ax.get_yticks()])
    ax.set_title('Appointment day difference VS No Show')
    # Add labels to specific points on the plot
    for i, row in filtered_df.iterrows():
        ax.text(row['Appointment_Scheduled_Difference'], 0 if row['No-show'] == 'No' else 1, row['No-show'], color='black', ha='center', va='bottom')

    st.pyplot(fig)


else:
    st.error("Please select a valid analysis from the dropdown.")
