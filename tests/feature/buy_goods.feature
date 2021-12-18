Feature: Buy goods
    A step where a player can buy goods

    Scenario: Buying a diamond
        Given I have less then 7 cards
        And A diamond is among the cards in the deck
        And It's my turn

        When I pick a diamond card

        Then I should see the bought diamond in my hand
