```markdown
# OpenClaw Setup Guide for Windows (WSL2)
## Complete Setup with Multi-Agent & Claude Subscription

---

## Table of Contents

- [Best Options Overview](#best-options-overview)
- [Prerequisites](#prerequisites)
- [Step 1: Install WSL2 & Ubuntu](#step-1-install-wsl2--ubuntu)
- [Step 2: Enable Systemd](#step-2-enable-systemd)
- [Step 3: Install OpenClaw](#step-3-install-openclaw)
- [Step 4: Configure Claude Subscription](#step-4-configure-claude-subscription)
- [Step 5: Multi-Agent Setup (No JSON Editing)](#step-5-multi-agent-setup-no-json-editing)
- [Step 6: Start the Gateway Service](#step-6-start-the-gateway-service)
- [Step 7: Auto-Start at Windows Boot (Optional)](#step-7-auto-start-at-windows-boot-optional)
- [Troubleshooting](#troubleshooting)
- [Quick Commands Reference](#quick-commands-reference)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## Best Options Overview

| Component | Best Option | Why |
|-----------|-------------|-----|
| **Windows Runtime** | WSL2 (Ubuntu) | Most stable path for full CLI, Gateway, and tool compatibility |
| **Claude Access** | **Claude CLI** (existing login) | Reuses your Claude subscription without a separate API key; works via `claude -p` non-interactive mode |
| **Multi-Agent Setup** | **CLI Commands** | No JSON editing needed - add/remove agents with simple commands |

> **⚠️ Important Note on Claude CLI Billing**: Starting June 15, 2026, `claude -p` usage via subscription draws from your monthly Agent SDK credit first, then usage credits at standard API rates.

---

## Prerequisites

- Windows 10/11 with virtualization enabled
- An active Claude subscription
- Internet connection
- Administrator access (for WSL installation)

---

## Step 1: Install WSL2 & Ubuntu

**Open PowerShell as Administrator** and run:

```powershell
# Install WSL2 with Ubuntu
wsl --install

# Or specify a specific Ubuntu version:
wsl --install -d Ubuntu-24.04
```

**Reboot your computer** if prompted.

After reboot, launch Ubuntu from your Start Menu and complete the initial setup (create username/password).

**Verify WSL installation:**

```powershell
wsl --list --verbose
```

You should see Ubuntu listed with version 2.

---

## Step 2: Enable Systemd

**Systemd is required** for the OpenClaw Gateway service to auto-start.

### Enable Systemd in WSL

In your WSL terminal, run:

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

### Restart WSL

**Shutdown WSL** from PowerShell:

```powershell
wsl --shutdown
```

**Re-open Ubuntu** and verify systemd is working:

```bash
systemctl --user status
```

> ✅ If you see a status message without errors, systemd is enabled correctly. If you get an error about D-Bus, restart WSL again.

---

## Step 3: Install OpenClaw

**Run these commands in your WSL terminal:**

### Option A: Quick Install (Recommended)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Option B: Install from Source

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
```

### Verify Installation

```bash
openclaw --version
openclaw doctor
```

> ✅ The `doctor` command will check your system and point out any issues. Run this regularly to ensure your setup is healthy.

---

## Step 4: Configure Claude Subscription

### Option A: Use Claude CLI (Recommended - No API Key Needed)

This method reuses your existing Claude subscription login.

**First, ensure Claude CLI is installed and logged in:**

```bash
# Install Claude CLI (if not already installed)
npm install -g @anthropic-ai/claude-cli

# Check login status
claude auth status

# If not logged in, run:
claude auth login
```

**Now run OpenClaw onboarding:**

```bash
openclaw onboard
```

> ✅ OpenClaw will automatically detect your Claude CLI credentials and use them. You'll see a message confirming "Claude CLI detected" during onboarding.

### Option B: Use API Key (Alternative)

If you prefer using an API key instead:

