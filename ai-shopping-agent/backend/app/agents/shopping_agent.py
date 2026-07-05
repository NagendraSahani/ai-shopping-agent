from typing import TypedDict
import json
from app.tools.recommendation_tool import RecommendationTool
from app.tools.comparison_table_tool import ComparisonTableTool
from app.tools.history_tool import HistoryTool
from langgraph.graph import END, StateGraph

from app.tools.planner_tool import PlannerTool
from app.tools.tavily_tool import TavilyTool
from app.tools.serpapi_tool import SerpAPITool
from app.tools.extractor_tool import ExtractorTool
from app.tools.compare_tool import CompareTool
from app.tools.review_tool import ReviewTool


class AgentState(TypedDict):

    query: str
    plan: dict

    tavily_result: dict
    serpapi_result: dict

    products: list

    best_product: dict

    review: str

    final_result: dict


class ShoppingAgent:

    # ---------------- Planner ---------------- #

    def planner_node(
        self,
        state: AgentState,
    ):

        planner = PlannerTool()

        try:

            state["plan"] = json.loads(
                planner.plan(
                    state["query"]
                )
            )

        except Exception:

            state["plan"] = {

                "need_search": True,

                "need_reviews": True,

                "need_compare": True,

            }

        return state

    # ---------------- Tavily ---------------- #

    def tavily_node(
        self,
        state: AgentState,
    ):

        tool = TavilyTool()

        state["tavily_result"] = tool.search(
            state["query"]
        )

        return state

    # ---------------- SerpAPI ---------------- #

    def serpapi_node(
        self,
        state: AgentState,
    ):

        tool = SerpAPITool()

        state["serpapi_result"] = tool.search(
            state["query"]
        )

        return state

    # ---------------- Extract ---------------- #

    def extract_node(
        self,
        state: AgentState,
    ):

        state["products"] = ExtractorTool.extract(
            state["serpapi_result"]
        )

        return state

    # ---------------- Compare ---------------- #

    def compare_node(
        self,
        state: AgentState,
    ):

        state["best_product"] = CompareTool.compare(
            state["products"]
        )

        return state

    # ---------------- Review ---------------- #

    def review_node(
        self,
        state: AgentState,
    ):

        state["review"] = ReviewTool.summarize(
            state["best_product"]
        )






        return state

    
    # ---------------- Final ---------------- #

    def final_node(
        self,
        state: AgentState,
    ):

        best = state.get("best_product")

        if not best:

            state["final_result"] = {

                "query": state["query"],

                "message": "No suitable product found.",

                "all_products": [],

            }

            return state


        ai_recommendation = RecommendationTool.recommend(
            best,
            state["products"],
        )

        comparison_table = ComparisonTableTool.build(
            state["products"],
        )
        sorted_products = sorted(
            state["products"],
            key=lambda x: x.get(
                "comparison",
                {},
            ).get(
                "total_score",
                0,
            ),
            reverse=True,
        )

        alternatives = []

        for product in sorted_products:

            if product.get("name") == best.get("name"):
                continue

            alternatives.append({

                "name": product.get(
                    "name",
                    "",
                ),

                "platform": product.get(
                    "platform",
                    "",
                ),

                "price": product.get(
                    "price",
                    0,
                ),

                "rating": product.get(
                    "rating",
                    0,
                ),

                "reviews": product.get(
                    "reviews",
                    0,
                ),

                "confidence": product.get(
                    "confidence",
                    0,
                ),

                "buy_link": product.get(
                    "link",
                    "",
                ),

            })

            if len(alternatives) == 3:
                break







        state["final_result"] = {

            "query": state["query"],

            "plan": state.get(
                "plan",
                {},
            ),

            "best_product": {

                "name": best.get(
                    "name",
                    "",
                ),

                "platform": best.get(
                    "platform",
                    "",
                ),

                "price": best.get(
                    "price",
                    0,
                ),

                "rating": best.get(
                    "rating",
                    0,
                ),

                "reviews": best.get(
                    "reviews",
                    0,
                ),

                "confidence": best.get(
                    "confidence",
                    0,
                ),

                "buy_link": best.get(
                    "link",
                    "",
                ),

                "thumbnail": best.get(
                    "thumbnail",
                    "",
                ),


                "score_breakdown": best.get(
                    "comparison",
                    {},
                ),









            },



            "comparison": best.get(
                "comparison",
                {},
            ),

            "comparison_table": comparison_table,
            "alternatives": alternatives,

            "ai_recommendation": ai_recommendation,

            "review": state.get(
                "review",
                "",
            ),

            "products_found": len(
                state.get(
                    "products",
                    [],
                )
            ),

            "all_products": state.get(
                "products",
                [],
            ),

            "sources": state.get(
                "tavily_result",
                {},
            ),

            "recommendation": {

                "summary": f"{best.get('name')} is the best overall choice.",

                "why_selected": [

                    "Lowest effective price",

                    "High customer rating",

                    "Large number of verified reviews",

                    "Trusted seller",

                    "Highest overall comparison score",

                ],

                "confidence": f"{best.get('confidence',0)}%",

            },

        }

        HistoryTool.save(
            state["final_result"]
        )

        return state
    # ---------------- Graph ---------------- #

    def build(self):

        graph = StateGraph(
            AgentState
        )

        graph.add_node(
            "planner",
            self.planner_node,
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
            "planner",
        )

        graph.add_edge(
            "planner",
            "tavily",
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