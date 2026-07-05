from app.tools.serpapi_tool import SerpAPITool

tool = SerpAPITool()

result = tool.search(
    "Best laptop under 60000"
)

print(result)