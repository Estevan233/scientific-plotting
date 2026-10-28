#!/usr/bin/env bash
# ==============================================================================
# One-click installer for scientific-plotting skill on macOS / Linux
# Usage:
#   ./install.sh                # Installs globally to ~/.gemini/skills/scientific-plotting
#   ./install.sh --workspace    # Installs to current directory's .agents/skills/scientific-plotting
#   ./install.sh --pip          # Also runs 'pip install -e .'
# ==============================================================================

set -euo pipefail

SCOPE="global"
DO_PIP=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --workspace)
      SCOPE="workspace"
      shift
      ;;
    --pip)
      DO_PIP=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================="
echo "   Scientific-Plotting Skill Installer (Unix/macOS)    "
echo "======================================================="

if [ "$SCOPE" = "global" ]; then
  TARGET_DIR="$HOME/.gemini/skills/scientific-plotting"
else
  TARGET_DIR="$(pwd)/.agents/skills/scientific-plotting"
fi

echo "[*] Installation Scope : $SCOPE"
echo "[*] Destination Path   : $TARGET_DIR"

mkdir -p "$TARGET_DIR"

ITEMS=(
  "SKILL.md"
  "AGENTS.md"
  "CLAUDE.md"
  "README.md"
  "pyproject.toml"
  "requirements.txt"
  "LICENSE"
  ".cursor"
  "scripts"
  "scientific_plotting"
  "examples"
  "references"
)

for item in "${ITEMS[@]}"; do
  if [ -e "$SCRIPT_DIR/$item" ]; then
    cp -r "$SCRIPT_DIR/$item" "$TARGET_DIR/"
    echo "  [+] Copied: $item"
  fi
done

if [ "$DO_PIP" = true ]; then
  echo "[*] Installing Python package via pip (editable mode)..."
  pip install -e "$TARGET_DIR"
fi

echo ""
echo "[OK] Installation completed successfully!"
echo "Skill is ready for Antigravity, Gemini CLI, Cursor, and Claude Code."

