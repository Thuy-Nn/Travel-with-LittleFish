import asyncio
import websockets
from websockets.asyncio.server import serve
from MODEL_ZOO import MODEL_ZOO

# Load the model and tokenizer
MODEL_TYPE = 'Qwen'
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
model = None


# create handler for each connection
async def handler(websocket):
    while True:
        user_message = await websocket.recv()

        if not user_message:
            await websocket.send("Message is required")
            return

        global model
        if model is None:
            if MODEL_TYPE not in MODEL_ZOO:
                await websocket.send("Model type is not supported")
                return

            model = MODEL_ZOO[MODEL_TYPE](MODEL_NAME)

        if model is None:
            await websocket.send("Internal server error")
            return

        response = model.invoke(user_message)
        await websocket.send(response)


async def main():
    async with serve(handler, '', 8080):
        await asyncio.get_running_loop().create_future()


# start_server = serve(handler, "localhost", 8000)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    asyncio.run(main())
