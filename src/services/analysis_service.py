from src.infrastructure.llm_client import LLMClient

class AnalysisService:
    def __init__(self, llm_client: LLMClient, repo):
        self.llm = llm_client
        self.repo = repo

    async def generate_summary(self, idea_id: int, summary_type: str):
        idea = await self.repo.get_by_id(idea_id)

        prompt = f"""
        Summarize this idea ({summary_type}):

        {idea['title']}
        {idea['description']}
        """

        response = await self.llm.generate(prompt)

        return {
            "idea_id": idea_id,
            "summary": response
        }