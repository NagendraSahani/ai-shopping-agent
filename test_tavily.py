from app.tools.tavily_tool import TavilyTool

tool = TavilyTool()

result = tool.search(
    "Best laptop under 60000 India"
)

print(result)