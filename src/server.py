import asyncio
import websockets


async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send("Echo: " + message)

start_server = websockets.serve(echo, "192.168.0.102", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
