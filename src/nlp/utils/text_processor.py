from .llm_client import mini_model, main_model
from .chat_templates import PromptTemplates as PT


async def clear_message(user_message: str) -> str:
    prompt = PT.clear_message.invoke(user_message)
    response = await mini_model.ainvoke(prompt)
    return response.content

async def rephrase_message(user_message: str) -> str:
    prompt = PT.rephrase_message.invoke(user_message)
    response = await mini_model.ainvoke(prompt)
    return response.content