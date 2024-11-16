from crewai import Task, Crew, Process
from typing import List
from agents.research_agents import (
    get_market_researcher, get_business_planner,
    get_social_media_strategist
)

def create_research_tasks(
    business_name: str,
    business_stage: str,
    industry: str,
    target_market: str
) -> List[Task]:
    """Create tasks for market research and strategy"""
    
    market_research_task = Task(
        description=f"""Conduct targeted market research for {business_name} with scale-appropriate analysis:
        Business Context:
        - Name: {business_name}
        - Stage: {business_stage}
        - Industry: {industry}
        - Target: {target_market}
        
        Analyze:
        1. Market Size & Growth
        2. Competitive Analysis
        3. Target Audience
        4. Market Trends""",
        agent=get_market_researcher(),
        expected_output=f"A detailed market analysis report for {business_name}"
    )

    strategy_task = Task(
        description=f"""Develop a social media strategy based on the market research for {business_name}.
        Include:
        1. Platform Strategy
        2. Content Strategy
        3. Engagement Plan
        4. Growth Strategy""",
        agent=get_social_media_strategist(),
        expected_output=f"A social media strategy for {business_name}"
    )

    business_plan_task = Task(
        description=f"""Create a practical business plan for {business_name} focused on:
        1. Executive Summary
        2. Financial Projections
        3. Implementation Timeline
        4. Risk Analysis""",
        agent=get_business_planner(),
        expected_output=f"A business plan for {business_name}"
    )

    return [market_research_task, strategy_task, business_plan_task]

def create_research_crew(tasks: List[Task]) -> Crew:
    """Create a crew for market research"""
    return Crew(
        agents=[
            get_market_researcher(),
            get_social_media_strategist(),
            get_business_planner()
        ],
        tasks=tasks,
        verbose=True,
        process=Process.sequential
    )