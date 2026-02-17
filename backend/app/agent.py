"""
LiveKit agent worker entry point

Run this script to start the LiveKit agent:
    python -m app.agent start
"""
from dotenv import load_dotenv
from livekit.agents import cli, WorkerOptions, WorkerPermissions, WorkerType
from app.services.livekit_agent_service import livekit_agent_entrypoint
from app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)
load_dotenv()


if __name__ == "__main__":
    logger.info("Starting LiveKit agent worker...")
    opts = WorkerOptions(
        entrypoint_fnc=livekit_agent_entrypoint,
        worker_type=WorkerType.ROOM,
        permissions=WorkerPermissions(
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True
        )
    )
    cli.run_app(opts)
