from kubernetes.main import App

def create_app() -> App:
    """Create a FastAPI app."""
    app = App()
    return app
