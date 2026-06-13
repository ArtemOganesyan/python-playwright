from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, then, when

from config import config


WAIT_TIMEOUT = config.timeouts.wait


def _page(world: dict[str, Page]) -> Page:
    return world["page"]


def _locator(page: Page, selector_type: str, selector: str):
    if selector_type == "xpath":
        return page.locator(f"xpath={selector}")
    if selector_type == "css":
        return page.locator(selector)
    raise ValueError(f"Unsupported selector type: {selector_type}")


def _product_card(page: Page, product_name: str):
    return page.locator(".product-item").filter(has_text=product_name).first


def _to_mouse_button(button: str) -> str:
    if button not in {"left", "right", "middle"}:
        raise ValueError(f"Unsupported mouse button: {button}")
    return button


@given(parsers.parse('I go to url "{url}"'))
def go_to_url(world: dict[str, Page], url: str):
    _page(world).goto(url)


@when("I reload the page")
def reload_page(world: dict[str, Page]):
    _page(world).reload()


@when("I go back")
def go_back(world: dict[str, Page]):
    _page(world).go_back()


@when("I go forward")
def go_forward(world: dict[str, Page]):
    _page(world).go_forward()


@when(parsers.parse('I click on element using {selector_type} "{selector}"'))
def click_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).click()


@when(parsers.parse('I double click on element using {selector_type} "{selector}"'))
def double_click_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).dblclick()


@when(parsers.parse('I right click on element using {selector_type} "{selector}"'))
def right_click_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).click(button="right")


@when(parsers.parse('I hover over element using {selector_type} "{selector}"'))
def hover_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).hover()


@when(parsers.parse('I fill element using {selector_type} "{selector}" with value "{value}"'))
def fill_element(world: dict[str, Page], selector_type: str, selector: str, value: str):
    _locator(_page(world), selector_type, selector).fill(value)


@when(parsers.parse('I type "{text}" into element using {selector_type} "{selector}"'))
def type_into_element(world: dict[str, Page], text: str, selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).type(text)


@when(parsers.parse('I clear element using {selector_type} "{selector}"'))
def clear_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).clear()


@when(parsers.parse('I focus on element using {selector_type} "{selector}"'))
def focus_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).focus()


@when(parsers.parse('I select option "{value}" from element using {selector_type} "{selector}"'))
def select_option(world: dict[str, Page], value: str, selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).select_option(value)


@when(parsers.parse('I select option by text "{text}" from element using {selector_type} "{selector}"'))
def select_option_by_text(world: dict[str, Page], text: str, selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).select_option(label=text)


@when(parsers.parse('I check element using {selector_type} "{selector}"'))
def check_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).check()


@when(parsers.parse('I uncheck element using {selector_type} "{selector}"'))
def uncheck_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).uncheck()


@when(parsers.parse('I scroll to element using {selector_type} "{selector}"'))
def scroll_to_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).scroll_into_view_if_needed()


@when(parsers.parse('I drag element using {source_type} "{source}" to element using {target_type} "{target}"'))
def drag_element(
    world: dict[str, Page],
    source_type: str,
    source: str,
    target_type: str,
    target: str,
):
    page = _page(world)
    _locator(page, source_type, source).drag_to(_locator(page, target_type, target))


@when(parsers.parse('I press "{key}" on element using {selector_type} "{selector}"'))
def press_on_element(world: dict[str, Page], key: str, selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).press(key)


@when(parsers.parse('I upload file "{file_path}" to element using {selector_type} "{selector}"'))
def upload_file(world: dict[str, Page], file_path: str, selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).set_input_files(file_path)


@when(parsers.parse('I wait for any element using {selector_type} "{selector}" to be visible'))
@then(parsers.parse('I should see any element using {selector_type} "{selector}"'))
def wait_for_visible(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).first.wait_for(state="visible", timeout=WAIT_TIMEOUT)


@when(parsers.parse('I wait for any element using {selector_type} "{selector}" to be hidden'))
@then(parsers.parse('I should not see any element using {selector_type} "{selector}"'))
def wait_for_hidden(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).first.wait_for(state="hidden", timeout=WAIT_TIMEOUT)


