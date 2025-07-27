import asyncio
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from pathlib import Path
import os

from browser_use.llm import ChatOpenAI
from browser_use import Agent, BrowserSession, Controller, ActionResult

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Configure the browser session
browser_session = BrowserSession(
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    user_data_dir='~/.config/browseruse/profiles/default',
    headless=False,  # Set to True to run without opening browser window
    viewport={'width': 964, 'height': 647},
)



controller = Controller()

@controller.action('Upload file to interactive element with file path')
async def upload_file(index: int, path: str, browser_session: BrowserSession, available_file_paths: list[str]):
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')

	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist')

	file_upload_dom_el = await browser_session.find_file_upload_element_by_index(index, max_height=3, max_descendant_depth=3)

	if file_upload_dom_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	file_upload_el = await browser_session.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file to index {index}'
		return ActionResult(extracted_content=msg, include_in_memory=True)
	except Exception as e:
		msg = f'Failed to upload file to index {index}: {str(e)}'
		return ActionResult(error=msg)
	
def create_file(file_type: str = 'txt'):
	with open(f'tmp.{file_type}', 'w') as f:
		f.write('test')
	file_path = Path.cwd() / f'tmp.{file_type}'
	return str(file_path)


# Load LLM
llm = ChatOpenAI(model="gpt-4.1")


# sensitive_data = {
#     'https://app.collarup.ai/auth': {
#         'x_username': 'rajivsingh9624@gmail.com',
#         'x_password': 'Test@123',
#     }
# }

task = """
1. add the candidate details in the form with name 'Sarthak Shah' email test@qa.com message 'Hello' upload the file subject 'Automation'
2. click on the submit button and wait to open a alter box
3. click on ok
"""

# Main function
async def main():
    initial_actions = [
        {'go_to_url': {'url': 'https://www.automationexercise.com/contact_us'}}
    ]
    available_file_paths = [create_file('pdf')]
    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser_session,
        controller=controller,
        initial_actions=initial_actions,
        # sensitive_data=sensitive_data
		available_file_paths=available_file_paths
    )

    # Run the agent
    result = await agent.run()

    # Parse the result from JSON string to dict
    # raw_json = result.final_result()
    action_finished = result.is_done()


    if not action_finished:
        print('Action not finished')



    # Clean up the browser session
    await browser_session.kill()

    # Print output

# Run it
asyncio.run(main())
