from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from core.config import settings

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, AnyMessage, HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun


# Define LangGraph State
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# Define LangGraph Agent
class Agent_Firefly:
    """Searching agent using LLMs and tools."""
    def __init__(self, tools):
        """Initialize the agent with necessary components."""
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE,
            temperature=0.7,
        )
        self.tools = tools

        self.llm_with_tools = self.llm.bind_tools(tools)
        
        # The graph
        builder = StateGraph(AgentState)
        
        
        # Define nodes: these do the work
        builder.add_node("assistant", self.run_agent_logic)
        builder.add_node("tools", ToolNode(self.tools))

        # Define edges: these determine how the control flow moves
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            # If the latest message requires a tool, route to tools
            # Otherwise, provide a direct response
            tools_condition,
        )
        builder.add_edge("tools", "assistant")
        
        # Graph compile
        self.graph = builder.compile()

    async def run_agent_logic(self, state: AgentState):
        """LLM을 호출하여 다음 행동을 결정하는 핵심 로직"""
        # 현재까지의 대화 기록을 LLM에 전달
        response = await self.llm.ainvoke(state["messages"])
        # LLM의 응답을 상태(messages)에 추가하여 반환
        return {"messages": [response]}

    # async def invoke(self, session_id: str, prompt: str, history: list[BaseMessage]):
    async def invoke(self, session_id: str, prompt: str):
        """
        에이전트를 실행하고, 구조화된 결과를 반환합니다.
        
        :param session_id: 대화의 고유 ID (LangGraph 메모리에 사용)
        :param prompt: 사용자의 현재 입력
        :param history: DB에서 가져온 이전 대화 기록
        """
        # LangGraph를 실행할 때 필요한 입력 데이터 구성
        input_data = {"messages": [HumanMessage(content=prompt)]}
        
        # 세션별로 대화 상태를 유지하기 위해 'configurable' 사용
        config = {"configurable": {"thread_id": session_id}}
        
        # 비동기적으로 그래프 실행
        response_graph = await self.graph.ainvoke(input_data, config=config)
        
        # 마지막 AI 응답 메시지를 가져옴
        last_message_content = response_graph["messages"][-1].content
        
        # # LLM 응답 파싱 (예: "action:attack|text:공격합니다!")
        # action = "idle"
        # response_text = last_message_content
        
        # try:
        #     parts = {p.split(':', 1)[0]: p.split(':', 1)[1] for p in last_message_content.split('|')}
        #     action = parts.get("action", "idle")
        #     response_text = parts.get("text", last_message_content)
        # except Exception:
        #     # 파싱 실패 시 기본값 사용
        #     pass

        # return {"action": action, "response_text": response_text}
        response_text = last_message_content
        return {"response_text": response_text}

# 다른 파일에서 이 인스턴스를 가져다 사용합니다.
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]
agent_instance = Agent_Firefly(tools=tools)