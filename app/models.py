import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ---------------- TOOLS ---------------- #
# We keep the tools simple so they can't fail.
@tool
def football_tool(query: str):
    """Answers questions about Football (Soccer)."""
    return "Football fact: The first World Cup was held in 1930 in Uruguay."

@tool
def basketball_tool(query: str):
    """Answers questions about Basketball."""
    return "Basketball fact: The game was invented by Dr. James Naismith in 1891."

@tool
def tennis_tool(query: str):
    """Answers questions about Tennis."""
    return "Tennis fact: The yellow tennis balls were first used at Wimbledon in 1986."

@tool
def cricket_tool(query: str):
    """Answers questions about Cricket."""
    return "Cricket fact: The longest cricket match lasted over 9 days in 1939."

tools = [football_tool, basketball_tool, tennis_tool, cricket_tool]

# ---------------- LOGIC ---------------- #
def run_ai_logic(user_input: str):
    try:
        # 1. Setup the Model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        ).bind_tools(tools)

        # 2. Define the Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized sports assistant. Use your tools for Football, Basketball, Tennis, and Cricket. If a question is about any other sport or topic, politely say you only support those four sports."),
            ("human", "{input}")
        ])

        # 3. Create and Invoke the Chain
        chain = prompt | llm
        response = chain.invoke({"input": user_input})

        # 4. Handle Tool Calls
        if response.tool_calls:
            results = []
            for tool_call in response.tool_calls:
                # Find the matching tool from our list
                selected_tool = next(t for t in tools if t.name == tool_call["name"])
                # Run the tool and get the result
                tool_output = selected_tool.invoke(tool_call["args"])
                results.append(str(tool_output))
            return " ".join(results)

        # 5. Handle Text Responses
        return str(response.content)

    except Exception as e:
        # This will print the EXACT error in your terminal
        print(f"\n❌ CRITICAL ERROR IN MODELS.PY: {str(e)}\n")
        return f"Backend Error: {str(e)}"