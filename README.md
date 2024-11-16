# Marketing Artificial Intelligence Assistant

## Overview

The Marketing Artificial Intelligence Assistant is a comprehensive end-to-end solution designed to empower marketing strategies using AI. This project includes multiple AI-powered agents to assist with market research, content creation, social media strategy development, and asset generation such as images and videos.

## Features

- **AI Influencer**: Engage with AI-powered influencers to enhance social media presence.
- **Market Research Agent**: Gather and analyze market data to guide business decisions.
- **Content Creation Agent**: Automatically generate written content for blogs, websites, and marketing materials.
- **Social Media Strategy Agent**: Develop data-driven social media strategies for businesses.
- **Assets Generation Agent**: Create high-quality assets such as images and videos for marketing purposes.

## Setup

To get started with the project, follow the steps below:

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/ShubhamJaitapkar99/maria
cd maria
```

2. Create a Virtual Environment
   
Create a virtual environment named env to isolate your project dependencies:
```bash
python -m venv env
```

3. Activate the Virtual Environment

On Windows:
```bash
.\env\Scripts\activate
```
On macOS/Linux:
```bash
source env/bin/activate
```

4. Install Dependencies
Install the required dependencies for the project:

```
pip install -r requirements.txt
```

5. Setup of API keys
You will have to generate your own API keys for the below,
1. Runway
2. OpenAI
3. Leonardo
4. Serper
5. Akool

Refer to the .env.example file in the repository and create a .env file with your specific configuration values.

7. Running the Project
Once your environment is set up, you can run the project by executing:

```
streamlit run main.py
```
This will start the application, and you can interact with the various AI agents to assist with marketing tasks.

