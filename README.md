# Ocean irc

an irc client/bot pair for implementing slack-like functionality

## Design Goals

- The entire service should be able to run on any irc server, and be invisible to users not running the Ocean client

- The Ocean Client should be clean, minimalist, and usable without constantly querying /who commands.

## Observations

- External service integrations (i.e. a chat message when a git branch is pushed to, etc) can already be implemented in vanilla irc with bots.

- Irc's existing commands are all formatted as `/command`. Therefore, in order to mesh well with existing services, custom Ocean commands should be prefixed with `/` (i.e `/hangouts`, `/yo`, &c)

##Protocol

###Client Protocol

 - On connecting to the 