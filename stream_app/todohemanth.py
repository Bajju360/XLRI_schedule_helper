import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re

st.header('Hemanth')
today = datetime.now().strftime("%d-%m-%Y")

# Get the directory where this script is located
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "schedule_hemanth.csv")

# Initialize session state for dataframe
if 'my_dataframe' not in st.session_state:
    try:
        st.session_state.my_dataframe = pd.read_csv(csv_path, header=None)
    except FileNotFoundError:
        st.error(f"CSV file 'schedule_hemanth.csv' not found at {csv_path}. Please make sure the file exists in the same directory as the script.")
        st.stop()
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        st.stop()
else:
    st.session_state.my_dataframe = pd.read_csv(csv_path, header=None)

my_dataframe = st.session_state.my_dataframe

# Function to parse the schedule data
def parse_schedule_data(df):
    parsed_data = []
    
    for index, row in df.iterrows():
        if pd.isna(row[0]) or row[0] == '':
            continue
            
        # Split the first column by semicolon
        parts = str(row[0]).split(';')
        
        if len(parts) >= 4:
            # Extract date, time, and priority from the first part
            datetime_priority = parts[0].strip()
            
            # Use regex to extract date, time, and priority
            # Pattern: DD-MM-YY HH.MM AM/PM (PRIORITY)
            match = re.match(r'(\d{2}-\d{2}-\d{2})\s+(\d{2}\.\d{2}\s+[AP]M)\s+\(([^)]+)\)', datetime_priority)
            
            if match:
                date = match.group(1)
                time = match.group(2)
                priority = match.group(3)
                topic = parts[1].strip() if len(parts) > 1 else ''
                professor = parts[2].strip() if len(parts) > 2 else ''
                lecture_hall = parts[3].strip() if len(parts) > 3 else ''
                
                # Set time required based on priority
                time_required = 90 if priority in ['ABCD', 'A', 'B'] else 0
                
                parsed_data.append({
                    'Date': date,
                    'Time': time,
                    'Time Required': time_required,
                    'Priority': priority,
                    'Topic': topic
                })
    
    return pd.DataFrame(parsed_data)

# Function to sort dataframe by date and time
def sort_dataframe_by_datetime(df):
    """Sort dataframe by date and time extracted from the first column"""
    if df.empty:
        return df
    
    # Create a temporary dataframe for sorting
    temp_data = []
    for index, row in df.iterrows():
        if pd.isna(row[0]) or row[0] == '':
            continue
        
        # Extract date and time from the first column
        datetime_str = str(row[0]).split(';')[0].strip()
        match = re.match(r'(\d{2}-\d{2}-\d{2})\s+(\d{2}\.\d{2}\s+[AP]M)', datetime_str)
        
        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            
            # Convert to datetime for sorting
            try:
                # Parse date (DD-MM-YY format)
                day, month, year = date_str.split('-')
                year = '20' + year  # Convert YY to YYYY
                
                # Parse time (HH.MM AM/PM format)
                time_part, ampm = time_str.split(' ')
                hour, minute = time_part.split('.')
                hour = int(hour)
                minute = int(minute)
                
                # Convert to 24-hour format
                if ampm == 'PM' and hour != 12:
                    hour += 12
                elif ampm == 'AM' and hour == 12:
                    hour = 0
                
                # Create datetime object
                dt = datetime(int(year), int(month), int(day), hour, minute)
                
                temp_data.append({
                    'original_row': row[0],
                    'datetime': dt
                })
            except:
                # If parsing fails, use a default datetime
                temp_data.append({
                    'original_row': row[0],
                    'datetime': datetime(1900, 1, 1)
                })
    
    # Sort by datetime
    temp_data.sort(key=lambda x: x['datetime'])
    
    # Create new sorted dataframe
    sorted_rows = [item['original_row'] for item in temp_data]
    sorted_df = pd.DataFrame(sorted_rows, columns=df.columns)
    
    return sorted_df

