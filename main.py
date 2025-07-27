import asyncio
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

from browser_use.llm import ChatOpenAI
from browser_use import Agent, BrowserSession, Controller

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Configure the browser session
browser_session = BrowserSession(
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    user_data_dir='~/.config/browseruse/profiles/default',
    headless=False,  # Set to True to run without opening browser window
    viewport={'width': 964, 'height': 647},
)

# Define the output models


# Controller for single candidate
controller = Controller()


# Load LLM
llm = ChatOpenAI(model="gpt-4.1")


task = """
1. add the  details in the form with firstname 'Sarthak Shah' email test@qa.com comment 'Hello' phone 9292929292 gender male yearofExperience 2 skill Functional testing in other details hello
2. click on the submit button 
"""

# Main function
async def main():
    initial_actions = [
        {'go_to_url': {'url': 'https://qavalidation.com/demo-form/?contact-form-hash=875a4285a37d67e2416c29f39cb2425c0d8d255c'}}
    ]

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser_session,
        # controller=controller,
        initial_actions=initial_actions,
        # sensitive_data=sensitive_data
    )

    # Run the agent
    await agent.run()

    # Clean up the browser session
    await browser_session.kill()

    # Print output
    # print(info)

# Run it
asyncio.run(main())
