fake_identity = "yolo"
pretend_this_is_safe = queue.Queue()


async def run_discord_bot():
    # Manage your Discord connection here
    while True:
        await asyncio.sleep(42)
        if we_were_kicked_from_a_channel():
            pretend_this_is_safe.push(("leave_channel", "magically_received_channel_id"))


async def read_incoming_core_messages():
    with connect_to_server() as client:
        client.Register(
            RegisterRequest(
                identity=fake_identity,
                id="discord, yo",
                supported_actions=[
                    "JoinChannel",
                    "LeaveChannel",
                    "ListChannelUsers",
                ],
            ),
        )

        event_queue = client.StreamEvents(StreamEventsRequest(identity=fake_identity))
        for thing in magical_select(event_queue, pretend_this_is_safe, timer(10)):
            if isinstance(thing, TimerTick):
                # Timer tick
                nonce = "lol"
                result = client.Heartbeat(HeartbeatRequest(nonce))
                if result.nonce != nonce:
                    print("uh oh")
            elif isinstance(thing, Event):
                # Seabird Core event
                do_discord_stuff_with_event(event)
            else:
                # Queue
                action, channel_id = thing

                if action == "leave_channel":
                    client.DeregisterChannels(
                        DeregisterChannelsRequest(
                            identity=fake_identity,
                            channel_ids=[channel_id],
                        ),
                    )


class ChatServiceHandler:
    async def run():
        """pretend there's something here"""

    async def JoinChannel(self, request: JoinChannelRequest) -> JoinChannelResponse:
        join_discord_channel(request.channel_name)

        return JoinChannelResponse()

    async def LeaveChannel(self, request: LeaveChannelRequest) -> LeaveChannelResponse:
        leave_discord_channel(get_channel_name_by_id(request.channel_id))

        return LeaveChannelResponse()

    async def ListChannelUsers(self, request: ListChannelUsersRequest) -> ListChannelUsersResponse:
        users = get_discord_channel_users(get_channel_name_by_id(request.channel_id))

        return ListChannelUsersResponse(
            channel_id=request.channel_id,
            user_ids=[user.id for user in users],
        )

    async def GetChannelTopic(self, request: ChannelTopicRequest) -> ChannelTopicResponse:
        raise HeyManICantDoThatError()

    async def SetChannelTopic(self, request: SetChannelTopicRequest) -> SetChannelTopicResponse:
        raise HeyManICantDoThatError()

    async def Heartbeat(self, request: HeartbeatRequest) -> HeartbeatResponse:
        return HeartbeatResponse(nonce=request.nonce)


async def main():
    """
    Each chat service runs three things:
    1. A thread managing connection(s) to the actual chat service (in this case FakeDiscord)
    2. A thread managing a connection to Seabird Core that both listens to messages from Core
       and sends actions back to Core
    3. A thread managing a server that Core can communicate with so that Core can do things like
       join/leave channels and other stuff.

    Upside:
    - We don't need to smash actions as an enum into common.Event
    Downside:
    - Core needs to manage connection to the chat, and vice-versa
    """
    await asyncio.gather(
        read_incoming_core_messages(),
        ChatServiceHandler().run(),
        run_discord_bot(),
    )
