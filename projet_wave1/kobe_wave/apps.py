from django.apps import AppConfig

class KobeWaveConfig(AppConfig):
    name = "kobe_wave"

    def ready(self):
        import threading
        from kobe_wave import precompute
        t = threading.Thread(target=precompute.precompute, daemon=True)
        t.start()
