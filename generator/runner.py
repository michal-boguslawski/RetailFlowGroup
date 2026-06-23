from numpy.random import gamma
from threading import Thread

from config.loader import load_config
from generator.core.loop import GeneratorLoop
from generator.builders.alpha_builder import AlphaBuilder
from generator.session.handlers.loader import load_handlers
from infrastructure.kafka.factory import build_kafka_config
from infrastructure.kafka.admin import KafkaAdminClient


if __name__ == "__main__":
    load_handlers()
    config = load_config("alpha")
    kafka_config = build_kafka_config(config.store_id)

    alpha_builder = AlphaBuilder()
    alpha_factory = alpha_builder.build_factory(config)
    alpha_router = alpha_builder.build_router(config)
    alpha_event_handler = alpha_builder.build_handler(config)

    admin_client = KafkaAdminClient(kafka_config)
    admin_client.ensure_topics()

    user_loop = GeneratorLoop(
        step=lambda: alpha_factory.make_one("users"),
        breaktime_generator=lambda: gamma(10, 2),
        router=alpha_router,
        pipeline=None,
    )

    events_loop = GeneratorLoop(
        step=lambda: alpha_event_handler.step(),
        breaktime_generator=lambda: gamma(0.5, 0.5),
        router=alpha_router,
        pipeline=None,
    )
    # user_loop.bootstrap(10)

    loops = [user_loop, events_loop]
    threads = [Thread(target=loop.run, daemon=True) for loop in loops]

    for t in threads:
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            for t in threads:
                t.join(timeout=0.5)

    except KeyboardInterrupt:
        print("Stopping...")

        for loop in loops:
            loop.stop()

        for t in threads:
            t.join()

        print("Stopped")
    