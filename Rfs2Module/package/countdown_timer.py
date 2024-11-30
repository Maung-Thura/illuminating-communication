import threading
import time
import asyncio

class CountdownTimer(threading.Thread):
    def __init__(self, duration, callback=None):
        """
        Initialize the countdown timer.
        :param duration: Countdown duration in seconds.
        :param callback: Function to call when countdown reaches zero.
        """
        super().__init__()
        self.duration = duration
        self.callback = callback  # Store the callback function
        self.running = True

    def run(self):
        """Executes the countdown."""
        while self.duration > 0 and self.running:
            mins, secs = divmod(self.duration, 60)
            print(f"Time left: {mins:02}:{secs:02}", end="\r")
            time.sleep(1)
            self.duration -= 1

        if self.running:
            print("\nCountdown complete!")
            if self.callback:  # Trigger the callback if it's provided
                asyncio.run(self.callback())
        else:
            print("\nCountdown stopped.")

    def stop(self):
        """Stops the countdown."""
        self.running = False
        print("\nCountdown stopped.")
