from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from prompts import analyst_prompt, architect_prompt, developer_prompt, reviewer_prompt, tester_prompt, diagram_creator_prompt, summarizer_prompt

load_dotenv()


class AgentState(TypedDict):
  messages: Annotated[list, add_messages]

llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=1000, temperature=0.6)

builder = StateGraph(AgentState)

def create_node(state: AgentState, system_prompt) -> AgentState:
  aimesg = [msg for msg in state['messages'] if isinstance(msg, AIMessage)]
  humanmsg = [msg for msg in state['messages'] if isinstance(msg, HumanMessage)]
  sysmsg = [SystemMessage(content=system_prompt)]

  message = sysmsg + humanmsg + aimesg
  response = llm.invoke(message)
  return {"messages": response.content}

# All function for Nodes
analyst = lambda state: create_node(state, analyst_prompt)
architech = lambda state: create_node(state, architect_prompt)
developer = lambda state: create_node(state, developer_prompt)
reviewer = lambda state: create_node(state, reviewer_prompt)
tester = lambda state: create_node(state, tester_prompt)
diagram_creator = lambda state: create_node(state, diagram_creator_prompt)
summarizer = lambda state: create_node(state, summarizer_prompt)

# Create Node
builder.add_node('Analyst', analyst)
builder.add_node("Architech", architech)
builder.add_node("Developer", developer)
builder.add_node("Reviewer", reviewer)
builder.add_node("Tester", tester)
builder.add_node("Diagram Creator", diagram_creator)
builder.add_node("Summarizer", summarizer)

# Create Edges
builder.add_edge(START, 'Analyst')
builder.add_edge('Analyst', 'Architech')
builder.add_edge('Architech', 'Developer')
builder.add_edge('Developer', 'Reviewer')
builder.add_edge('Reviewer', 'Tester')
builder.add_edge('Tester', 'Diagram Creator')
builder.add_edge('Diagram Creator', 'Summarizer')
builder.add_edge('Summarizer', END)

# Create graph
graph = builder.compile()

try:
  graph.get_graph().draw_mermaid_png(output_file_path="aget_graph.png")
except Exception as e:
  print(f'Error generating graph: {e}')
  

# Create main loop
def main_loop():
  while True:
    user_input = input("Enter Query: ")
    if user_input.lower() in ['q', 'quit', 'exit']:
      break
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]})
    print("Analyst", result['messages'][-7].content, "\n")
    print("Architech", result['messages'][-6].content, "\n")
    print("Developer", result['messages'][-5].content, "\n")
    print("Reviewer", result['messages'][-4].content, "\n")
    print("Tester", result['messages'][-3].content, "\n")
    print("Diagram Creator", result['messages'][-2].content, "\n")
    print("Summarizer", result['messages'][-1].content, "\n")


if __name__ == "__main__":
  main_loop()

  