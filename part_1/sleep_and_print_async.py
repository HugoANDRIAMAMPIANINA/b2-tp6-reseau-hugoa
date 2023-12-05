import asyncio

async def count():
    for i in range(0,10):
        print(i)
        await asyncio.sleep(0.5)
        
loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(count()),
    loop.create_task(count())
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()