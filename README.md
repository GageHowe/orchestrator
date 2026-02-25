# agent-orchestration

This repo implements a centralized agent registry that informs the orchestrator agent of available agents, and ensures agents communicated with are trustworthy.

### Flow
* Orchestrator agent calls the Registry for a list of authenticated agents.
* For each remote agent, the Registry sends a nonce that the agent (if legitimate) will be able to sign with its private key.
* The Registry returns a list of authenticated agents with their address/port, summary of services, and usage guide.
* User submits a request.
* The Orchestrator then calls each agent over https as needed.

Note: the Orchestrator should be able to await responses and continue completing the task until completion.

WORK IN PROGRESS
