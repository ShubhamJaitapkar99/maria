from crewai import Task, Crew, Process
from typing import List
from agents.content_agents import (
    get_content_strategist,
    get_visual_director,
    get_leonardo_expert
)
from agents.research_agents import get_market_researcher

def create_content_generation_tasks(
    business_idea: str,
    target_audience: str,
    brand_style: str
) -> List[Task]:
    """Create tasks for content generation"""
    
    market_researcher = get_market_researcher()
    content_strategist = get_content_strategist()
    visual_director = get_visual_director()
    leonardo_expert = get_leonardo_expert()
    
    research_task = Task(
        description=f"""Research current marketing trends and successful campaigns for:
        Business: '{business_idea}'
        Target: '{target_audience}'
        Style: '{brand_style}'
        
        1. Analyze top-performing social media content in this niche
        2. Identify visual trends that drive engagement
        3. Study successful competitor campaigns
        4. Note specific imagery styles that resonate with the audience
        5. Research color schemes and visual elements that perform well""",
        agent=market_researcher,
        expected_output="A detailed market research report with trends and recommendations"
    )

    strategy_task = Task(
        description="""Using the market research, develop a content concept that:
        1. Aligns with current trends
        2. Reflects brand values
        3. Appeals to target audience
        4. Has viral potential
        5. Can be executed well by AI""",
        agent=content_strategist,
        expected_output="A comprehensive content strategy with visual concepts"
    )

    visual_task = Task(
        description="""Create a detailed visual concept optimized for Leonardo.ai that includes:
        1. Scene composition and framing
        2. Lighting setup and atmosphere
        3. Human subject details (if included)
        4. Environment and prop specifics
        5. Color grading and post-processing style""",
        agent=visual_director,
        expected_output="A detailed visual direction document"
    )

    prompt_task = Task(
        description="""Create a hyper-optimized Leonardo.ai prompt using the visual concept.
        Must include quality terms, camera details, lighting setup, and technical specifications.
        Format as:
        PROMPT: "detailed prompt"
        NEGATIVE: "negative prompt" """,
        agent=leonardo_expert,
        expected_output="A formatted Leonardo.ai prompt with main and negative prompts"
    )

    return [research_task, strategy_task, visual_task, prompt_task]

def create_content_crew(tasks: List[Task]) -> Crew:
    """Create a crew for content generation"""
    return Crew(
        agents=[
            get_market_researcher(),
            get_content_strategist(),
            get_visual_director(),
            get_leonardo_expert()
        ],
        tasks=tasks,
        process=Process.sequential
    )