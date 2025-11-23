import typing as tp

import pytest
import pytest_asyncio

from textual_demo.main import (
    StopWatchApp,
    StopWatch,
    TimeDisplay,
    START_BTN_ID,
    STOP_BTN_ID,
    RESET_BTN_ID,
)

if tp.TYPE_CHECKING:
    from textual.pilot import Pilot


@pytest_asyncio.fixture
async def pilot() -> tp.AsyncGenerator["Pilot[StopWatchApp]", None]:
    app = StopWatchApp()
    async with app.run_test() as _pilot:  # type: ignore
        yield _pilot


@pytest.mark.asyncio
async def test_keys(pilot: "Pilot[StopWatchApp]"):
    app = pilot.app
    # App launches with one StopWatch widget
    assert len(app.query(StopWatch)) == 1

    # Let's add one StopWatch
    await pilot.press("a")
    assert len(app.query(StopWatch)) == 2

    # Let's remove one StopWatch
    await pilot.press("r")
    assert len(app.query(StopWatch)) == 1


@pytest.mark.asyncio
async def test_stopwatch(pilot: "Pilot[StopWatchApp]"):
    app = pilot.app
    time_display = app.query_one(TimeDisplay)
    assert time_display.value == "00:00:00.00"

    await pilot.click(f"#{START_BTN_ID}")
    await pilot.pause(0.1)
    await pilot.click(f"#{STOP_BTN_ID}")
    assert time_display.value != "00:00:00.00"

    await pilot.click(f"#{RESET_BTN_ID}")
    assert time_display.value == "00:00:00.00"
