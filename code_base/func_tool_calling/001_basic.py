from openai import OpenAI
import json

def add_two_numbers(a: int, b: int) -> int:
    return a + b

available_functions = {
    'add_two_numbers': add_two_numbers,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first integer number"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second integer number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]

system_prompt = """**When responding to a user's request, please follow these guidelines:**

1. **Analyze the request:** Determine if the user is asking for a calculation that requires adding two numbers. Look for phrases like "add", "sum", "calculate", etc.

2. **Call the tool when necessary:** If the user's request needs to add two numbers, call the `add_two_numbers` function.

3. **Structure the function call:** Provide the necessary parameters in a JSON object, like this:

```json
{{
    "name": "add_two_numbers",
    "arguments": {{
        "a": <first_number>,
        "b": <second_number>
    }}
}}
tools :
{tool}
"""

tool_json = json.dumps(tools[0], indent=4)
system_prompt = system_prompt.format(tool=tool_json)

print("System prompt:")
print(system_prompt)

base_url = "http://111.223.37.51/v1"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjcyMDAzOTkuMDU5LCJkYXRhIjp7Im9yZ2FuaXphdGlvbl9pZCI6IjY2ZjE3ZjRlNzdjZTg0ZDM5ZWE0MTQ0YSIsInRva2VuX25hbWUiOiIxOTIuMTY4LjEwLjk0In0sImlhdCI6MTcyNzEwMjk5OH0.uM47lcykCkhK9yaf3gnpzJEg1T27r6Z2Cq6Lvley3qA"

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

user_query = "What your name"
print(f"\nUser query: {user_query}")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ],
    tools=tools,
    tool_choice="auto"
)

print("\nAPI response:", response.choices[0].message.content or "[calculate detect, using tool]")

if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
    for tool in response.choices[0].message.tool_calls:
        function_name = tool.function.name
        function_to_call = available_functions.get(function_name)
        
        if function_to_call:
            args = json.loads(tool.function.arguments)
            print(f"\nTool call arguments: {args}")
            
            result = function_to_call(**args)
            print(f"Function output: {result} (from {function_name})")
            
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool.id,
                                "type": "function",
                                "function": {
                                    "name": function_name,
                                    "arguments": tool.function.arguments
                                }
                            }
                        ]
                    },
                    {
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "content": str(result)
                    },
                    {
                        "role": "user",
                        "content": f"Answer my question with summary of this\nResult from Tools: {result}\nin conversations form"
                    }
                ]
            )
            print("\nFinal AI response:", second_response.choices[0].message.content)
        else:
            print(f"Function not found: {function_name}")