@when(parsers.parse('I wait for text "{text}" to appear in element using {selector_type} "{selector}"'))
def wait_for_text(world: dict[str, Page], text: str, selector_type: str, selector: str):
    expect(_locator(_page(world), selector_type, selector)).to_contain_text(text, timeout=WAIT_TIMEOUT)


@when("I accept the alert")
def accept_alert(world: dict[str, Page]):
    _page(world).on("dialog", lambda dialog: dialog.accept())


@when("I dismiss the alert")
def dismiss_alert(world: dict[str, Page]):
    _page(world).on("dialog", lambda dialog: dialog.dismiss())


@when(parsers.parse('I switch to frame using {selector_type} "{selector}"'))
def switch_to_frame(world: dict[str, Page], selector_type: str, selector: str):
    world["frame"] = _page(world).frame_locator(f"xpath={selector}" if selector_type == "xpath" else selector)


@when(parsers.parse("I set viewport size to {width:d} by {height:d}"))
def set_viewport_size(world: dict[str, Page], width: int, height: int):
    _page(world).set_viewport_size({"width": width, "height": height})


@when("I take a screenshot")
def take_screenshot(world: dict[str, Page]):
    _page(world).screenshot(path="screenshot.png")


@when("I take a full page screenshot")
def take_full_page_screenshot(world: dict[str, Page]):
    _page(world).screenshot(path="fullpage.png", full_page=True)


@when("I pause execution")
def pause_execution(world: dict[str, Page]):
    _page(world).pause()


@when(parsers.parse('I evaluate JavaScript "{script}"'))
def evaluate_javascript(world: dict[str, Page], script: str):
    _page(world).evaluate(script)


@when(parsers.parse('I set cookie "{name}" with value "{value}"'))
def set_cookie(world: dict[str, Page], name: str, value: str):
    _page(world).context.add_cookies([{"name": name, "value": value, "url": _page(world).url}])


@when("I clear cookies")
def clear_cookies(world: dict[str, Page]):
    _page(world).context.clear_cookies()


@when(parsers.parse('I set extra HTTP header "{name}" to "{value}"'))
def set_extra_http_header(world: dict[str, Page], name: str, value: str):
    _page(world).set_extra_http_headers({name: value})


@when(parsers.parse('I emulate media type "{media_type}"'))
def emulate_media_type(world: dict[str, Page], media_type: str):
    _page(world).emulate_media(media=media_type)


@when(parsers.parse("I set geolocation to latitude {latitude:g} longitude {longitude:g}"))
def set_geolocation(world: dict[str, Page], latitude: float, longitude: float):
    _page(world).context.set_geolocation({"latitude": latitude, "longitude": longitude})


@when(parsers.parse('I grant permission "{permission}"'))
def grant_permission(world: dict[str, Page], permission: str):
    _page(world).context.grant_permissions([permission])


@when(parsers.parse('I route "{url_pattern}" to respond with "{response_body}"'))
def route_response(world: dict[str, Page], url_pattern: str, response_body: str):
    _page(world).route(url_pattern, lambda route: route.fulfill(body=response_body))


@when(parsers.parse('I wait for request "{url_pattern}"'))
def wait_for_request(world: dict[str, Page], url_pattern: str):
    _page(world).wait_for_request(url_pattern)


@when(parsers.parse('I wait for response "{url_pattern}"'))
def wait_for_response(world: dict[str, Page], url_pattern: str):
    _page(world).wait_for_response(url_pattern)


@when(parsers.parse('I add script tag with url "{url}"'))
def add_script_tag_url(world: dict[str, Page], url: str):
    _page(world).add_script_tag(url=url)


@when(parsers.parse('I add script tag with content "{content}"'))
def add_script_tag_content(world: dict[str, Page], content: str):
    _page(world).add_script_tag(content=content)


@when(parsers.parse('I add style tag with url "{url}"'))
def add_style_tag_url(world: dict[str, Page], url: str):
    _page(world).add_style_tag(url=url)


@when(parsers.parse('I add style tag with content "{content}"'))
def add_style_tag_content(world: dict[str, Page], content: str):
    _page(world).add_style_tag(content=content)


@when(parsers.parse('I set local storage item "{key}" to "{value}"'))
def set_local_storage_item(world: dict[str, Page], key: str, value: str):
    _page(world).evaluate("([key, value]) => localStorage.setItem(key, value)", [key, value])


