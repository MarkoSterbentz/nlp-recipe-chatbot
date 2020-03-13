from rasa.core.channels.slack import SlackInput
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.utils.endpoints import EndpointConfig

# Replace <model_directory> with your models directory
nlu_interpreter = RasaNLUInterpreter('./models/model/nlu')
# Load agent with created models and connect to action server endpoint, replace <action_server_endpoint> with your endpoint
agent = Agent.load('./models/model', interpreter = nlu_interpreter, 
action_endpoint = EndpointConfig(url='http://localhost:5005/webhook'))

input_channel = SlackInput(
    # this is the `bot_user_o_auth_access_token`
    slack_token="xoxb-994655275015-992801903680-jqB9xEbzEcAU3bBIdoF0c470",
    # slack_channel="#general"
    # the name of your channel to which the bot posts (optional)
    )

s = agent.handle_channels([input_channel], 5004)