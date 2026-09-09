# Simulation network and knowledge failures

Read when knowledge-dependent simulations fail together, an upstream fetch times out, or an integration needs an egress allowlist.

A wholesale 0-of-5 across knowledge-dependent simulations usually means the environment, not the agent. Check the setup-failure tag `^kb-search-failure:setup-error` and upstream fetch timeouts before touching code. Upstream knowledge dependencies can have real multi-day outages. Do not change the implementation to hide an unavailable dependency.

Simulations and staging conversations egress from production's NAT EIPs on Sierra-managed deployments. Exceptions: the knowledge crawler (Firecrawl's rotating IPs), PCI connectors (PCI EIPs), and BYOC (the customer's network). This is the topology, not a current IP list. Confirm the actual egress with `ask_sierra_assistant` before changing an allowlist, and never infer a source IP from a staging hostname.

Read [result access](simulation-results.md) for the detailed evidence and [testing](testing.md) for the gate interpretation.
