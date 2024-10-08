import asyncio

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI

from config import settings

from tools.block_height import block_height_tool
from tools.current_epoch import current_epoch_info_tool
from tools.account_info import account_info_tool
from tools.account_balance import account_balance_tool
from tools.supply import supply_tool
from tools.token_supply import token_supply_tool
from tools.token_largest_accounts import token_largest_accounts_tool
from tools.search_token_by_name import search_token_by_name_tool
from tools.account_tokens import account_tokens_tool


tools = [
    block_height_tool,
    current_epoch_info_tool,
    account_info_tool,
    account_balance_tool,
    supply_tool,
    token_supply_tool,
    token_largest_accounts_tool,
    search_token_by_name_tool,
    account_tokens_tool,
]

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model="gpt-4o",
    temperature=0,
)

prompt = hub.pull("hwchase17/structured-chat-agent")

agent = create_structured_chat_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

agent_strachpad = """
If user asks about balance return in sol. 1 solana = 1000000000 lamports.
Always convert lamports to solana.
"""

async def run_agent(question: str) -> str:
    response = await agent_executor.ainvoke(
        {
            "input": question,
            "agent_strachpad": agent_strachpad,
        }
    )
    return response["output"]

async def main():
    # question = "What balance of the account 6nXwxdCx9efetSx2d3ZC6ZBSsNsc3HyVpaQodXrwYRVL in sol?"
    question = "What is the current supply?"
    response = await run_agent(question)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
