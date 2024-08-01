import os
import pandas as pd

from dotenv import load_dotenv

from flask import request, Flask, jsonify

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from langchain_openai import ChatOpenAI

load_dotenv()

gpt35 = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0
)

data_file = "dataset_43718.pq"
bank_data = pd.read_parquet(data_file)

pandas_agent = create_pandas_dataframe_agent(
    llm=gpt35,
    df=bank_data,
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True
)

dataframe_agent_api = Flask("DataFrame Agent")

@dataframe_agent_api.get('/')
def home():
    return 'Welcome to the DataFrame Agent'

@dataframe_agent_api.post('/v1/input')
def predict():

   user_input = request.get_data(as_text=True)

   try:
       response = pandas_agent.invoke(user_input)

       prediction = response['output']

   except Exception as e:
       prediction = e
        
   return jsonify({'output': prediction})

if __name__ == '__main__':
    dataframe_agent_api.run(debug=True, host='0.0.0.0', port=8000)