@when(parsers.parse('I set session storage item "{key}" to "{value}"'))
def set_session_storage_item(world: dict[str, Page], key: str, value: str):
    _page(world).evaluate("([key, value]) => sessionStorage.setItem(key, value)", [key, value])


@when(parsers.parse('I tap on element using {selector_type} "{selector}"'))
def tap_element(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).tap()


@when(parsers.parse('I take screenshot of element using {selector_type} "{selector}"'))
def take_element_screenshot(world: dict[str, Page], selector_type: str, selector: str):
    _locator(_page(world), selector_type, selector).screenshot(path="element.png")


@when(parsers.parse('I press keyboard key "{key}"'))
def press_keyboard_key(world: dict[str, Page], key: str):
    _page(world).keyboard.press(key)


@when(parsers.parse('I hold keyboard key "{key}"'))
def hold_keyboard_key(world: dict[str, Page], key: str):
    _page(world).keyboard.down(key)


@when(parsers.parse('I release keyboard key "{key}"'))
def release_keyboard_key(world: dict[str, Page], key: str):
    _page(world).keyboard.up(key)


@when(parsers.parse('I type "{text}" on page'))
def type_on_page(world: dict[str, Page], text: str):
    _page(world).keyboard.type(text)


@when(parsers.parse("I click at coordinates {x:d} {y:d}"))
def click_at_coordinates(world: dict[str, Page], x: int, y: int):
    _page(world).mouse.click(x, y)


@when(parsers.parse("I double click at coordinates {x:d} {y:d}"))
def double_click_at_coordinates(world: dict[str, Page], x: int, y: int):
    _page(world).mouse.dblclick(x, y)


@when(parsers.parse("I move mouse to coordinates {x:d} {y:d}"))
def move_mouse_to_coordinates(world: dict[str, Page], x: int, y: int):
    _page(world).mouse.move(x, y)


@when(parsers.parse('I press mouse button "{button}" down'))
def press_mouse_button_down(world: dict[str, Page], button: str):
    _page(world).mouse.down(button=_to_mouse_button(button))


@when(parsers.parse('I press mouse button "{button}" up'))
def press_mouse_button_up(world: dict[str, Page], button: str):
    _page(world).mouse.up(button=_to_mouse_button(button))


@when(parsers.parse("I wheel mouse by {delta_x:d} {delta_y:d}"))
def wheel_mouse(world: dict[str, Page], delta_x: int, delta_y: int):
    _page(world).mouse.wheel(delta_x, delta_y)


@when("I close the page")
def close_page(world: dict[str, Page]):
    _page(world).close()


@when("I bring page to front")
def bring_page_to_front(world: dict[str, Page]):
    _page(world).bring_to_front()


@when(parsers.parse('I set page content to "{html}"'))
def set_page_content(world: dict[str, Page], html: str):
    _page(world).set_content(html)


@when(parsers.parse('I wait for load state "{state}"'))
def wait_for_load_state(world: dict[str, Page], state: str):
    _page(world).wait_for_load_state(state)


@when(parsers.parse('I wait for function "{expression}"'))
def wait_for_function(world: dict[str, Page], expression: str):
    _page(world).wait_for_function(expression)


@when(parsers.parse("I wait for timeout in milliseconds {milliseconds:d}"))
def wait_for_timeout(world: dict[str, Page], milliseconds: int):
    _page(world).wait_for_timeout(milliseconds)


@then(parsers.parse('I should see element using {selector_type} "{selector}" contains "{text}"'))
def element_contains(world: dict[str, Page], selector_type: str, selector: str, text: str):
    assert text in (_locator(_page(world), selector_type, selector).text_content() or "")


@then(parsers.parse('I should see the page title is exactly "{expected_title}"'))
def title_is_exactly(world: dict[str, Page], expected_title: str):
    expect(_page(world)).to_have_title(expected_title, timeout=config.timeouts.expect)


@then(parsers.parse('I should see the current URL is exactly "{expected_url}"'))
def url_is_exactly(world: dict[str, Page], expected_url: str):
    expect(_page(world)).to_have_url(expected_url, timeout=config.timeouts.expect)


