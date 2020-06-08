# proto

This repository contains Seabird's gRPC protobuf definitions.

## What is this?

This project moves Seabird plugins from the same process as Seabird proper out into completely separate processes (even in separate containers/hosts/etc) that communicate with the `core` bot over RPC.

## But why?

1. This setup allows for low-interruption upgrades of individual plugins.

2. This setup enables finer-grained, cleaner control over access to the bot. In particular it allows us to define an admin interface for the bot over RPC and make tools for it.

3. This setup allows for testing plugin instances against the production version of the `core`.

## Isn't this a bad idea? I mean, this is just a chat bot.

Yes, for the following reasons:

1. This setup is more complicated in code than the existing system of one-thread-per-plugin. The setup forces us to think about failure scenarios that aren’t present in a single-process architecture. We also need to expose a more fully featured API from `core` in order to properly support tracking useful information.

2. This setup is more complicated to run than the existing system. We need to make sure to have a good README and wikis as necessary to set this up properly. Perhaps we should also have Dockerfiles and/or setup scripts.

3. The database connection cannot easily be shared. Because of this, each plugin will need to maintain their own connection to the database if they need it.

## Client connection information

Each gRPC request contains an Identity as the first field. This should be constructed with an auth token. Auth tokens need to be manually configured on the server side.

## What is "core"?

`core` is the main process and service implementation that acts as a broker for chat messages. It's the server on the other end of the gRPC connection.

## As a client, what can I expect from core?

Every incoming IRC message that `core` receives from its connected IRC server will be sent to each connected plugin through that plugin’s event stream.

Events will be delivered to plugins at most one time. Messages may be queued, but there is no guarantee. If an event stream starts lagging behind, it will be dropped.

## What happens if core restarts?

If the running instance of `core` restarts, all client connections will be interrupted. Each client will need to reconnect (see the [client connection information](#client-connection-information)).

## Are plugins allowed to reconnect?

Yes. Additionally, there is no limitation on opened event streams by clients.

## I want to use this! How do I do that?

Unfortunately, this is under active development and still fairly clunky, but if you really want to get involved you're welcome to!

At a minimum, you'll need a running instance of [core](https://github.com/seabird-irc/seabird-core). From there, you may clone various plugin repositories as desired and configure them to connect to `core`.

## License

MIT
