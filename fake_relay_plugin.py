async def get_channel_by_name(client, service_id, channel_name):
    response = client.ListChannels(
        ListChannelsRequest(identity="yolo", service_id=service_id),
    )
    for channel in response.channels:
        if channel.name == channel_name:
            return channel.id

    return None

async def main():
    relay = {
        "from": {
            "service": "some_service",
            "channel": "some_channel",
        },
        "to": {
            "service": "some_other_service",
            "channel": "some_other_channel",
        },
    }

    async with connect_to_service() as client:
        response = await client.ListServices(ListServicesRequest(identity="yolo"))
        from_service_id = None
        to_service_id = None
        for service in response.services:
            if service.name == relay["from"]["service"]:
                from_service_id = service.id

            if service.name == relay["to"]["service"]:
                to_service_id = service.id

        # TODO: combine requests if they're the same
        from_channel_id = await get_channel_by_name(client, from_service_id, relay["from"]["channel"])
        to_channel_id = await get_channel_by_name(client, to_service_id, relay["to"]["channel"])

        for event in await client.StreamEvents(StreamEventsRequest(identity="yolo")):
            if event.source_id == from_channel_id:
                await client.SendMessage(
                    SendMessageRequest(
                        identity="yolo",
                        destination_id=to_channel_id,
                        text=event.text,
                    )
                )