@then(parsers.parse('I should see element using {selector_type} "{selector}" has attribute "{attribute}" with value exactly "{value}"'))
def attribute_is_exactly(
    world: dict[str, Page],
    selector_type: str,
    selector: str,
    attribute: str,
    value: str,
):
    assert _locator(_page(world), selector_type, selector).get_attribute(attribute) == value


@then(parsers.parse('I should see element using {selector_type} "{selector}" is checked'))
def element_is_checked(world: dict[str, Page], selector_type: str, selector: str):
    assert _locator(_page(world), selector_type, selector).is_checked()


@then(parsers.parse('I should see element using {selector_type} "{selector}" is not checked'))
def element_is_not_checked(world: dict[str, Page], selector_type: str, selector: str):
    assert not _locator(_page(world), selector_type, selector).is_checked()


@then(parsers.parse('I should see element using {selector_type} "{selector}" is enabled'))
def element_is_enabled(world: dict[str, Page], selector_type: str, selector: str):
    assert _locator(_page(world), selector_type, selector).is_enabled()


@then(parsers.parse('I should see element using {selector_type} "{selector}" is disabled'))
def element_is_disabled(world: dict[str, Page], selector_type: str, selector: str):
    assert not _locator(_page(world), selector_type, selector).is_enabled()


@then(parsers.parse('I should see element using {selector_type} "{selector}" is visible'))
def element_is_visible(world: dict[str, Page], selector_type: str, selector: str):
    assert _locator(_page(world), selector_type, selector).is_visible()


@then(parsers.parse('I should see element using {selector_type} "{selector}" is hidden'))
def element_is_hidden(world: dict[str, Page], selector_type: str, selector: str):
    assert _locator(_page(world), selector_type, selector).is_hidden()


@then(parsers.parse('I should see element using {selector_type} "{selector}" inner text is exactly "{expected_text}"'))
def inner_text_is_exactly(world: dict[str, Page], selector_type: str, selector: str, expected_text: str):
    assert _locator(_page(world), selector_type, selector).inner_text() == expected_text


@then(parsers.parse('I should see element using {selector_type} "{selector}" inner HTML is exactly "{expected_html}"'))
def inner_html_is_exactly(world: dict[str, Page], selector_type: str, selector: str, expected_html: str):
    assert _locator(_page(world), selector_type, selector).inner_html() == expected_html


@then(parsers.parse('I should see element using {selector_type} "{selector}" text content is exactly "{expected_text}"'))
def text_content_is_exactly(world: dict[str, Page], selector_type: str, selector: str, expected_text: str):
    assert _locator(_page(world), selector_type, selector).text_content() == expected_text


@then(parsers.parse('I should see element using {selector_type} "{selector}" input value is exactly "{expected_value}"'))
def input_value_is_exactly(world: dict[str, Page], selector_type: str, selector: str, expected_value: str):
    assert _locator(_page(world), selector_type, selector).input_value() == expected_value


@then(parsers.parse('I should see element using {selector_type} "{selector}" count is exactly {expected_count:d}'))
def element_count_is_exactly(world: dict[str, Page], selector_type: str, selector: str, expected_count: int):
    assert _locator(_page(world), selector_type, selector).count() == expected_count


@then(parsers.parse('I should see local storage item "{key}" is exactly "{expected_value}"'))
def local_storage_is_exactly(world: dict[str, Page], key: str, expected_value: str):
    assert _page(world).evaluate("(key) => localStorage.getItem(key)", key) == expected_value


@then(parsers.parse('I should see session storage item "{key}" is exactly "{expected_value}"'))
def session_storage_is_exactly(world: dict[str, Page], key: str, expected_value: str):
    assert _page(world).evaluate("(key) => sessionStorage.getItem(key)", key) == expected_value


@then(parsers.parse('I should see cookie "{name}" value is exactly "{expected_value}"'))
def cookie_value_is_exactly(world: dict[str, Page], name: str, expected_value: str):
    cookies: list[dict[str, Any]] = _page(world).context.cookies()
    cookie = next((item for item in cookies if item["name"] == name), None)
    assert cookie is not None
    assert cookie["value"] == expected_value


@then(parsers.parse('I should see the page title contains "{expected_title}"'))
def title_contains(world: dict[str, Page], expected_title: str):
    expect(_page(world)).to_have_title(re.compile(f".*{re.escape(expected_title)}.*"), timeout=config.timeouts.expect)


