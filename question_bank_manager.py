import asyncio 
from agents import gen_trace_id, trace, Runner
from planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from qb_generator_agent import qb_generator_agent, QuestionBankData
import search_agent

class QuestionBankManager:
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the question bank"""
        trace_id = gen_trace_id()
        with trace("Deep Research", trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, generating question bank..."
            question_bank = await self.generate_question_bank(query, search_results)
            yield question_bank.questions
    
    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def generate_question_bank(self, query: str, search_results: list[str]) -> QuestionBankData:
        """ Generate a question bank """
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            qb_generator_agent,
            input,
        )

        print("Finished generating question bank")
        return result.final_output_as(QuestionBankData)



