import asyncio


async def primary_task(step=1):
    print('primary task {step}'.format(step=step))
    await asyncio.sleep(1)
    await primary_task(step + 1)


async def secondary_task(step=1):
    print('secondary task {step}'.format(step=step))
    await asyncio.sleep(1)
    await secondary_task(step + 1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(secondary_task())
    loop.run_until_complete(primary_task())