1. Create an API key in the [Anthropic Console](https://console.anthropic.com/)
2. Set it as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
openclaw onboard
```

### Verify Claude Access

```bash
openclaw models status --provider anthropic
```

> ✅ You should see your available Claude models listed (e.g., Claude 3.5 Sonnet, Claude 3 Opus, etc.).

---

## Step 5: Multi-Agent Setup (No JSON Editing)

OpenClaw includes CLI commands to add and manage agents **without touching JSON files**. Each agent gets its own isolated workspace, state, and tool permissions.

### Complete Agent Management Commands

| Command | Description |
|---------|-------------|
| `openclaw agents add <id>` | Add a new agent with default settings |
| `openclaw agents add <id> --default` | Add as default agent |
| `openclaw agents add <id> --workspace <path>` | Add agent with custom workspace |
| `openclaw agents remove <id>` | Remove an agent |
| `openclaw agents list` | List all configured agents |
| `openclaw agents list --verbose` | List agents with detailed info |
| `openclaw agents restrict <id> --allow <tools>` | Allow specific tools for an agent |
| `openclaw agents restrict <id> --deny <tools>` | Deny specific tools for an agent |
| `openclaw agents set-default <id>` | Set which agent is the default |

### Channel Binding Commands

| Command | Description |
|---------|-------------|
| `openclaw bindings add <channel> --agent <id>` | Route a channel type to an agent |
| `openclaw bindings add <channel> --agent <id> --channel-id <id>` | Route specific channel to an agent |
| `openclaw bindings list` | List all channel bindings |
| `openclaw bindings remove <id>` | Remove a binding |

### Example: Creating a Basic Setup

```bash
# 1. Add your first agent (main/default)
openclaw agents add main --default

# 2. Add a second agent for documentation tasks
openclaw agents add docs --workspace ~/.openclaw/workspace-docs

# 3. Add a third agent for coding
openclaw agents add code --workspace ~/.openclaw/workspace-code

# 4. Restrict what the "docs" agent can do
openclaw agents restrict docs --allow read,write --deny exec

# 5. Route Slack messages to specific agents
openclaw bindings add slack --agent docs --channel-id "C0DOCS"   # docs agent for docs channel
openclaw bindings add slack --agent code --channel-id "C0CODE"   # code agent for code channel
openclaw bindings add slack --agent main                          # all other Slack messages go to main
```

### Example: Two Specialized Agents

```bash
# Create a "research" agent with restricted permissions
openclaw agents add research
openclaw agents restrict research --allow read,web_search --deny exec,write

# Create a "developer" agent with full access
openclaw agents add developer --workspace ~/.openclaw/workspace-dev

# Route accordingly
openclaw bindings add slack --agent research --channel-id "C0RESEARCH"
openclaw bindings add slack --agent developer --channel-id "C0DEVELOPER"
```

### View Your Configuration

```bash
# See all agents
openclaw agents list --verbose

# See all bindings
openclaw bindings list
```

> 💡 **Each agent gets its own**: Isolated workspace, Separate state management, Independent tool permissions, Unique identity (name/emoji)

---

## Step 6: Start the Gateway Service

### Install and Start the Service

```bash
# Install the gateway service (auto-starts on WSL boot)
openclaw gateway install

# Or use onboard with daemon installation:
openclaw onboard --install-daemon
```

### Verify Service Status

```bash
systemctl --user status openclaw-gateway --no-pager
```

> ✅ You should see `active (running)` in the status output. The service starts automatically when WSL boots.

### Check Gateway Logs

```bash
openclaw gateway logs

# Follow logs in real-time:
openclaw gateway logs --follow

# View last 50 lines:
openclaw gateway logs --lines 50
```

### Stop/Start the Service Manually

```bash
# Stop the service
systemctl --user stop openclaw-gateway

# Start the service
systemctl --user start openclaw-gateway

# Restart the service
systemctl --user restart openclaw-gateway
```

---

## Step 7: Auto-Start at Windows Boot (Optional)

For setups where you want the gateway running **before Windows login** (headless/always-on setups).

### Enable User Lingering

User lingering allows services to run even when you're not logged in:

```bash
sudo loginctl enable-linger "$(whoami)"
```

### Create Windows Scheduled Task

**In PowerShell as Administrator:**

```powershell
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

> Replace `Ubuntu` with your distro name (check with `wsl --list --verbose`).

### Verify Auto-Start

1. Reboot Windows
2. After reboot, open WSL and check:

```bash
systemctl --user status openclaw-gateway
```

> ✅ The service should be running automatically.

---

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| **Gateway service not starting** | Run `openclaw doctor --deep` to check configuration |
| **Claude auth not detected** | Verify `claude auth status` works outside OpenClaw; or use `ANTHROPIC_API_KEY` environment variable |
| **Agent tools not available** | Check per-agent restrictions with `openclaw agents list --verbose` |
| **Bindings not routing** | Verify channel IDs with `openclaw bindings list` |
| **Permission denied errors** | Ensure your user owns the workspace directories: `chown -R $USER:$USER ~/.openclaw/` |
| **WSL not starting** | Run `wsl --shutdown` then restart from Start Menu |
| **Systemd not working** | Verify `/etc/wsl.conf` contains `systemd=true` and restart WSL |
| **API key not recognized** | Ensure `ANTHROPIC_API_KEY` is set in your environment: `echo $ANTHROPIC_API_KEY` |
| **Port already in use** | Change gateway port in config or find the process using it: `sudo lsof -i :18789` |

### Quick Diagnostic Commands

```bash
# Deep system check
openclaw doctor --deep

# Check agent status
openclaw agents list --verbose

# Check gateway status
systemctl --user status openclaw-gateway

# View recent errors
openclaw gateway logs --lines 50

# Check system resources
wsl --status
```

### Resetting Your Setup

If you need to start fresh:

```bash
# Uninstall the gateway
openclaw gateway uninstall

# Remove OpenClaw configuration (backup first!)
mv ~/.openclaw ~/.openclaw.backup

# Re-run onboarding
openclaw onboard
```

---

## Quick Commands Reference

### Agent Management

```bash
# Add an agent
openclaw agents add <id> [--workspace <path>] [--default]

# Remove an agent
openclaw agents remove <id>

# List agents
openclaw agents list [--verbose]

# Restrict agent tools
openclaw agents restrict <id> --allow <tool1,tool2> --deny <tool3,tool4>

# Set default agent
openclaw agents set-default <id>
```

### Channel Bindings

```bash
# Add a binding
openclaw bindings add <channel> --agent <id> [--channel-id <id>]

# List bindings
openclaw bindings list

# Remove a binding
openclaw bindings remove <id>
```

### Gateway Control

```bash
# Install as service
openclaw gateway install

# Uninstall service
openclaw gateway uninstall

# View logs
openclaw gateway logs [--follow] [--lines <n>]
```

### System Checks

```bash
# Basic health check
openclaw doctor

# Comprehensive check
openclaw doctor --deep

# Check model availability
openclaw models status [--provider <provider>]
```

### Testing Your Setup

```bash
# Send a test message to the default agent
openclaw message send "Hello, what can you help me with?"

# Send a message to a specific agent
openclaw message send --agent docs "Summarize this document for me"

# Send a message with context
openclaw message send --agent code "Review this code" --file ./code.py
```

---

## Next Steps

1. **Test your setup**: Send a message to your default agent
2. **Add more agents**: Use `openclaw agents add` for different use cases
3. **Configure bindings**: Connect your agents to Slack, Discord, or other channels
4. **Customize workspaces**: Each agent gets its own isolated workspace
5. **Set up monitoring**: Enable logging and alerts for your agents
6. **Explore advanced features**: 
   - Custom tool creation
   - Agent collaboration patterns
   - Multi-channel routing

### Example: Complete Production Setup

```bash
# Create specialized agents
openclaw agents add support --workspace ~/.openclaw/workspace-support
openclaw agents add dev --workspace ~/.openclaw/workspace-dev
openclaw agents add ops --workspace ~/.openclaw/workspace-ops

# Set restrictions
openclaw agents restrict support --allow read,web_search,ticket --deny exec,write
openclaw agents restrict ops --allow read,exec,deploy --deny write

# Route channels
openclaw bindings add slack --agent support --channel-id "C0SUPPORT"
openclaw bindings add slack --agent dev --channel-id "C0DEV"
openclaw bindings add discord --agent support --channel-id "tickets"
openclaw bindings add irc --agent ops --channel-id "#deployment"

# Set defaults
openclaw agents set-default support
```

---

## Additional Resources

- [OpenClaw Official Documentation](https://openclaw.ai/docs)
- [Multi-Agent Configuration Guide](https://openclaw.ai/docs/agents)
- [Channel Bindings Setup](https://openclaw.ai/docs/bindings)
- [WSL2 Systemd Setup Guide](https://learn.microsoft.com/en-us/windows/wsl/systemd)
- [Claude CLI Documentation](https://docs.anthropic.com/en/docs/claude-cli)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

### Community Support

- [OpenClaw Discord](https://discord.gg/openclaw)
- [GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [Stack Overflow (openclaw tag)](https://stackoverflow.com/questions/tagged/openclaw)

---
