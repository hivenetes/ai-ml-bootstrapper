import os
from dotenv import load_dotenv
from crewai import Crew, Flow
from crewai.flow.flow import listen, start
from product_research import product_researcher, product_research_task
from competitor_research import competitor_analyst, competitor_research_task
from comparison_report import comparison_analyst, comparison_research_task
import streamlit as st

load_dotenv()

class MarketResearchAssistant(Flow):
    @start()
    def get_product_narsi_info(self):  
        product_research_crew = Crew(
            agents=[product_researcher], 
            tasks=[product_research_task]
        )

        result = product_research_crew.kickoff()
        return result
    
    @listen(get_product_narsi_info)
    def get_competitor_info(self):
        competitor_research_crew = Crew(
            agents=[competitor_analyst], 
            tasks=[competitor_research_task]
        )

        my_product = st.session_state.get("my_product")
        competitor1 = st.session_state.get("competitor1")
        competitor2 = st.session_state.get("competitor2") 

        result = competitor_research_crew.kickoff(inputs={"my_product": my_product, "competitor1": competitor1, "competitor2": competitor2})
        return result

    @listen(get_competitor_info)
    def get_comparison_info(self):
        comparison_research_crew = Crew(
            agents=[comparison_analyst], 
            tasks=[comparison_research_task]
        )

        result = comparison_research_crew.kickoff()
        return result

if __name__ == "__main__":
    flow = MarketResearchAssistant()
    result = flow.kickoff()  
    print(result)