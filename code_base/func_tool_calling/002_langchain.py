from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage, ToolMessage
# from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

@tool
def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def fake_weather_api(city: str) -> str:
    """Check the weather in a specified city."""
    return "Sunny, 22°C"

@tool
def outdoor_seating_availability(city: str) -> str:
    """Check if outdoor seating is available at a specified restaurant in a given city."""
    return "Outdoor seating is available."

tools = [fake_weather_api, outdoor_seating_availability, add_two_numbers]

base_url = "xxx"
api_key = "xxx"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    base_url=base_url
    )

prompt = "hello how are you sir? How will the weather be in munich today? I would like to eat outside if possible and i think 1+1=?"

# result = llm.invoke(prompt)

# print(result)

llm_with_tools = llm.bind_tools(tools)

result = llm_with_tools.invoke(prompt)

print(result)
