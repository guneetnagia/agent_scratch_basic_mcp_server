import aiohttp

class LLMClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    async def generate(self, prompt: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                json={"model": self.model, "prompt": prompt, "stream": False}
            ) as resp:
                data = await resp.json()
                return data.get("response")