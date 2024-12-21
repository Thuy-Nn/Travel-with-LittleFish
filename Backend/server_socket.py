import asyncio

import yaml
from websockets.asyncio.server import serve

from MODEL_ZOO import MODEL_ZOO

config = yaml.safe_load(open("config.yaml"))

# Load the model and tokenizer
MODEL_TYPE = "OpenAI"
MODEL_NAME = "gpt-4o-mini-2024-07-18"
# MODEL_TYPE = "Llama"
# MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
# MODEL_TYPE = "Qwen"
# MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

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
    async with serve(handler, config['ENV']['host'], config['ENV']['port']):
        print(f"Socket server is listening at {config['ENV']['host']}:{config['ENV']['port']}")
        await asyncio.get_running_loop().create_future()


if __name__ == '__main__':
    asyncio.run(main())
