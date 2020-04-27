# proto

This repository contains Seabird's gRPC protobuf definitions.

## What is this?

This project moves Seabird plugins from individual threads in the same process as Seabird proper out into completely separate processes (even in separate containers/hosts/etc) that communicate with the `core` bot over RPC.

## ...why?

1. This setup allows for low-interruption upgrades of individual plugins.

2. This setup enables finer-grained, cleaner control over access to the bot.

This in particular is useful for defining an admin interface for the bot. The

3. This setup allows for testing plugin instances against the production version of the `core`.

## Isn't this a bad idea? I mean, this is just an IRC bot.

Yes, for the following reasons:

1. This setup is more complicated in code than the existing system of one-thread-per-plugin.
The setup forces us to think about failure scenarios that aren’t present in a single-process architecture. We also need to expose a more fully featured API from `core` in order to properly support tracking useful information.

2. This setup is more complicated to run than the existing system.
We need to make sure to have a good README and wikis as necessary to set this up properly. Perhaps we should also have Dockerfiles and/or setup scripts.

3. The database connection cannot easily be shared
Because of this, each plugin will need to maintain their own connection to the database if they need it.

## Client connection flow

1. Plugin initializes
2. Plugin calls `Register`
3. Plugin streams `Events`

## What is "core"?
`core` is the core IRC bot that maintains a connection to a given IRC server. It's the server on the other end of the gRPC connection.

## As a client, what can I expect from core?
Every incoming IRC message that `core` receives from its connected IRC server will be sent to each connected plugin through that plugin’s event stream.

Events will be delivered to plugins at most one time. Messages will not be queued, nor do they require acks from plugins (beyond gRPC's internal protocol).

## What happens if core restarts?
If the running instance of `core` restarts, all client connections will be interrupted. Each client will need to reconnect (see [this](#client-connection-flow)).

## Are plugins allowed to reconnect?
Yes. Additionally, there is no limitation on opened event streams by clients.

## I want to use this! How do I do that?
Unfortunately, this is under active development and is pretty clunky for now.

You'll need at a minimum a running instance of [core](https://github.com/seabird-irc/seabird-core). From there, you may clone various plugin repositories as desired and configure them to connect to `core`.

## License

MIT