@then(parsers.parse('I should see the current URL contains "{expected_url}"'))
def url_contains(world: dict[str, Page], expected_url: str):
    expect(_page(world)).to_have_url(re.compile(f".*{re.escape(expected_url)}.*"), timeout=config.timeouts.expect)


@then(parsers.parse('I should see element using {selector_type} "{selector}" has attribute "{attribute}" contains "{value}"'))
def attribute_contains(
    world: dict[str, Page],
    selector_type: str,
    selector: str,
    attribute: str,
    value: str,
):
    assert value in (_locator(_page(world), selector_type, selector).get_attribute(attribute) or "")


@then(parsers.parse('I should see element using {selector_type} "{selector}" inner text contains "{expected_text}"'))
def inner_text_contains(world: dict[str, Page], selector_type: str, selector: str, expected_text: str):
    assert expected_text in _locator(_page(world), selector_type, selector).inner_text()


@then(parsers.parse('I should see element using {selector_type} "{selector}" inner HTML contains "{expected_html}"'))
def inner_html_contains(world: dict[str, Page], selector_type: str, selector: str, expected_html: str):
    assert expected_html in _locator(_page(world), selector_type, selector).inner_html()


@then(parsers.parse('I should see element using {selector_type} "{selector}" input value contains "{expected_value}"'))
def input_value_contains(world: dict[str, Page], selector_type: str, selector: str, expected_value: str):
    assert expected_value in _locator(_page(world), selector_type, selector).input_value()


@then(parsers.parse('I should see product "{product_name}" with price "{expected_price}"'))
def product_with_price(world: dict[str, Page], product_name: str, expected_price: str):
    card = _product_card(_page(world), product_name)
    expect(card).to_be_visible(timeout=WAIT_TIMEOUT)
    expect(card.locator(".product-title")).to_contain_text(product_name, timeout=config.timeouts.expect)
    expect(card.locator(".price.actual-price")).to_have_text(expected_price, timeout=config.timeouts.expect)


@when(parsers.parse('I open product "{product_name}"'))
def open_product(world: dict[str, Page], product_name: str):
    card = _product_card(_page(world), product_name)
    expect(card).to_be_visible(timeout=WAIT_TIMEOUT)
    card.locator(".product-title a").click()


@then(parsers.parse('I should see product details for "{product_name}"'))
def product_details_for(world: dict[str, Page], product_name: str):
    expect(_page(world).locator(".product-name")).to_have_text(product_name, timeout=config.timeouts.expect)


@then(parsers.parse('I should see product detail price "{expected_price}"'))
def product_detail_price(world: dict[str, Page], expected_price: str):
    expect(_page(world).locator(".product-price")).to_have_text(expected_price, timeout=config.timeouts.expect)


@given("I open the nopCommerce demo store")
def open_nopcommerce_demo_store(world: dict[str, Page]):
    _page(world).goto("https://nop-qa.portnov.com/")


@then("the nopCommerce home page is displayed")
def nopcommerce_home_page_is_displayed(world: dict[str, Page]):
    page = _page(world)
    expect(page).to_have_title(re.compile(".*Your store.*"), timeout=config.timeouts.expect)
    expect(page.locator(".topic-block-title")).to_contain_text("Welcome to our store", timeout=config.timeouts.expect)


@then("the featured products list has four items")
def featured_products_list_has_four_items(world: dict[str, Page]):
    expect(_page(world).locator(".product-item")).to_have_count(4, timeout=config.timeouts.expect)


@then("the featured products show the expected demo prices")
def featured_products_show_expected_demo_prices(world: dict[str, Page]):
    expected_products = {
        "Build your own computer": "$1,200.00",
        "Apple MacBook Pro 13-inch": "$1,800.00",
        "HTC One M8 Android L 5.0 Lollipop": "$245.00",
        "$25 Virtual Gift Card": "$25.00",
    }
    for product_name, expected_price in expected_products.items():
        product_with_price(world, product_name, expected_price)


@when("I open the Apple MacBook product page")
def open_apple_macbook_product_page(world: dict[str, Page]):
    open_product(world, "Apple MacBook Pro 13-inch")


