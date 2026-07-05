from fastapi import APIRouter

from app.agents.shopping_agent import ShoppingAgent

router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"],
)

agent = ShoppingAgent().build()


@router.post("/shopping")
def shopping_agent(query: str):

    result = agent.invoke(
        {
            "query": query
        }
    )

    return result["final_result"]