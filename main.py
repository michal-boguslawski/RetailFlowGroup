def main():
    mode = os.getenv("MODE", "generator")

    if mode == "generator":
        from generator.runner import run_generator
        run_generator()

    elif mode == "pipeline":
        from ingestion.streaming import run_pipeline
        run_pipeline()

    elif mode == "bootstrap":
        from bootstrap.seed import run_bootstrap
        run_bootstrap()
