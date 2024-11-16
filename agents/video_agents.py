from crewai import Agent
from config import search_tool

def get_video_prompt_agent() -> Agent:
    return Agent(
        role='Video Motion Expert',
        goal='Create compelling video motion prompts following Runway guidelines',
        backstory="""You are an expert in creating video motion prompts that bring static images 
        to life. You understand Runway's Gen-3 Alpha model capabilities and follow their 
        prompting best practices.""",
        verbose=True
    )

def get_runway_researcher() -> Agent:
    return Agent(
        role='Runway Documentation Expert',
        goal='Research and master Runway Gen-3 Alpha prompting best practices',
        backstory="""You are a technical documentation expert specializing in AI video generation. 
        You have extensively studied Runway's Gen-3 Alpha model and understand all its capabilities 
        and limitations. You focus on creating cinematic, hyper-realistic motion effects.""",
        tools=[search_tool],
        verbose=True,
        llm_model="gpt-4"
    )