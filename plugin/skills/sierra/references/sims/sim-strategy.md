# Simulation Strategy

This document contains guidance about organising simulations - how to mantain, fix and iterate over sim suite.

## Suite Design Principles

- Suite must be intuitive to explore through both - Studio UI and CLI. For humans and coding agents.
- An agent can have hundeds of simulations. It's impossible for a human to keep the details of all of them in their head, which is why organization is so important.
- Collaborators on the agent will frequently vibe-code simulations, so don't trust existing organisation at face value.
- Naming: group and simulation names are for humans and are meant to work together.  In Studio, simulation names are truncated at 45 characters and groups even sooner. 
  - Maximise information in those first 45 characters, avoid things like generic prefixes.
  - Group names provide grouping data, simulation names narrow down the senario within that group.
- If working on an issue, with the report ready, identify whether there's an existing simulation that is already guarding the target behaviour.
  - If there is one, see if it did not observe the behaviour correctly or at all. In this case the preferred strategy is to re-use the existing simulation.
  - If the behaviour was not guarded, find simulations with similar scenarios.
- For simulations we expect to have to iterate for task at hand, see if they would benefit from small refactoring to better observe the organisation principles.
- A single simulation must evaluate a single scenario end to end. A scenario split into several simulations is bad - it increases complexity and tax on effort needed to maintain them.
- CLI and Agent readability is archieved through tags. Design them to facilitate running sim runs scoped to behaviour patterns.

## Grouping

I've been able to identify the following groups that are common:

- "Abuse"
- "Guardrails"

