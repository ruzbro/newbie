#!/bin/bash
set -e

# install nvm - this is idempotent and will just update if already installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Source nvm script to make it available in this session.
# The nvm installer puts the script in /usr/local/share/nvm in this environment.
export NVM_DIR="/usr/local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Now that nvm is loaded, install node and the gemini-cli
nvm install --lts
npm install -g @google/gemini-cli 