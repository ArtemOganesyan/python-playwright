@bdd
Feature: nopCommerce demo catalog

  @bdd1
  Scenario: Featured products, product details, and search
    Given I open the nopCommerce demo store
    Then the nopCommerce home page is displayed
    Then the featured products list has four items
    Then the featured products show the expected demo prices

    When I open the Apple MacBook product page
    Then the Apple MacBook product details are displayed
    Then the Apple MacBook price and availability are correct

    When I search the store for computer
    Then the computer search results are displayed
    Then the search results include Build your own computer with the expected price