# Function to insert a row at the correct sorted position
def insert_row_sorted(df, new_entry):
    """Insert a new entry at the correct chronological position"""
    if df.empty:
        return pd.DataFrame([[new_entry]], columns=df.columns)
    
    # Extract date and time from the new entry
    datetime_str = new_entry.split(';')[0].strip()
    match = re.match(r'(\d{2}-\d{2}-\d{2})\s+(\d{2}\.\d{2}\s+[AP]M)', datetime_str)
    
    if not match:
        # If parsing fails, append to the end
        return pd.concat([df, pd.DataFrame([[new_entry]], columns=df.columns)], ignore_index=True)
    
    date_str = match.group(1)
    time_str = match.group(2)
    
    # Convert to datetime for comparison
    try:
        day, month, year = date_str.split('-')
        year = '20' + year
        
        time_part, ampm = time_str.split(' ')
        hour, minute = time_part.split('.')
        hour = int(hour)
        minute = int(minute)
        
        if ampm == 'PM' and hour != 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0
        
        new_dt = datetime(int(year), int(month), int(day), hour, minute)
    except:
        # If parsing fails, append to the end
        return pd.concat([df, pd.DataFrame([[new_entry]], columns=df.columns)], ignore_index=True)
    
    # Find the correct insertion position
    insert_index = 0
    for index, row in df.iterrows():
        if pd.isna(row[0]) or row[0] == '':
            continue
        
        # Extract date and time from existing row
        existing_datetime_str = str(row[0]).split(';')[0].strip()
        existing_match = re.match(r'(\d{2}-\d{2}-\d{2})\s+(\d{2}\.\d{2}\s+[AP]M)', existing_datetime_str)
        
        if existing_match:
            existing_date_str = existing_match.group(1)
            existing_time_str = existing_match.group(2)
            
            try:
                day, month, year = existing_date_str.split('-')
                year = '20' + year
                
                time_part, ampm = existing_time_str.split(' ')
                hour, minute = time_part.split('.')
                hour = int(hour)
                minute = int(minute)
                
                if ampm == 'PM' and hour != 12:
                    hour += 12
                elif ampm == 'AM' and hour == 12:
                    hour = 0
                
                existing_dt = datetime(int(year), int(month), int(day), hour, minute)
                
                # Compare datetimes
                if new_dt < existing_dt:
                    break
                else:
                    insert_index = index + 1
            except:
                insert_index = index + 1
    
    # Insert the new row at the correct position
    df_list = df.values.tolist()
    df_list.insert(insert_index, [new_entry])
    
    return pd.DataFrame(df_list, columns=df.columns)

# Sort the original dataframe
my_dataframe = sort_dataframe_by_datetime(my_dataframe)

# ===== INPUT PROCESSING SECTION (TOP PRIORITY) =====

# Create dropdown options
today_dt = datetime.now()
date_options = []
for i in range(3650):  # 10 years * 365 days
    date = today_dt + timedelta(days=i)
    date_options.append(date.strftime("%d-%m-%y"))

# Time dropdown - 15 minutes gap
time_options = []
for hour in range(24):
    for minute in [0, 15, 30, 45]:
        time_str = f"{hour:02d}.{minute:02d}"
        if hour < 12:
            time_options.append(f"{time_str} AM")
        else:
            time_options.append(f"{time_str} PM")

# Time required dropdown - 0 to 300 in 15-minute increments
time_required_options = list(range(0, 301, 15))

# Topic dropdown
topic_options = ["Assignment", "Gym", "Other"]

