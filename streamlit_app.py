__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent
# from tools import yt_tool
# from dotenv import load_dotenv
from crewai import LLM
import litellm
import openai
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool
import streamlit as st

load_dotenv()

# Title
st.set_page_config(page_title="EducatorAI", layout="wide")

# Title and description
st.title("AI Educator Powered By CrewAI")
st.markdown("Please provide a text file only")

# Sidebar
with st.sidebar:
    st.header("Content Settings")

    topic = st.text_area(
        "Enter the topic",
        height=68,
        placeholder="Enter the topic",
        key="text_area_1"
    )

    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

def generate_content(topic):
        # Create a {topic} Tag Researcher
        researcher = Agent(
            role='{topic} Tag Researcher',
            goal='Generate quirky and attractive taglines for {topic} that are creative, engaging, and memorable.',
            description='Scrape the PDF documents to extract information related to {topic}.',
            verbose=True,
            memory=True,
            backstory=(
                "Act as a creative branding expert and generate quirky, engaging, and memorable taglines for {topic} "
                "that capture attention and leave a lasting impact."
            ),
            allow_delegation=True,
        )

        # Create a {topic} Writer Agent
        reporting_analyst = Agent(
            role='{topic} Writer Agent',
            goal='The writer\'s role is to craft quirky, engaging, and memorable taglines for {topic}, ensuring they are creative, attention-grabbing, and aligned with the brand\'s identity and message.',
            description='Write the scraped content from the researcher and display the findings in a report format.',
            verbose=True,
            memory=True,
            backstory=(
                "To craft quirky, engaging, and memorable taglines for {topic}, ensuring they effectively capture attention, "
                "reflect the brand’s personality, and leave a lasting impact on the audience."
            ),
            allow_delegation=True,
            tools=[FileWriterTool()]
        )

        research_task = Task(
            description=(
                "To conduct thorough research and generate a collection of unique, quirky, and engaging taglines for {topic} "
                "that are fresh, impactful, and aligned with the brand’s identity. The researcher must avoid repetition and "
                "ensure originality while maintaining high creative standards."
            ),
            expected_output='To generate 10 quirky, attractive, interesting lines for t-shirt branding.',
            agent=researcher,
        )

        reporting_task = Task(
            description=(
                "Review the researched content and write down the 10 best taglines that can be printed on the t-shirt which best explains the {topic}."
            ),
            expected_output='A refined set of fresh, impactful, and standout taglines that effectively communicate the {topic} and leave a lasting impression on the audience. Write the 10 lines researched.',
            agent=reporting_analyst,
            output_file='report.txt'
        )

        # Crew
        crew = Crew(
            agents=[researcher, reporting_analyst],
            tasks=[research_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff(inputs={"topic": topic})

# Main content area
if generate_button:
    with st.spinner("Generating Content...This may take a moment.."):
        try:
            result = generate_content(topic, uploaded_file)
            if result:
                st.markdown("### Generated Content")
                st.markdown(result)

                # Add download button
                st.download_button(
                    label="Download Content",
                    data=result.raw,
                    file_name=f"article.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("----")
st.markdown("Built by AritraM")
