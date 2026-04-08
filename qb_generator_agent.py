from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a exam setter for a school examination."
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with a question bank in text form having three different sections a specified. Question bank should have 3 sections very short questions, short questions and long questions. Max 10 questions for each section having 50 percent easy level, 30 percent medium level and 20 percent hard level\n"
    "No similar question allowed. Questions should be cover maximum of initial research results. Don't mention any remarks or hints about question difficulty level but do have questions."
)


class QuestionBankData(BaseModel):
    questions: str = Field(description="A question bank having three sections")


qb_generator_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=QuestionBankData,
)