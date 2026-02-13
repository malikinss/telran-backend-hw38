# ./src/utils/thinking_dots.py

import sys
import time
import threading


class ThinkingDots:
    """
    Displays a "thinking..." animation in the console using dots.

    The animation runs in a background thread, printing a dot
    at regular intervals until stopped.

    Example:
        td = ThinkingDots("Processing")
        td.start()
        do_some_long_task()
        td.stop()
    """

    def __init__(self, label: str, interval: float = 0.5) -> None:
        """
        Initialize the ThinkingDots animation.

        Args:
            label: Text displayed before the dots (e.g., "Processing").
            interval: Seconds between printing each dot (default 0.5s).
        """
        self.label = label
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def _worker(self) -> None:
        """
        Worker function running in a separate thread that prints dots.

        Prints a dot every `interval` seconds. After 20 dots, starts a new
        line and reprints the label. Stops when `_stop_event` is set.
        """
        sys.stdout.write(self.label)
        sys.stdout.flush()
        dots = 0

        while not self._stop_event.is_set():
            sys.stdout.write(".")
            sys.stdout.flush()
            dots += 1
            if dots % 20 == 0:
                sys.stdout.write("\n" + self.label)
                sys.stdout.flush()
            time.sleep(self.interval)

    def start(self) -> None:
        """
        Start the thinking dots animation in a background thread.

        Does nothing if the animation is already running.
        """
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the thinking dots animation and wait for the thread to finish.

        If the animation was not running, this method does nothing.
        """
        if not self._thread or not self._thread.is_alive():
            return

        self._stop_event.set()
        self._thread.join()

        sys.stdout.write("\n")
        sys.stdout.flush()
