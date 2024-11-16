from crewai import Agent
from config import search_tool

def get_creative_director() -> Agent:
    return Agent(
        role='Creative Director',
        goal='Create compelling visual concepts optimized for Leonardo.ai generation',
        backstory="""You are a creative director with expertise in visual storytelling 
        and photorealistic image generation. You excel at creating concepts that leverage 
        Leonardo.ai's strengths in realistic photography, cinematic imagery, and 
        high-detail compositions.""",
        verbose=True,
        llm_model="gpt-4"
    )

def get_visual_prompt_expert() -> Agent:
    return Agent(
        role='Leonardo.ai Prompt Expert',
        goal='Create highly optimized prompts for Leonardo.ai image generation',
        backstory="""You are a prompt engineering expert specialized in Leonardo.ai's 
        image generation capabilities. You understand how to craft prompts that maximize 
        photorealism, lighting, and composition while avoiding common AI artifacts.""",
        verbose=True,
        llm_model="gpt-4"
    )

def get_content_strategist() -> Agent:
    return Agent(
        role='Content Strategy Expert',
        goal='Develop engaging content concepts based on market research',
        backstory="""Senior content strategist with expertise in creating viral social 
        media campaigns. You understand how to translate brand values into visually 
        compelling content that resonates with target audiences.""",
        verbose=True,
        llm_model="gpt-4"
    )

def get_visual_director() -> Agent:
    return Agent(
        role='Visual Creative Director',
        goal='Create detailed visual concepts optimized for Leonardo.ai generation',
        backstory="""Expert visual director specializing in commercial photography and 
        social media content. You excel at creating concepts that leverage Leonardo.ai's 
        strengths in photorealistic imagery while maintaining brand authenticity.""",
        verbose=True,
        llm_model="gpt-4"
    )

def get_leonardo_expert() -> Agent:
    return Agent(
        role='Leonardo.ai Expert',
        goal='Optimize prompts for hyper-realistic marketing imagery',
        backstory="""Leonardo.ai specialist with deep understanding of model capabilities. 
        You excel at creating prompts that generate consistent, professional marketing 
        content with human subjects and lifestyle imagery.""",
        verbose=True,
        llm_model="gpt-4"
    )