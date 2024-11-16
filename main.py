import streamlit as st
from datetime import datetime
import time
import logging
from openai import OpenAI
from runwayml import RunwayML
import requests
from crewai import Crew, Process
import os

# Import local modules
from config import DEFAULT_SESSION_STATE
from services.leonardo import LeonardoAI
from tasks.content_tasks import create_content_generation_tasks, create_content_crew
from tasks.research_tasks import create_research_tasks, create_research_crew
from tasks.video_tasks import create_video_prompt_task, create_video_crew
logging.getLogger('opentelemetry').setLevel(logging.ERROR)

# Initialize clients
client = OpenAI()
client_runway = RunwayML()
content_leonardo_client = LeonardoAI(os.environ["LEONARDO_CONTENT_API_KEY"])
leonardo_client = LeonardoAI(os.environ["LEONARDO_API_KEY"])

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

def handle_content_generation(business_idea: str, target_audience: str, brand_style: str):
    """Handle the content generation process"""
    # Create tasks and crew
    tasks = create_content_generation_tasks(business_idea, target_audience, brand_style)
    crew = create_content_crew(tasks)
    
    # Run the crew
    result = crew.kickoff()
    
    # Extract the prompt
    leonardo_prompt = extract_leonardo_prompt(result)
    
    if leonardo_prompt:
        generate_and_display_content(leonardo_prompt, business_idea)

def extract_leonardo_prompt(result) -> str:
    """Extract Leonardo.ai prompt from crew result"""
    leonardo_prompt = ""
    if hasattr(result, 'raw'):
        for task_output in result.tasks_output:
            if 'PROMPT:' in task_output.raw:
                leonardo_prompt = task_output.raw.split('PROMPT:')[1].split('NEGATIVE:')[0].strip().strip('"')
                break
        
        if not leonardo_prompt:
            leonardo_prompt = result.tasks_output[-1].raw.strip()
            leonardo_prompt = f"8k resolution, award winning photography, professional photograph, {leonardo_prompt}"
    
    return leonardo_prompt

def generate_and_display_content(prompt: str, business_idea: str):
    """Generate and display content using Leonardo.ai"""
    try:
        with st.spinner("Generating marketing image with Leonardo.ai..."):
            prompt_text = clean_prompt(prompt)
            response = content_leonardo_client.generate_marketing_image(prompt_text)
            
            if "url" in response:
                handle_successful_generation(response, prompt)
            else:
                st.error(f"Error generating image: {response.get('error', 'Unknown error')}")
                if 'details' in response:
                    st.write("Error details:", response['details'])

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        st.write("Debug - Exception details:", str(e))

def clean_prompt(prompt: str) -> str:
    """Clean and format the prompt for Leonardo.ai"""
    if "PROMPT:" in prompt:
        prompt_text = prompt.split("PROMPT:")[1].split("NEGATIVE:")[0].strip().strip('"')
    else:
        prompt_text = prompt.strip()
    
    if not any(term in prompt_text.lower() for term in ["8k", "award winning", "professional"]):
        prompt_text = f"8k resolution, award winning photography, professional photograph, {prompt_text}"
    
    if len(prompt_text) > 500:
        prompt_text = prompt_text[:500]
    
    return prompt_text

def handle_successful_generation(response: dict, prompt: str):
    """Handle successful image generation"""
    image_url = response["url"]
    if image_url:
        st.session_state.generated_image_url = image_url
        st.session_state.dalle_prompt = prompt
        st.session_state.generated_content.append({
            'type': 'image',
            'url': image_url,
            'description': "Marketing Content",
            'prompt': prompt,
            'created_at': datetime.now().isoformat()
        })
        
        display_generated_content(image_url, response, prompt)

def display_generated_content(image_url: str, response: dict, prompt: str):
    """Display generated content and debug information"""
    st.success("Your Instagram marketing content has been generated!")
    st.image(image_url, caption="Generated Marketing Content")
    st.markdown(f"[Download Image]({image_url})")
    
    with st.expander("Debug Info"):
        st.write("Content added to session state:")
        st.write(st.session_state.generated_content[-1])
    
    with st.expander("Generation Details"):
        st.write("Prompt:", prompt)
        st.write("Model ID:", response.get('modelId'))
        st.write("Seed:", response.get('seed'))

def handle_video_generation(business_idea: str):
    """Handle video generation process"""
    if not st.session_state.generated_image_url:
        return
    
    st.markdown("---")
    st.subheader("Video Generation")
    
    if st.button("Generate Video from Image"):
        task = create_video_prompt_task(
            business_idea, 
            st.session_state.dalle_prompt
        )
        crew = create_video_crew(task)
        generate_video(crew)

