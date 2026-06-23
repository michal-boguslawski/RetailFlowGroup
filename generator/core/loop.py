from collections import defaultdict
from threading import Event
from typing import Callable

from domain.types import GeneratedRecord
from generator.stores.base import BaseRouter
from generator.pipeline.base import Pipeline
from sinks.base import BaseSink


class GeneratorLoop:
    def __init__(
        self,
        step: Callable[[], GeneratedRecord],   # could be make_one for user, or step for session, where step handles transitons
        breaktime_generator: Callable[[], float],
        router: BaseRouter,
        pipeline: Pipeline | None = None,
    ):
        self.step = step
        self.breaktime_generator = breaktime_generator
        self.pipeline = pipeline
        self.router = router
        self.record_count = 0

        self.stop_event = Event()

    def _group_by_sink(
        self, records: list[GeneratedRecord]
    ) -> dict[BaseSink, list[GeneratedRecord]]:

        groups = defaultdict(list)

        for record in records:
            for sink in self.router.route(record):
                groups[sink].append(record)

        return groups

    def _process_records(
        self,
        records: list[GeneratedRecord]
    ) -> list[GeneratedRecord]:
        if self.pipeline:
            processed = []

            for record in records:
                processed.extend(
                    self.pipeline.run(record)
                )
        else:
            processed = records

        for sink, batch in self._group_by_sink(processed).items():
            sink.bulk_write(batch)

        return processed

    def bootstrap(self, n: int):
        records = [self.step() for _ in range(n)]

        self._process_records(records)

    def tick(self) -> None:
        record = self.step()

        records = self._process_records([record])

        self.record_count += len(records)

        if self.record_count % 100 == 0:
            print(f"{self.record_count} records processed")

    def run(self):
        while not self.stop_event.is_set():
            self.tick()

            breaktime = self.breaktime_generator()
            print(f"Wait for {breaktime} seconds...")

            self.stop_event.wait(breaktime)

    def stop(self):
        self.stop_event.set()
