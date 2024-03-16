import asyncio


async def foo():
    print('Start foo')
    await asyncio.sleep(1)
    print('End foo')


async def main():
    print('Start main')
    await foo()
    print('End main')


asyncio.run(main())
