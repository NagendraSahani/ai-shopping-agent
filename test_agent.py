from app.agents.shopping_agent import ShoppingAgent

agent = ShoppingAgent().build()

result = agent.invoke(
    {
        "query": "Best Laptop under 60000"
    }
)

print(result["final_result"])