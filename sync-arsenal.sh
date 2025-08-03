#!/bin/bash

# Elite AI Prompt Arsenal Sync Script
# Easy deployment to any project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
PROJECT_PATH="."
GLOBAL_MODE=false

# Help function
show_help() {
    echo -e "${CYAN}Elite AI Prompt Arsenal Sync Script${NC}"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -p, --path PATH     Target project path (default: current directory)"
    echo "  -g, --global        Deploy to global snippets (all Cursor workspaces)"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                          # Deploy to current project"
    echo "  $0 -p /path/to/project      # Deploy to specific project"
    echo "  $0 -g                       # Deploy globally"
    echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        -g|--global)
            GLOBAL_MODE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🚀 Deploying Elite AI Prompt Arsenal...${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$GLOBAL_MODE" = true ]; then
    # Deploy to global snippets
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        GLOBAL_DIR="$APPDATA/Code/User/snippets"
    else
        # macOS/Linux
        GLOBAL_DIR="$HOME/.config/Code/User/snippets"
    fi
    
    # Create directory if it doesn't exist
    mkdir -p "$GLOBAL_DIR"
    
    # Copy files
    cp "$SCRIPT_DIR/.vscode/Elite Prompt Setup.code-snippets" "$GLOBAL_DIR/elite-global-snippets.code-snippets"
    cp "$SCRIPT_DIR/.vscode/Smart Context Templates.code-snippets" "$GLOBAL_DIR/elite-context-templates.code-snippets"
    
    echo -e "${GREEN}✅ Deployed to global snippets:${NC}"
    echo -e "${CYAN}   - $GLOBAL_DIR/elite-global-snippets.code-snippets${NC}"
    echo -e "${CYAN}   - $GLOBAL_DIR/elite-context-templates.code-snippets${NC}"
else
    # Deploy to project .vscode folder
    PROJECT_VSCODE_DIR="$PROJECT_PATH/.vscode"
    TARGET_FILE="$PROJECT_VSCODE_DIR/Elite Prompt Setup.code-snippets"
    TARGET_CONTEXT_FILE="$PROJECT_VSCODE_DIR/Smart Context Templates.code-snippets"
    
    # Create .vscode directory if it doesn't exist
    mkdir -p "$PROJECT_VSCODE_DIR"
    
    # Copy files
    cp "$SCRIPT_DIR/.vscode/Elite Prompt Setup.code-snippets" "$TARGET_FILE"
    cp "$SCRIPT_DIR/.vscode/Smart Context Templates.code-snippets" "$TARGET_CONTEXT_FILE"
    
    echo -e "${GREEN}✅ Deployed to project:${NC}"
    echo -e "${CYAN}   - $TARGET_FILE${NC}"
    echo -e "${CYAN}   - $TARGET_CONTEXT_FILE${NC}"
fi

echo ""
echo -e "${CYAN}🎯 Elite AI Prompt Arsenal ready to use!${NC}"
echo -e "${YELLOW}📝 Available prefixes:${NC}"
echo -e "${YELLOW}   Elite Prompts: thinkwithai, surgicalfix, refactorintent, writetest, doccode, unstuck, augmentsearch, kenyafirst, mindreset${NC}"
echo -e "${YELLOW}   Context Chains: taskchain, memorychain, debugchain, refactorchain, searchchain, recoverychain${NC}"
echo ""
echo -e "${GREEN}✨ Your Cursor experience is now enhanced with elite AI patterns!${NC}" 