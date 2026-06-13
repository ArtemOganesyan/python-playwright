import pytest
import re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width":1440,"height":1000}}


def test_example(page: Page) -> None:
    page.goto("https://nop-qa.portnov.com/")
    page.get_by_role("link", name="Jewelry").click()
    page.get_by_role("button", name="Add to cart").nth(1).click()
