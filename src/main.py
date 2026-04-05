#!/usr/bin/env python3
"""
Idea Hub MCP Server - Entry Point

Starts the MCP server using FastMCP.
"""

import logging
from src.server import IdeaHubMCPServer

# Configure logging (upgrade to JSON later if needed)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("🚀 Starting Idea Hub MCP Server...")

        server = IdeaHubMCPServer()
        app = server.get_app()

        # FastMCP handles async internally
        app.run()

    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")

    except Exception as e:
        logger.exception("❌ Server failed")
        raise e


if __name__ == "__main__":
    main()