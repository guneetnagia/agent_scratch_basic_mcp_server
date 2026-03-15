"""
Idea Hub MCP Server Implementation

This module implements the core MCP server for the Idea Hub platform using FastMCP.
It provides tools for AI agents to interact with the idea management system,
including semantic search, duplicate detection, contributor matching, and more.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import os
import sys
from pathlib import Path

# Import MCP components
try:
    from fastmcp import FastMCP
    from typing_extensions import Annotated
except ImportError:
    print("FastMCP dependencies not found. Please install with: pip install fastmcp")
    sys.exit(1)

# Import our custom tools and utilities


logger = logging.getLogger(__name__)


@dataclass
class ServerContext:
    """Context object to share resources between tools."""
    db_connection: DatabaseConnection
    config: MCPConfig
    idea_tools: IdeaTools
    vector_tools: VectorTools
    contributor_tools: ContributorTools
    ai_tools: AITools


class IdeaHubMCPServer:
    """Main MCP server class for Idea Hub using FastMCP."""
    
    def __init__(self):
        self.app = FastMCP("Idea Hub MCP Server")
        self.context: Optional[ServerContext] = None
        self._setup_tools()
    
    def _setup_tools(self):
        """Set up MCP tools using FastMCP decorators."""
        
        @self.app.tool()
        async def search_ideas(
            query: Annotated[str, "Search query for ideas"],
            search_type: Annotated[str, "Type of search (semantic, keyword, hybrid)"] = "hybrid",
            limit: Annotated[int, "Maximum number of results"] = 10,
            status_filter: Annotated[Optional[str], "Optional status filter"] = None
        ) -> Dict[str, Any]:
            """Search for ideas using semantic search or keywords."""
            if not self.context:
                await self._initialize_context()
            
            return await self.context.idea_tools.search_ideas(
                query=query,
                search_type=search_type,
                limit=limit,
                status_filter=status_filter
            )
        
        @self.app.tool()
        async def get_idea_details(
            idea_id: Annotated[int, "ID of the idea to get details for"]
        ) -> Dict[str, Any]:
            """Get detailed information about a specific idea."""
            if not self.context:
                await self._initialize_context()
            
            return await self.context.idea_tools.get_idea_details(idea_id)
        
        @self.app.tool()
        async def detect_duplicates(
            title: Annotated[str, "Title of the idea to check for duplicates"],
            description: Annotated[str, "Description of the idea to check"],
            threshold: Annotated[float, "Similarity threshold (0.0-1.0)"] = 0.8
        ) -> Dict[str, Any]:
            """Detect duplicate or similar ideas."""
            if not self.context:
                await self._initialize_context()
            
            return await self.context.idea_tools.detect_duplicates(
                title=title,
                description=description,
                threshold=threshold
            )
        
        @self.app.tool()
        async def generate_idea_summary(
            idea_id: Annotated[int, "ID of the idea to summarize"],
            summary_type: Annotated[str, "Type of summary (brief, detailed, technical, business)"] = "brief"
        ) -> Dict[str, Any]:
            """Generate AI summary of an idea."""
            if not self.context:
                await self._initialize_context()
            
            return await self.context.ai_tools.generate_summary(
                idea_id=idea_id,
                summary_type=summary_type
            )
        
    
    async def _initialize_context(self):
        """Initialize the server context with all required components."""
        if self.context:
            return  # Already initialized
            
        logger.info("Initializing MCP server context...")
        
        try:
            # Load configuration
            config = MCPConfig()
            
            # Initialize database connection
            db_connection = DatabaseConnection(config)
            await db_connection.initialize()
            
            # Initialize tool classes
            idea_tools = IdeaTools(db_connection, config)
            vector_tools = VectorTools(db_connection, config)
            contributor_tools = ContributorTools(db_connection, config)
            ai_tools = AITools(db_connection, config)
            
            # Create context
            self.context = ServerContext(
                db_connection=db_connection,
                config=config,
                idea_tools=idea_tools,
                vector_tools=vector_tools,
                contributor_tools=contributor_tools,
                ai_tools=ai_tools
            )
            
            logger.info("MCP server context initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize server context: {e}")
            raise
    
    async def run(self):
        """Run the MCP server."""
        logger.info("Starting Basic Agent Scratch MCP Server...")
        
        try:
            # Initialize context
            await self._initialize_context()
            
            # Run the FastMCP server
            await self.app.run()
            
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            # Cleanup
            if self.context and self.context.db_connection:
                await self.context.db_connection.close()
    
    def get_app(self):
        """Get the FastMCP app instance."""
        return self.app