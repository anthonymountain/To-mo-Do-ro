import time
from plyer import notification


def timer(work_time=25, break_time=5):
    """Run a Pomodoro session."""
    print(f"Work session started! Focus for {work_time} minutes.")
    time.sleep(work_time * 60)
    notification.notify(
        title="Pomodoro Timer",
        message="Time's up! Take a 5-minute break.",
        timeout=10
    )

    print(f"Break session started! Relax for {break_time} minutes.")
    time.sleep(break_time * 60)
    notification.notify(
        title="Pomodoro Timer",
        message="Break over! Back to work.",
        timeout=10
    )
