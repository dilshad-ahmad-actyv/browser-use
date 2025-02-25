import streamlit as st
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set event loop policy for Windows (Fix Playwright issue)
if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Streamlit UI
st.title("Epiplex Chat Agent")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Ensure 'input' key exists before using it
if "input" not in st.session_state:
    st.session_state["input"] = ""

async def run_agent(task):
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,
    )
    result = await agent.run()
    return result

# Input field for user
user_input = st.text_input("How may I assist you: ", key="input")

if st.button("Ask"):
    if user_input:
        st.write("Processing...")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(run_agent(user_input))

        # Store in session state to keep history
        st.session_state.conversation.append((user_input, response))

        # # Clear input field using experimental rerun
        # st.session_state["input"] = ""  
        st.rerun()  # Ensures UI refreshes properly

# Display conversation history
st.write("### Conversation History:")
for question, answer in st.session_state.conversation:
    st.write(f"**Q:** {question}")
    st.write(f"**A:** {answer}")
    st.write("---")