# Input form - PROCESS FIRST
st.subheader("Add New Entries")
with st.form("add_entry_form"):
    st.write("Add a new entry:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.selectbox("Date", date_options, index=0)
        selected_time = st.selectbox("Time", time_options, index=48)  # Default to 12:00 PM
    
    with col2:
        selected_time_required = st.selectbox("Time Required (minutes)", time_required_options, index=6)  # Default to 90 minutes
        selected_topic = st.selectbox("Topic", topic_options, index=0)
    
    # Submit button
    submitted = st.form_submit_button("Add Entry")
    
    if submitted:
        # Format the entry in the original CSV format with default priority ABCDE
        formatted_entry = f"{selected_date} {selected_time} (ABCDE);{selected_topic};;"
        
        # Insert the new entry at the correct sorted position
        my_dataframe = insert_row_sorted(my_dataframe, formatted_entry)
        
        # Update session state
        st.session_state.my_dataframe = my_dataframe
        
        # Save the updated dataframe back to CSV file
        try:
            my_dataframe.to_csv(csv_path, index=False, header=False)
            st.success(f"Added new entry: {selected_date} {selected_time} - {selected_topic}")
            
            # Re-parse the data after adding entry
            st.session_state.parsed_df = parse_schedule_data(my_dataframe)
            
        except Exception as e:
            st.error(f"Error saving to CSV: {str(e)}")

# Legacy text area method - PROCESS SECOND
st.subheader("Add Multiple Entries (Legacy Method)")
st.write("Enter new entries in the format: DD-MM-YY HH.MM AM/PM (PRIORITY);TOPIC;PROFESSOR;LECTURE_HALL")
st.write("Example: 15-08-25 02.45 PM (ABCD);MSTBJ24-4;Indrajit Mukherjee;LC2/L.H. 16")

# Text area for multiple entries
new_entries_text = st.text_area(
    "Enter new entries (one per line):",
    height=150,
    placeholder="15-08-25 02.45 PM (ABCD);MSTBJ24-4;Indrajit Mukherjee;LC2/L.H. 16\n16-08-25 06.30 PM (B);GTMBJ24-4;Sumit Sarkar;LC2/L.H. 17"
)

# Button to add entries
if st.button("Add Entries"):
    if new_entries_text.strip():
        # Parse new entries
        lines = new_entries_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line:
                # Normalize the line: replace tabs with semicolons and ensure proper format
                line = line.replace('\t', ';')
                # Ensure we have at least 4 semicolons for proper format
                parts = line.split(';')
                if len(parts) < 4:
                    # Pad with empty strings if needed
                    line = line + ';' * (4 - len(parts))
                
                # Insert the new entry at the correct sorted position
                my_dataframe = insert_row_sorted(my_dataframe, line)
        
        # Update session state
        st.session_state.my_dataframe = my_dataframe
        
        # Save the updated dataframe back to CSV file
        try:
            my_dataframe.to_csv(csv_path, index=False, header=False)
            st.success(f"Added {len(lines)} new entries successfully!")
            
            # Re-parse the data after adding entries
            st.session_state.parsed_df = parse_schedule_data(my_dataframe)
            
            # Force refresh of the display by rerunning
            st.rerun()
            
        except Exception as e:
            st.error(f"Error saving to CSV: {str(e)}")
    else:
        st.warning("Please enter at least one entry.")

# ===== DATA PROCESSING SECTION =====

# Parse the data AFTER input processing - use my_dataframe which is always updated
parsed_df = parse_schedule_data(my_dataframe)
st.session_state.parsed_df = parsed_df

# ===== DISPLAY SECTION =====

# Create all_filtered_df from my_dataframe which is always updated
all_parsed_df = parse_schedule_data(my_dataframe)
all_filtered_df = all_parsed_df[all_parsed_df['Priority'].isin(['ABCD', 'B', 'ABCDE'])]

# Filter to show only ABCD, B, ABC, or ABCDE priority
if not parsed_df.empty and 'Priority' in parsed_df.columns:
    filtered_df = parsed_df[parsed_df['Priority'].isin(['ABCD', 'B', 'ABCDE'])]
    
    # Filter to show only today and tomorrow's entries
    today_str = datetime.now().strftime("%d-%m-%y")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%y")
    
    if 'Date' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['Date'] == today_str) | (filtered_df['Date'] == tomorrow_str)]
else:
    filtered_df = pd.DataFrame()  # Empty DataFrame if no data

# Ensure filtered_df is a DataFrame
filtered_df = pd.DataFrame(filtered_df) if not isinstance(filtered_df, pd.DataFrame) else filtered_df

# Display the parsed data
if not filtered_df.empty:
    st.subheader(f"Today & Tomorrow's Schedule (ABCD, B, and ABCDE Priority)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Show some statistics
    st.subheader("Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Entries (ABCD, B & ABCDE)", len(filtered_df))
    
    with col2:
        # Convert to list and count unique values, handling any NaN values
        topics_list = filtered_df['Topic'].tolist()
        unique_topics = len(set([topic for topic in topics_list if pd.notna(topic) and topic != '']))
        st.metric("Unique Topics", unique_topics)
    
    # Show all values from CSV in same format
    st.subheader("All Values from CSV File (ABCD, B, and ABCDE Priority)")
    st.dataframe(all_filtered_df, use_container_width=True)
        
else:
    st.error("No valid schedule data found in the CSV file.")