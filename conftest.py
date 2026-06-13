"""Pytest and Playwright fixtures shared by classic and BDD tests."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config import config


REPORTS_DIR = Path("test-reports")
VIDEOS_DIR = REPORTS_DIR / "videos"


def _launch_args(browser_name: str) -> list[str]:
    base_args: list[str] = []
    if browser_name == "chromium":
        base_args.extend(
            [
                "--disable-web-security",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ]
        )
    elif browser_name == "firefox":
        base_args.append("--disable-web-security")

    if browser_name == "firefox" and not config.browser.headless:
        return base_args

    return [
        *base_args,
        f"--window-position={config.browser.window_position_x},{config.browser.window_position_y}",
        f"--window-size={config.browser.viewport_width},{config.browser.viewport_height}",
    ]


@pytest.fixture(scope="session", autouse=True)
def global_setup_and_teardown() -> Generator[None, None, None]:
    REPORTS_DIR.mkdir(exist_ok=True)
    yield
    for directory in (Path("temp"), Path("downloads")):
        shutil.rmtree(directory, ignore_errors=True)
    print(f"Completed at: {datetime.now(timezone.utc).isoformat()}")


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    with sync_playwright() as playwright:
        browser_name = config.browser.name
        if browser_name not in {"chromium", "firefox", "webkit"}:
            browser_name = "chromium"

        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(
            headless=config.browser.headless,
            slow_mo=config.browser.slow_mo,
            args=_launch_args(browser_name),
            ignore_default_args=["--disable-extensions"],
        )
        yield browser
        browser.close()


@pytest.fixture()
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport=config.browser.viewport,
        permissions=["geolocation"],
        geolocation={"longitude": -122.4194, "latitude": 37.7749},
        locale="en-US",
        timezone_id="America/Los_Angeles",
        ignore_https_errors=True,
        record_video_dir=str(VIDEOS_DIR),
        record_video_size=config.browser.viewport,
    )
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    page.set_default_timeout(config.timeouts.global_timeout)
    page.set_default_navigation_timeout(config.timeouts.navigation)
    yield page
    if not page.is_closed():
        page.close()


@pytest.fixture()
def world(page: Page) -> dict[str, Page]:
    return {"page": page}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "page" in item.fixturenames:
        page = item.funcargs.get("page")
        if page and not page.is_closed():
            screenshots_dir = REPORTS_DIR / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot = screenshots_dir / f"{item.name}.png"
            page.screenshot(path=str(screenshot), full_page=True)