def generate_video(crew: Crew):
    """Generate video using RunwayML"""
    try:
        prompt_result = crew.kickoff()
        video_prompt = extract_video_prompt(prompt_result)
        
        if video_prompt:
            st.info(f"Generated video prompt: {video_prompt}")
            process_video_generation(video_prompt)
    except Exception as e:
        st.error(f"Error generating video: {str(e)}")

def extract_video_prompt(result) -> str:
    """Extract video prompt from crew result"""
    if hasattr(result, 'raw'):
        if 'VIDEO_PROMPT:' in result.raw:
            return result.raw.split('VIDEO_PROMPT:')[1].strip().strip('"')
    return ""

def process_video_generation(video_prompt: str):
    """Process video generation with RunwayML"""
    with st.spinner("Generating video..."):
        if len(video_prompt) > 520:
            st.error("Video prompt is too long. Must be under 520 characters.")
            return
        
        generate_runway_video(video_prompt)

def generate_runway_video(prompt: str):
    """Generate video using RunwayML"""
    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        try:
            response = client_runway.image_to_video.create(
                model='gen3a_turbo',
                prompt_image=st.session_state.generated_image_url,
                prompt_text=prompt
            )
            success = True
            handle_runway_response(response, prompt)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Failed after {max_retries} attempts: {str(e)}")
            else:
                time.sleep(5 * (attempt + 1))

def handle_runway_response(response, prompt: str):
    """Handle RunwayML video generation response"""
    if hasattr(response, 'id'):
        progress_bar = st.progress(0)
        status_text = st.empty()
        monitor_video_generation(response.id, progress_bar, status_text, prompt)

def monitor_video_generation(task_id: str, progress_bar, status_text, prompt: str):
    """Monitor video generation progress"""
    max_attempts = 60
    attempts = 0
    
    while attempts < max_attempts:
        try:
            status_response = client_runway.tasks.retrieve(id=task_id)
            if status_response.status == "SUCCEEDED":
                handle_successful_video(status_response.output[0], prompt)
                break
            elif status_response.status == "FAILED":
                handle_failed_video(status_response)
                break
            elif status_response.status in ["PENDING", "RUNNING"]:
                update_progress(status_response, progress_bar, status_text)
        except Exception as e:
            st.error(f"Error checking status: {str(e)}")
        
        time.sleep(5)
        attempts += 1
    
    if attempts >= max_attempts:
        st.error("Video generation timed out. Please try again.")

def handle_successful_video(video_url: str, prompt: str):
    """Handle successful video generation"""
    st.session_state.generated_content.append({
        'type': 'video',
        'url': video_url,
        'description': "Marketing Video",
        'prompt': prompt,
        'created_at': datetime.now().isoformat()
    })
    
    st.session_state.video_generated = True
    st.success("Video generated successfully!")
    st.video(video_url)
    st.markdown(f"[Download Video]({video_url})")

def handle_failed_video(status_response):
    """Handle failed video generation"""
    st.error(f"Video generation failed: {status_response.failure}")
    if status_response.failure_code == "INTERNAL.BAD_OUTPUT.CODE01":
        st.error("The input image or prompt may be causing issues. Try a different prompt or image.")

def update_progress(status_response, progress_bar, status_text):
    """Update video generation progress"""
    progress = getattr(status_response, 'progress', 0)
    progress_bar.progress(progress)
    status_text.text(f"Processing video... {int(progress * 100)}%")


