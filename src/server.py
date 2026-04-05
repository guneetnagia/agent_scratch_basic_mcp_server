"""
Idea Hub MCP Server (Refactored with Service Layer)

Clean architecture:
Tools → Services → Repositories → Infrastructure
"""

import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

from fastmcp import FastMCP
from typing_extensions import Annotated

# Services
from src.services.search_service import SearchService
from src.services.duplicate_service import DuplicateService
from src.services.analysis_service import AnalysisService
from src.services.contributor_service import ContributorService

# Repositories
from src.repositories.idea_repository import IdeaRepository
# (add contributor repo later)

# Infrastructure
from src.infrastructure.embedding_client import EmbeddingClient
from src.infrastructure.llm_client import LLMClient


logger = logging.getLogger(__name__)


# =========================
# Context (NO GOD OBJECT)
# =========================
@dataclass
class ServerContext:
    search_service: SearchService
    duplicate_service: DuplicateService
    analysis_service: AnalysisService
    contributor_service: ContributorService


# =========================
# MCP SERVER
# =========================
class IdeaHubMCPServer:

    def __init__(self):
        self.app = FastMCP("Idea Hub MCP Server")
        self.context: Optional[ServerContext] = None
        self._register_tools()

    # -------------------------
    # Context Initialization
    # -------------------------
    async def _initialize_context(self):
        if self.context:
            return

        logger.info("⚙️ Initializing services...")

        # Infrastructure
        embedding_client = EmbeddingClient()
        llm_client = LLMClient()

        # Repositories
        idea_repo = IdeaRepository()

        # Services
        search_service = SearchService(idea_repo, embedding_client)
        duplicate_service = DuplicateService(idea_repo, embedding_client)
        analysis_service = AnalysisService(llm_client, idea_repo)

        contributor_service = ContributorService(
            contributor_repo=None,  # TODO: implement
            idea_repo=idea_repo,
            embedding_client=embedding_client
        )

        self.context = ServerContext(
            search_service=search_service,
            duplicate_service=duplicate_service,
            analysis_service=analysis_service,
            contributor_service=contributor_service
        )

        logger.info("✅ Services initialized")

    # -------------------------
    # Tool Registration
    # -------------------------
    def _register_tools(self):

        @self.app.tool()
        async def search_ideas(
            query: Annotated[str, "Search query"],
            search_type: Annotated[str, "semantic | keyword | hybrid"] = "hybrid",
            limit: Annotated[int, "Max results"] = 10,
            status_filter: Annotated[Optional[str], "Optional status"] = None
        ) -> Dict[str, Any]:

            await self._initialize_context()

            return await self.context.search_service.search(
                query=query,
                search_type=search_type,
                limit=limit,
                status_filter=status_filter
            )

        @self.app.tool()
        async def detect_duplicates(
            title: Annotated[str, "Idea title"],
            description: Annotated[str, "Idea description"],
            threshold: Annotated[float, "Similarity threshold"] = 0.8
        ) -> Dict[str, Any]:

            await self._initialize_context()

            return await self.context.duplicate_service.detect(
                title=title,
                description=description,
                threshold=threshold
            )

        @self.app.tool()
        async def generate_idea_summary(
            idea_id: Annotated[int, "Idea ID"],
            summary_type: Annotated[str, "brief | detailed | technical"] = "brief"
        ) -> Dict[str, Any]:

            await self._initialize_context()

            return await self.context.analysis_service.generate_summary(
                idea_id=idea_id,
                summary_type=summary_type
            )

        @self.app.tool()
        async def match_contributors_to_idea(
            idea_id: Annotated[int, "Idea ID"],
            required_skills: Annotated[list, "Skills list"],
            max_contributors: Annotated[int, "Max contributors"] = 3
        ) -> Dict[str, Any]:

            await self._initialize_context()

            return await self.context.contributor_service.match(
                idea_id=idea_id,
                required_skills=required_skills,
                max_contributors=max_contributors
            )

    # -------------------------
    # Public API
    # -------------------------
    def get_app(self):
        return self.app
    

    async def shutdown(self):
        from src.infrastructure.database import Database
        await Database.disconnect()