@then("the Apple MacBook product details are displayed")
def apple_macbook_product_details_are_displayed(world: dict[str, Page]):
    page = _page(world)
    expect(page).to_have_title(re.compile(".*Apple MacBook Pro 13-inch.*"), timeout=config.timeouts.expect)
    product_details_for(world, "Apple MacBook Pro 13-inch")


@then("the Apple MacBook price and availability are correct")
def apple_macbook_price_and_availability_are_correct(world: dict[str, Page]):
    product_detail_price(world, "$1,800.00")
    expect(_page(world).locator(".availability")).to_contain_text("In stock", timeout=config.timeouts.expect)


@when("I search the store for computer")
def search_store_for_computer(world: dict[str, Page]):
    page = _page(world)
    page.goto("https://nop-qa.portnov.com/")
    page.locator("#small-searchterms").fill("computer")
    page.keyboard.press("Enter")


@then("the computer search results are displayed")
def computer_search_results_are_displayed(world: dict[str, Page]):
    page = _page(world)
    expect(page).to_have_url(re.compile(".*search.*"), timeout=config.timeouts.expect)
    expect(page.locator(".product-item").first).to_be_visible(timeout=WAIT_TIMEOUT)


@then("the search results include Build your own computer with the expected price")
def search_results_include_build_your_own_computer(world: dict[str, Page]):
    product_with_price(world, "Build your own computer", "$1,200.00")


@then(parsers.parse('I should see local storage item "{key}" contains "{expected_value}"'))
def local_storage_contains(world: dict[str, Page], key: str, expected_value: str):
    value = _page(world).evaluate("(key) => localStorage.getItem(key)", key)
    assert expected_value in (value or "")


@then(parsers.parse('I should see session storage item "{key}" contains "{expected_value}"'))
def session_storage_contains(world: dict[str, Page], key: str, expected_value: str):
    value = _page(world).evaluate("(key) => sessionStorage.getItem(key)", key)
    assert expected_value in (value or "")


@then(parsers.parse('I should see cookie "{name}" value contains "{expected_value}"'))
def cookie_value_contains(world: dict[str, Page], name: str, expected_value: str):
    cookies: list[dict[str, Any]] = _page(world).context.cookies()
    cookie = next((item for item in cookies if item["name"] == name), None)
    assert cookie is not None
    assert expected_value in cookie["value"]


@when(parsers.parse('I wait for element using {selector_type} "{selector}" to be interactable'))
def wait_for_interactable(world: dict[str, Page], selector_type: str, selector: str):
    locator = _locator(_page(world), selector_type, selector)
    locator.wait_for(state="visible", timeout=WAIT_TIMEOUT)
    expect(locator).to_be_enabled(timeout=WAIT_TIMEOUT)


@when("I wait for new popup to open")
def wait_for_new_popup(world: dict[str, Page]):
    world["popup"] = _page(world).wait_for_event("popup")


@when("I wait for new tab to open")
def wait_for_new_tab(world: dict[str, Page]):
    world["new_page"] = _page(world).context.wait_for_event("page")


@then("I should see a new tab has opened")
def new_tab_opened(world: dict[str, Page]):
    assert len(_page(world).context.pages) > 1


@when("I switch to new tab")
def switch_to_new_tab(world: dict[str, Page]):
    pages = _page(world).context.pages
    assert len(pages) > 1
    world["page"] = pages[-1]
    _page(world).wait_for_load_state()
    _page(world).bring_to_front()


@when("I wait for new tab and switch to it")
def wait_for_new_tab_and_switch(world: dict[str, Page]):
    new_page = _page(world).context.wait_for_event("page")
    world["page"] = new_page
    _page(world).wait_for_load_state()
    _page(world).bring_to_front()


@when(parsers.parse('I switch to tab with title "{title}"'))
def switch_to_tab_with_title(world: dict[str, Page], title: str):
    for candidate in _page(world).context.pages:
        if candidate.title() == title:
            world["page"] = candidate
            _page(world).bring_to_front()
            return
    raise AssertionError(f'Tab with title "{title}" not found')


@when(parsers.parse('I create file "{path}" with content "{content}"'))
def create_file(path: str, content: str):
    Path(path).write_text(content, encoding="utf-8")