def show_ai_influencer_tab():
    """Display AI influencer tab"""
    st.title("AI Influencer Generator")
    
    with st.form("influencer_form"):
        brand_style = st.text_area("Describe your brand style:")
        target_audience = st.text_input("Describe your target audience:")
        num_photos = st.slider("Number of photos to generate", 1, 5, 3)
        submit_button = st.form_submit_button("Generate Influencer")
        
    if submit_button and brand_style and target_audience:
        try:
            with st.spinner("Creating your AI influencer..."):
                tasks = create_content_generation_tasks(brand_style, target_audience, brand_style)
                crew = create_content_crew(tasks)
                result = crew.kickoff()
                
                prompts = result.tasks_output[1].raw.split("PROMPT:")
                st.subheader("Generated Images")
                cols = st.columns(3)
                
                for i in range(num_photos):
                    with cols[i % 3]:
                        with st.spinner(f"Generating photo {i+1}..."):
                            response = leonardo_client.generate_image(prompts[0])
                            if "url" in response:
                                image_url = response["url"]
                                if image_url:
                                    st.image(image_url, caption=f"Photo {i+1}")
                                    try:
                                        image_response = requests.get(image_url)
                                        if image_response.status_code == 200:
                                            st.download_button(
                                                f"Download Photo {i+1}",
                                                data=image_response.content,
                                                file_name=f"influencer_photo_{i+1}.jpg",
                                                mime="image/jpeg"
                                            )
                                            st.session_state.generated_content.append({
                                                'type': 'image',
                                                'url': image_url,
                                                'description': f"AI Influencer Photo {i+1}",
                                                'prompt': prompts[0],
                                                'created_at': datetime.now().isoformat()
                                            })
                                    except Exception as e:
                                        st.error(f"Error downloading image: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
def show_content_generation_tab():
    """Display content generation tab"""
    st.title("Website Asset Generator")
    
    with st.form("content_form"):
        business_idea = st.text_area("Describe your business idea:")
        target_audience = st.text_input("Describe your target audience:")
        brand_style = st.text_input("Describe your brand style:")
        submit_button = st.form_submit_button("Generate Assets")
    
    if submit_button and business_idea and target_audience:
        handle_content_generation(business_idea, target_audience, brand_style)
        handle_video_generation(business_idea)

def show_market_research_tab():
    """Display market research tab"""
    st.title("Market Research & Strategy")
    
    business_name = st.text_input("Enter your business name:")
    business_stage = st.selectbox(
        "Select your business stage:",
        ["Startup/New Idea", "Early Stage Business", "Established Business", "Enterprise"]
    )
    industry = st.text_input("Enter your industry:")
    target_market = st.text_input("Describe your target market:")
    
    if business_name and st.button("Analyze Market & Create Strategy"):
        handle_market_research(business_name, business_stage, industry, target_market)

def handle_market_research(business_name: str, business_stage: str, industry: str, target_market: str):
    """Handle market research process"""
    with st.spinner("Analyzing market and creating strategy..."):
        try:
            tasks = create_research_tasks(business_name, business_stage, industry, target_market)
            crew = create_research_crew(tasks)
            result = crew.kickoff()
            
            display_research_results(result)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Debug - Error details:", str(e))

def display_research_results(result):
    """Display market research results"""
    st.markdown("---")
    
    results_tab1, results_tab2, results_tab3 = st.tabs([
        "📊 Market Research",
        "📱 Social Media Strategy",
        "📈 Business Plan"
    ])
    
    with results_tab1:
        st.markdown("### Market Research Insights")
        st.markdown(result.tasks_output[0].raw)
    
    with results_tab2:
        st.markdown("### Social Media Strategy")
        st.markdown(result.tasks_output[1].raw)
    
    with results_tab3:
        st.markdown("### Business Plan")
        st.markdown(result.tasks_output[2].raw)

def show_content_manager_tab():
    """Display content manager tab"""
    st.title("Content Manager")
    
    with st.expander("Debug Session State"):
        st.write("Number of items in generated_content:", len(st.session_state.generated_content))
        st.write("All session state keys:", st.session_state.keys())
        st.write("Content items:", st.session_state.generated_content)
    
    display_content_grid()

def display_content_grid():
    """Display content in a grid layout"""
    col1, col2 = st.columns(2)
    with col1:
        content_type = st.selectbox(
            "Filter by type",
            ["All", "Images", "Videos", "Marketing Plans", "AI Influencer"]
        )
    with col2:
        date_range = st.date_input(
            "Date range",
            value=(datetime.now(), datetime.now())
        )
    
    display_filtered_content(content_type)

def display_filtered_content(content_type: str):
    """Display filtered content"""
    if not st.session_state.generated_content:
        st.info("No content generated yet. Generate some content in other tabs to see it here!")
        return
    
    filtered_content = filter_content(content_type)
    display_content_items(filtered_content)

def filter_content(content_type: str):
    """Filter content based on type"""
    if content_type == "All":
        return st.session_state.generated_content
    return [
        item for item in st.session_state.generated_content 
        if item['type'].lower() == content_type.lower()
    ]

def main():
    initialize_session_state()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Content Generation",
        "Market Research & Strategy",
        "AI Influencer",
        "Content Manager"
    ])
    
    with tab1:
        show_content_generation_tab()
    
    with tab2:
        show_market_research_tab()
    
    with tab3:
        show_ai_influencer_tab()
    
    with tab4:
        show_content_manager_tab()

if __name__ == "__main__":
    main()