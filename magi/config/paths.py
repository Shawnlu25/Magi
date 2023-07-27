from pathlib import Path

WORKSPACE_PATH = Path.home() / ".magi"
CONFIG_PATH = WORKSPACE_PATH / "config.yaml"
DIALOGUE_SAVE_PATH = WORKSPACE_PATH / "dialogues"

def initialize_workspace_paths():
    if not WORKSPACE_PATH.exists():
        WORKSPACE_PATH.mkdir(parents=True, exist_ok=True)
    
    if not DIALOGUE_SAVE_PATH.exists():
        DIALOGUE_SAVE_PATH.mkdir(parents=True, exist_ok=True)