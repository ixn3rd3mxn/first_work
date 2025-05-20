from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from newsapi import NewsApiClient

news_api = NewsApiClient(api_key='xxx')

@tool
def search_news(query: str) -> str:
    """Search for news articles based on a query term."""
    try:
        response = news_api.get_everything(q=query)
        articles = response.get('articles', [])
        if not articles:
            return f"No news articles found for query: {query}"
        result = f"Top news articles for '{query}':\n"
        for idx, article in enumerate(articles, 1):
            result += f"{idx}. {article['title']} - {article['source']['name']} ({article['publishedAt'][:10]})\n"
        return result
    except Exception as e:
        return f"Error fetching news: {str(e)}"

tools = [search_news]

print()
print(tools)
print()

base_url = "xxx"
api_key = "xxx"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    base_url=base_url
)

print(llm)
print()

llm_with_tools = llm.bind_tools(tools)

print(llm_with_tools)
print()

prompt = "Ayo sir, i need to read murder news, can you help me to find this news topic?"

result = llm_with_tools.invoke(prompt)

print(result)
print()

if hasattr(result, 'tool_calls') and result.tool_calls:
    for tool_call in result.tool_calls:
        if tool_call['name'] == 'search_news':
            query = tool_call['args']['query']
            news_result = search_news.invoke({"query": query})
            print(news_result)