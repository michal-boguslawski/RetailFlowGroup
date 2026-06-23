import time
from threading import Event
from typing import Callable

from domain.types import GeneratedRecord
from generator.stores.base import BaseRouter


class GeneratorLoop:
    def __init__(
        self,
        step: Callable[[], GeneratedRecord],   # could be make_one for user, or step for session, where step handles transitons
        breaktime_generator: Callable[[], float],
        router: BaseRouter,
        pipeline = None,
    ):
        self.step = step
        self.breaktime_generator = breaktime_generator
        self.pipeline = pipeline
        self.router = router
        self.tick_count = 0

        self.stop_event = Event()

    def bootstrap(self, n: int):
        records = [self.step() for _ in range(n)]
        if records is None:
            return

        if self.pipeline:
            records = [self.pipeline.run(record) for record in records]

        for sink in self.router.route(records[0]):
            sink.bulk_write(records)

    def tick(self) -> None:
        record = self.step()

        if record is None:
            return

        if self.pipeline:
            record = self.pipeline.run(record)

        for sink in self.router.route(record):
            sink.write(record)

        self.tick_count += 1

        if self.tick_count % 100 == 0:
            print(f"{self.tick_count} records processed")

    def run(self):
        while not self.stop_event.is_set():
            self.tick()

            breaktime = self.breaktime_generator()
            print(f"Wait for {breaktime} seconds...")

            # IMPORTANT: replace time.sleep()
            self.stop_event.wait(breaktime)

    def stop(self):
        self.stop_event.set()
