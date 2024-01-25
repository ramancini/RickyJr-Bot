import database_fns as dbf
import datetime

import os
from openai import OpenAI
from dotenv import load_dotenv

# # Create a database operations object
# db = dbf.DatabaseOperations()

# # Try getting a non-existent message log
# print(db.get_message_log(123456789))

# # Add a message log
# db.add_message(123456789, datetime.datetime.now(), 'user', 'Hello World!')

# # Get the message log
# print(db.get_message_log(123456789))

# # Clear the message log
# db.clear_message_log(123456789)

load_dotenv(dotenv_path='data/.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)