from crewai import Task, Crew, Process
from agents.video_agents import get_video_prompt_agent

def create_video_prompt_task(business_idea: str, original_prompt: str) -> Task:
    """Create task for video prompt generation"""
    return Task(
        description=f"""Create a cinematic video motion prompt (MAXIMUM 450 characters) that 
        emphasizes hyper-realism:

        Business Idea: '{business_idea}'
        Original Image: Generated from '{original_prompt}'
        
        REQUIREMENTS:
        1. Use professional cinematography terms
        2. Specify exact camera movements
        3. Include lighting transitions
        4. Add atmospheric effects
        5. Keep under 450 characters(strictly!!!)
        
        Format: VIDEO_PROMPT: "your cinematic prompt here" """,
        agent=get_video_prompt_agent(),
        expected_output="A cinematic video generation prompt under 450 characters"
    )

def create_video_crew(task: Task) -> Crew:
    """Create a crew for video generation"""
    return Crew(
        agents=[get_video_prompt_agent()],
        tasks=[task],
        process=Process.sequential
    )