import os
import openai
import httpx
from langchain_openai import ChatOpenAI

from src.core.config import OPENAI_API_KEY

proxy_headers = {
    'http://': os.environ["PROXY_URL"],
    'https://': os.environ["PROXY_URL"]
}

http_client = httpx.AsyncClient(proxies=proxy_headers)
proxed_openai_client = openai.AsyncOpenAI(
    base_url="https://api.openai.com/v1", 
    api_key=OPENAI_API_KEY, 
    http_client=http_client
)

mini_model = ChatOpenAI(
    model_name='gpt-4o-mini',
    max_retries=3,
    api_key=OPENAI_API_KEY,
    http_client=http_client
    )

main_model = ChatOpenAI(
    model_name='gpt-4o',
    max_retries=3,
    api_key=OPENAI_API_KEY,
    http_client=http_client
    )
