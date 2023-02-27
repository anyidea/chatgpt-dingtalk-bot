import trio


class AsyncChatbotPool:
    def __init__(self, objs):
        self.objects = trio.Queue()
        for obj in objs:
            self.objects.put_nowait(obj)
        self.locks = {}

    async def get_object(self):
        obj = await self.objects.get()
        lock = trio.Lock()
        self.locks[obj] = lock
        async with lock:
            return obj

    def release_object(self, obj):
        if obj in self.locks:
            lock = self.locks[obj]
            lock.release()
            self.objects.put_nowait(obj)
        else:
            raise ValueError("Invalid chabot: %s" % obj)
