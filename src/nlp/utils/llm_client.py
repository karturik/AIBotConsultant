import os
import openai
import httpx
from langchain_openai import ChatOpenAI

from src.core.config import OPENAI_API_KEY, PROXY_URL

proxies = httpx.Proxy(url=PROXY_URL)

http_client = httpx.AsyncClient(proxy=proxies)

mini_model = ChatOpenAI(
    model_name='gpt-4o-mini',
    max_retries=3,
    api_key=OPENAI_API_KEY,
    http_async_client=http_client
    )

main_model = ChatOpenAI(
    model_name='gpt-4o',
    max_retries=3,
    api_key=OPENAI_API_KEY,
    http_async_client=http_client
    )
