import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Flow
from crewai.flow.flow import listen, start
from src.daily_updates_urls_finder import daily_updates_finder, daily_updates_task, DailyUpdatesUrls
from src.daily_updates_scraper import daily_updates_scraper_agent, daily_updates_scrape_task, DailyUpdates, DailyUpdatesList
from src.daily_updates_podcaster import podcast_agent, podcast_task
from src.database import Database
import streamlit as st

load_dotenv()

class DailyUpdatesFlow(Flow):    
    @start()
    def find_daily_updates(self):  
        db = Database()   
        username = st.session_state["username"]
        u_id = db.get_user_id(username)
        custom_urls = db.get_user_custom_urls(u_id)

        daily_updates_finding_crew = Crew(
            agents=[daily_updates_finder], 
            tasks=[daily_updates_task]
        )

        if st.session_state["use_saved_urls"]:
            urls_list = [url[0] for url in custom_urls]
            daily_updates_urls = DailyUpdatesUrls(urls=urls_list)
        else:
            result = daily_updates_finding_crew.kickoff()
            daily_updates_urls = DailyUpdatesUrls(urls=result["urls"])

        udu_id = db.create_daily_update(u_id, reference_urls=daily_updates_urls.urls)
        st.session_state["udu_id"] = udu_id
        st.session_state["u_id"] = u_id
        return daily_updates_urls
    
    @listen(find_daily_updates)
    def scrape_daily_updates(self, daily_updates_urls):
        db = Database()   
        daily_updates_scraping_crew = Crew(
            agents=[daily_updates_scraper_agent], 
            tasks=[daily_updates_scrape_task]
        )

        daily_updates_urls = ", ".join(daily_updates_urls.urls)
        result = daily_updates_scraping_crew.kickoff(inputs={"urls": daily_updates_urls})
        daily_updates_list = DailyUpdatesList(updates=result["updates"])

        if daily_updates_list and daily_updates_list.updates and len(daily_updates_list.updates) > 0:
            udu_id = st.session_state["udu_id"]

            for update in daily_updates_list.updates:
                db.create_daily_update_scrapes(udu_id, update.title, update.summary, update.url)

            return daily_updates_list
        else:
            u_id = st.session_state["u_id"]
            db.delete_daily_update(udu_id, u_id)
            st.warning("No daily updates found. Please try again later.")
            return None
    
    @listen(scrape_daily_updates)
    def convert_to_podcast(self, daily_updates_list):
        if daily_updates_list and daily_updates_list.updates and len(daily_updates_list.updates) > 0:
            db = Database()   
            podcast_crew = Crew(
                agents=[podcast_agent], 
                tasks=[podcast_task]
            )
            
            contents = ""   
            for update in daily_updates_list.updates:
                contents += f"{update.title}\n{update.summary}\n\n"

            result = podcast_crew.kickoff(inputs={"contents": contents})

            audio_filename = result["audio_filename"]
            udu_id = st.session_state["udu_id"]
            db.update_audio_filename(udu_id, audio_filename)

            return result
        else:
            st.warning("No daily updates found. Please try again later.")
            return None

def get_content(use_saved_urls=False):
    st.session_state["use_saved_urls"] = use_saved_urls
    flow = DailyUpdatesFlow()
    result = flow.kickoff()  
    return result

if __name__ == "__main__":
    st.session_state["username"] = "bnarasimha21@gmail.com"
    get_content()



