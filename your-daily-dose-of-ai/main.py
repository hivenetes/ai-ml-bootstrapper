import streamlit as st
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.daily_updates_urls_finder import daily_updates_finder, daily_updates_task
from src.database import Database
from src.get_daily_updates import get_content
load_dotenv()

def get_audio_files():
    """Get list of audio files with their metadata"""
    audio_dir = "audio_files"
    audio_files = []
    
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith(('.mp3', '.wav', '.ogg')):
                file_path = os.path.join(audio_dir, file)
                try:
                    # Split filename parts (format: YYYY-MM-DD_HH-MM-SS_email_type.mp3)
                    parts = file.split('_')
                    date_str = parts[0]  # YYYY-MM-DD
                    time_str = parts[1]  # HH-MM-SS
                    email = parts[2]     # email address
                    type_str = parts[3].split('.')[0]  # type (custom/daily)
                    
                    # Parse datetime
                    date_time = datetime.strptime(f"{date_str}_{time_str}", '%Y-%m-%d_%H-%M-%S')
                    
                    audio_files.append({
                        'date': date_time,
                        'email': email,
                        'type': type_str,
                        'filename': file,
                        'path': file_path
                    })
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue
    
    # Sort files by date (newest first)
    return sorted(audio_files, key=lambda x: x['date'], reverse=True)

def main():
    st.title("Your Daily Dose of AI")
    
    # Initialize database
    db = Database()
    username = st.session_state.get("username")
    db.add_user(username)  # This will do nothing if user already exists
    u_id = db.get_user_id(username)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🎧 Listen AI Doses", "➕ Create New AI Dose", "⚙️ Manage AI Doses"])
    
    # Tab 1: Listen to Podcasts
    with tab1:
        st.write("")
        
        # Get updates from database
        updates = db.get_user_daily_updates(u_id)

        if not updates:
            st.warning("No audio files found.")
        else:
            # Group updates by date
            if updates:                
                # Display each update in table format
                for udu_id, reference_urls, audio_filename, created_at in updates:
                    if audio_filename and os.path.exists(os.path.join("audio_files", audio_filename)):
                        # Ensure created_at is a datetime object
                        if isinstance(created_at, str):
                            created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                        
                        # Extract type from filename (custom/daily)
                        file_type = audio_filename.split('_')[3].split('.')[0]
                        
                        st.subheader(created_at.date())

                        with st.container():
                            col1, col2, col3 = st.columns([2, 1, 2])
                            with col1:
                                st.write(created_at.strftime('%Y-%m-%d %H:%M:%S'))
                            with col2:
                                st.write(file_type.capitalize())
                            with col3:
                                st.audio(os.path.join("audio_files", audio_filename))
                            
                        st.divider()
            else:
                st.warning("No audio files found.")

    # Tab 2: Create New AI Dose
    with tab2:
        st.header("Create Today's AI Dose", divider=True)
        st.write("System automatically creates audio file from today's updates searching the web.")
        if st.button("🎙️ Create Today's AI Dose", type="primary", use_container_width=True):
            with st.spinner('Creating today\'s AI Dose...'):
                result = get_content(use_saved_urls=False)
                if result:
                    st.success("Today's AI Dose created successfully!")
                else:
                    st.error("Failed to create AI Dose")

        st.write("")
        st.write("")

        # Section 2: Create from Saved URLs
        st.header("Create AI Dose from Saved URLs", divider=True)
        st.write("System automatically creates audio file from saved URLs. You can add any URL to this list by entering the URL and clicking Add URL button. Finally click the 'Create AI Dose from Saved URLs' below to continue.")

        st.subheader("Add Custom URL")
        new_url = st.text_input("Enter URL to include in AI dose:", placeholder="https://example.com")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Add URL", use_container_width=True):
                if new_url:
                    db.add_user_custom_urls(u_id, new_url)
                    st.rerun()
                else:
                    st.warning("Please enter a valid URL")
        
        # Display saved URLs
        urls = db.get_user_custom_urls(u_id)
        if urls:
            for url in urls:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(url[0])  # url is a tuple, get first element
                with col2:
                    if st.button("Delete", key=url[0]):
                        db.delete_user_custom_urls(u_id, url[0])
                        st.rerun()
            
            # Add some space before the button
            st.write("")
            
            # Create Podcast from Saved URLs button
            if st.button("📑 Create AI Dose from Saved URLs", type="primary", use_container_width=True):
                with st.spinner('Creating AI Dose from saved URLs...'):
                    result = get_content(use_saved_urls=True)
                    if result:
                        st.success("AI Dose from saved URLs created successfully!")
                    else:
                        st.error("Failed to create AI Dose")
        else:
            st.info("No custom URLs added yet")
        
        st.write("")
        st.write("")

    # Tab 3: Manage AI Doses
    with tab3:
        st.header("Manage AI Doses")
        
        daily_updates =  db.get_user_daily_updates(u_id)
        if not daily_updates:
            st.warning("No daily updates found.")
            return
                
        # Sort files by date (newest first)
        daily_updates.sort(key=lambda x: x[3], reverse=True)
        
        # Display files in a table format
        for udu_id, reference_urls, audio_filename, created_at in daily_updates:
            if not audio_filename:
                continue
                
            audio_path = os.path.join("audio_files", audio_filename)
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                
                with col1:
                    st.write(created_at.strftime('%Y-%m-%d'))
                with col2:
                    st.write(created_at.strftime('%H:%M:%S'))
                with col3:
                    st.audio(audio_path)
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_btn_{udu_id}"):
                        try:
                            if db.delete_daily_update(udu_id, u_id):
                                
                                if os.path.exists(audio_path):
                                    os.remove(audio_path)
                                st.success("Record deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete record")
                        except Exception as e:
                            st.error(f"Error deleting record: {e}")
                
                st.divider()

if __name__ == "__main__":
    st.session_state["username"] = "bnarasimha21@gmail.com"
    main()
