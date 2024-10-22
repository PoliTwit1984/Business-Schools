import pandas as pd
from openai import OpenAI
import os
from time import sleep
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Perplexity API key
API_KEY = "pplx-08b9af382e82aca32d846c90695abca4dfeb18f39fbba6dajoey"

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Read the CSV file
df = pd.read_csv('SchoolsD1.csv')

# Print column names
print("CSV Columns:", df.columns.tolist())

def get_university_name(team_name, state):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about universities and their sports teams."
        },
        {
            "role": "user",
            "content": f"What is the full name of the college or university associated with the team '{team_name}' in the state of {state}? Please respond with only the full name of the university."
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error making API call for team {team_name}: {str(e)}")
        return f"Error: Unable to determine university for {team_name}"

def get_school_info(school_name, state):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about business programs at universities."
        },
        {
            "role": "user",
            "content": f"Provide information about the business school or program at {school_name} in {state}. Include the name of the business school and any notable details about the school. Format your response as: 'Business School: [Name of Business School]\nNotable Details: [Details about the school]'"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error making API call for {school_name}: {str(e)}")
        return f"Error: Unable to retrieve information for {school_name}"

def process_schools(df):
    for index, row in df.iterrows():
        # Use .get() method to avoid KeyError if column doesn't exist
        team = row.get('team', row.get('Team', 'Unknown Team'))
        state = row.get('state', row.get('State', 'Unknown State'))
        
        logging.info(f"Processing team: {team}")
        
        # Get university name
        university = get_university_name(team, state)
        logging.info(f"Determined university: {university}")
        
        # Get business school information
        info = get_school_info(university, state)
        
        # Write to file after each school is processed
        with open('SchoolsD1_processed.txt', 'a') as f:
            f.write(f"Team: {team}\nUniversity: {university}\nState: {state}\n")
            f.write(f"{info}\n\n")
        
        logging.info(f"Updated data saved for {university}")
        
        sleep(1)  # To avoid hitting rate limits

# Process the schools and create the new file
logging.info("Starting to process schools")
process_schools(df)

logging.info("Processing complete. Data saved to SchoolsD1_processed.txt")

# Print the first few lines of the new file
with open('SchoolsD1_processed.txt', 'r') as f:
    print(f.read(500))  # Print first 500 characters
