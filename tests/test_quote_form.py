from config import config


def test_should_fill_out_and_verify_required_fields_on_quote_form(page):
    # The upstream TypeScript project contains this test as an empty scaffold.
    page.goto(config.test_data.quote_base_url)
    assert page.title()

