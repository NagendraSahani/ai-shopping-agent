from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.tools.tavily_tool import TavilyTool
from app.tools.serpapi_tool import SerpAPITool
from app.tools.extractor_tool import ExtractorTool
from app.tools.compare_tool import CompareTool
from app.tools.review_tool import ReviewTool


class AgentState(TypedDict):

    query: str

    tavily_result: dict

    serpapi_result: dict

    products: list

    best_product: dict

    review: str

    final_result: dict


class ShoppingAgent:

    def tavily_node(
        self,
        state: AgentState,
    ):

        tool = TavilyTool()

        state["tavily_result"] = tool.search(
            state["query"]
        )

        return state

    def serpapi_node(
        self,
        state: AgentState,
    ):

        tool = SerpAPITool()

        state["serpapi_result"] = tool.search(
            state["query"]
        )

        return state

    def extract_node(
        self,
        state: AgentState,
    ):

        state["products"] = ExtractorTool.extract(
            state["serpapi_result"]
        )

        return state

    def compare_node(
        self,
        state: AgentState,
    ):

        state["best_product"] = CompareTool.compare(
            state["products"]
        )

        return state

    def review_node(
        self,
        state: AgentState,
    ):

        state["review"] = ReviewTool.summarize(
            state["products"]
        )

        return state

    def final_node(
        self,
        state: AgentState,
    ):

        state["final_result"] = {

            "query": state["query"],

            "best_product": state["best_product"],

            "all_products": state["products"],

            "review": state["review"],

            "sources": state["tavily_result"],

        }

        return state

    def build(self):

        graph = StateGraph(
            AgentState
        )

        graph.add_node(
            "tavily",
            self.tavily_node,
        )

        graph.add_node(
            "serpapi",
            self.serpapi_node,
        )

        graph.add_node(
            "extract",
            self.extract_node,
        )

        graph.add_node(
            "compare",
            self.compare_node,
        )

        graph.add_node(
            "review",
            self.review_node,
        )

        graph.add_node(
            "final",
            self.final_node,
        )

        graph.set_entry_point(
            "tavily"
        )

        graph.add_edge(
            "tavily",
            "serpapi",
        )

        graph.add_edge(
            "serpapi",
            "extract",
        )

        graph.add_edge(
            "extract",
            "compare",
        )

        graph.add_edge(
            "compare",
            "review",
        )

        graph.add_edge(
            "review",
            "final",
        )

        graph.add_edge(
            "final",
            END,
        )

        return graph.compile()