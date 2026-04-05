class ContributorService:
    def __init__(self, contributor_repo, idea_repo, embedding_client):
        self.contributor_repo = contributor_repo
        self.idea_repo = idea_repo
        self.embedding_client = embedding_client

    async def match(self, idea_id: int, required_skills: list, max_contributors: int):
        idea = await self.idea_repo.get_by_id(idea_id)

        idea_embedding = await self.embedding_client.embed(
            idea["title"] + " " + idea["description"]
        )

        contributors = await self.contributor_repo.find_all()

        scored = []
        for c in contributors:
            score = self._score(c, required_skills, idea_embedding)
            scored.append((score, c))

        scored.sort(reverse=True)

        return {
            "matches": [c for _, c in scored[:max_contributors]]
        }

    def _score(self, contributor, required_skills, idea_embedding):
        skill_overlap = len(set(required_skills) & set(contributor["skills"]))
        return skill_overlap  # extend later