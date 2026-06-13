"""Centralized project configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value.split("#", 1)[0].strip())


def _str(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.split("#", 1)[0].strip()


@dataclass(frozen=True)
class BrowserConfig:
    name: str
    headless: bool
    slow_mo: int
    viewport_width: int
    viewport_height: int
    window_position_x: int
    window_position_y: int

    @property
    def viewport(self) -> dict[str, int]:
        return {"width": self.viewport_width, "height": self.viewport_height}


@dataclass(frozen=True)
class TimeoutConfig:
    global_timeout: int
    action: int
    navigation: int
    expect: int
    wait: int


@dataclass(frozen=True)
class TestDataConfig:
    quote_base_url: str
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class OtherConfig:
    debug: bool
    ci: bool


@dataclass(frozen=True)
class Config:
    browser: BrowserConfig
    timeouts: TimeoutConfig
    test_data: TestDataConfig
    other: OtherConfig


config = Config(
    browser=BrowserConfig(
        name=_str("BROWSER", "chromium").lower(),
        headless=_bool("HEADLESS", False),
        slow_mo=_int("SLOW_MO", 0),
        viewport_width=_int("VIEWPORT_WIDTH", 1920),
        viewport_height=_int("VIEWPORT_HEIGHT", 1080),
        window_position_x=_int("WINDOW_POSITION_X", 0),
        window_position_y=_int("WINDOW_POSITION_Y", 0),
    ),
    timeouts=TimeoutConfig(
        global_timeout=_int("GLOBAL_TIMEOUT", 30000),
        action=_int("ACTION_TIMEOUT", 5000),
        navigation=_int("NAVIGATION_TIMEOUT", 30000),
        expect=_int("EXPECT_TIMEOUT", 5000),
        wait=_int("WAIT_TIMEOUT", 10000),
    ),
    test_data=TestDataConfig(
        quote_base_url=_str("TEST_QUOTE_BASE_URL", "https://skryabin.com/market/quote.html"),
        username=_str("TEST_USERNAME", "jdoe"),
        email=_str("TEST_EMAIL", "jdoe@example.com"),
        password=_str("TEST_PASSWORD", "Pass123!"),
        first_name=_str("TEST_FIRST_NAME", "John"),
        last_name=_str("TEST_LAST_NAME", "Doe"),
    ),
    other=OtherConfig(
        debug=_bool("DEBUG", False),
        ci=bool(os.getenv("CI")),
    ),
)

