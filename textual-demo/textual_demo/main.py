from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Button, Digits

LIGHT_THEME = "textual-light"
DARK_THEME = "textual-dark"

START_BTN_ID = "start"
STOP_BTN_ID = "stop"
RESET_BTN_ID = "reset"


class TimeDisplay(Digits):
    start_time = reactive(monotonic)  # type: ignore
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time = self.total + monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.time = 0
        self.total = 0


class StopWatch(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Start", id=START_BTN_ID, variant="success")
        yield Button("Stop", id=STOP_BTN_ID, variant="error")
        yield Button("Restart", id=RESET_BTN_ID)
        yield TimeDisplay()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == START_BTN_ID:
            time_display.start()
            self.add_class("started")
        elif button_id == STOP_BTN_ID:
            time_display.stop()
            self.remove_class("started")
        elif button_id == RESET_BTN_ID:
            time_display.reset()


class StopWatchApp(App):
    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(StopWatch(), id="timers")

    def action_add_stopwatch(self) -> None:
        new_stopwatch = StopWatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        timers = self.query(StopWatch)
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME


def main() -> None:
    app = StopWatchApp()
    app.run()


if __name__ == "__main__":
    main()
