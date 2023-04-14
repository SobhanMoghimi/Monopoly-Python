import time

from Board import Board
from Enums import PropertyTypeEnum
from ConsoleLog import ConsoleLog
from Property import Property


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.balance = 1500
        self.owned_property_list = []
        self.prison_time = 0
        self.doubled_dice_times = 0
        self.is_visiting = False

    def net_worth(self, props) -> int:
        return self.balance + sum(
            [props[_property.cell_number - 1].price for _property in self.owned_property_list]) + sum(
            [props[_property.cell_number - 1].rent for _property in self.owned_property_list])

    def move_player(self, steps: int):
        self.position = (self.position + steps)
        if self.position >= 37:
            self.balance += 200
            self.position %= 37
            time.sleep(0.8)
            print("Congrats! {} Got $200 for moving on the GO property.", self.name)

    def pay_rent(self, rent, owner):
        self.balance -= rent
        owner.balance += rent

    def apply_tax(self, tax_type):
        if tax_type == PropertyTypeEnum.INCOME_TAX:
            self.balance -= 200
            print("{} Landed on {}. ${} was paid for tax.".format(self.name, tax_type, 200))
        elif tax_type == PropertyTypeEnum.SUPER_TAX:
            self.balance -= 100
            print("{} Landed on {}. ${} was paid for tax.".format(self.name, tax_type, 100))

    def is_defeated(self):
        return self.balance < 0

    def go_to_jail(self):
        self.position = 10
        self.prison_time = 1

    def handle_jail(self):
        if self.prison_time == 0:
            print("Sorry! You're landed on jail...\n"
                  "Enter your choice:\n"
                  "1.Get out of jail for $50.\n"
                  "2.Stay in jail for 3 rounds unless you make a double.\n")
            while True:
                input_choice = input()
                if input_choice == '1':
                    self.get_out_of_jail_for_money()
                    break
                if input_choice == '2':
                    print("Staying in jail...")
                    break
                else:
                    print("Wrong Input. Try Again:")
        elif self.prison_time <= 2:
            print("Sorry! You're still in jail for more {} rounds.\n", 3 - self.prison_time)
            self.prison_time += 1
        else:
            self.get_out_of_jail()

    def get_out_of_jail_for_money(self):
        self.balance -= 50
        self.prison_time = 0
        print("Got out of jail for $50...\n")

    def get_out_of_jail(self):
        print("Congrats! You got out of prison after three failed attempts. Just visiting...")
        self.prison_time = 0

    def buy_property(self, new_property):
        if self.balance >= new_property.price:
            new_property.owner = self
            self.owned_property_list.append(new_property)
            self.balance -= new_property.price
            if new_property.property_type != PropertyTypeEnum.AIRPORT:
                self.check_bought_a_country(new_property.country)
            print("Bought {} for ${}.".format(new_property.name, new_property.price))
            return True
        else:
            print("Your balance is lower than the expected balance for this action!")
            return False

    def check_bought_a_country(self, new_country) -> bool:
        owned_properties_of_the_country = 0
        for _property in self.owned_property_list:
            if _property.country == new_country:
                owned_properties_of_the_country += 1

        number_of_cities_in_a_country = Board.number_of_cities_in_a_country(new_country)

        if number_of_cities_in_a_country == owned_properties_of_the_country:
            print("Congrats {}. You bought {}."
                  " You can now upgrade cities of this country.".format(self.name, new_country))
            Board.upgrade_cities_to_upgradable(new_country)
            return True
        return False

    def add_balance(self, money: int):
        self.balance += money

    def check_positive_balance(self):
        if self.balance >= 0:
            return
        else:
            print("Your balance is less that zero; Sell properties to avoid bankruptcy.")

    def work_with_properties(self):
        print("You're Balance is {}.\n".format(self.balance))
        while True:
            input_choice = input("Enter 1 to check properties or 0 to pass: ")
            if input_choice == '0':
                break
            elif input_choice == '1':
                if self.owned_property_list:
                    self.print_owned_properties()

                    while True:
                        property_chosen = input("Enter a property number to select: or 0 to pass: ")
                        if property_chosen == '0':
                            break
                        else:
                            try:
                                self.work_with_a_property(int(property_chosen))
                            except Exception as e:
                                print("Input Error!", e)

                else:
                    print("No properties yet...")
            else:
                print("Wrong input. Try Again...")

    def work_with_a_property(self, property_index: int):
        print("You're Balance is {}.\n".format(self.balance))
        working_property = None
        for _property in self.owned_property_list:
            if _property.cell_number == property_index:
                working_property = _property
                break
        if not working_property:
            raise Exception("Not found")

        options = ["0.Exit"]
        options_numbers = ["0"]
        if working_property.is_upgradable:
            options.append("1.Upgrade")
            options_numbers.append("1")
        if working_property.buildings_count > 0:
            options.append("2.Downgrade")
            options_numbers.append("2")
        elif not working_property.is_upgradable:
            flag = True
            for _property in self.owned_property_list:
                if _property.country == working_property.country:
                    if _property.buildings_count > 0:
                        # print("You can't sell a property with more than 1 building in other cities of same country!")
                        flag = False
            if flag:
                options.append("4.Sell")
                options_numbers.append("4")

            # options.append("3.Mortgage")
            # options_numbers.append("3")
        print("Selected Property:\n" + str(working_property))
        print("Options: \n")
        for option in options:
            print(option)
        while True:
            action = input("Choose option: ")
            if action == '0':
                print("Exiting...\n")
                time.sleep(1)
                break
            elif action not in options_numbers:
                print("Wrong Input! Try again.")
                continue
            else:
                if action == '1':
                    self.upgrade_property(working_property)
                elif action == '2':
                    self.downgrade_property(working_property)
                # if action == '3':
                #     self.mortgage_property(working_property)
                elif action == '4':
                    self.sell_property(working_property)

    def upgrade_property(self, input_property: Property):
        if self.balance > input_property.price / 2:
            if input_property.buildings_count > 3:
                print("You can't upgrade a property with more than 3 buildings!")
                return False
            else:
                upgrade_cost = input_property.price / 2
                self.balance -= upgrade_cost
                input_property.upgrade()
                print("Upgraded {} for ${}.".format(input_property.name, upgrade_cost))
                return True
        else:
            print("Your balance is lower than the expected balance for this action!")
            return False

    def downgrade_property(self, input_property: Property):
        if input_property.buildings_count <= 0:
            print("You can't downgrade a property with less than 1 building!")
            return False
        else:
            downgrade_price = (input_property.price // 3) / 2
            self.balance += downgrade_price
            input_property.downgrade()
            print("Downgraded {} for ${}.".format(input_property.name, downgrade_price))
            return True

    def sell_property(self, input_property: Property):
        if input_property.buildings_count > 0:
            print("You can't sell a property with more than 1 building!")
            return False
        else:
            sell_price = input_property.price
            self.balance += sell_price
            input_property.sell()
            self.owned_property_list.remove(input_property)
            print("Sold {} for ${}.".format(input_property.name, sell_price))
            Board.change_cities_to_not_upgradable(input_property.country)

    def print_owned_properties(self):
        for owned_property in self.owned_property_list:
            print(owned_property)

    # def handle_negative_balance(self):
    #     # todo: change!
    #     while self.balance < 0:
    #         print("Select a property to sell, downgrade or mortgage")
    #         i = 0
    #         for owned_property in self.owned_property_list:
    #             print('property{} = ' + owned_property, i)
    #             i += 1
    #         while i > len(self.owned_property_list) or i < 0:
    #             input_property = int(input(""))
    #             if input_property < 0 or input_property >= len(self.owned_property_list):
    #                 ConsoleLog.print_invalid_input()

    def set_doubled_dice_times(self, times: int) -> None:
        self.doubled_dice_times = times

    def check_doubled_dice_times(self):
        if self.doubled_dice_times >= 3:
            print("You have doubled the dice for {} rounds.\n Now you go to Jail!", self.doubled_dice_times)
            self.position = 11  # position of jail
            self.doubled_dice_times = 0
            self.prison_time = 1

    def just_visiting(self):
        print("{} landed on {}".format(self.name, "JUST_VISITING"))

    def land_on_property(self, landed_property):
        print("{} landed on {}.".format(self.name, landed_property.name))
        if landed_property.owner:
            if landed_property.owner is not self:
                print("Sorry, this property is owned by Agent.")
                if landed_property.is_mortgaged:
                    print("No Rent needed!")
                else:
                    print("Paying rent...")
                self.pay_rent(rent=landed_property.rent, owner=landed_property.owner)
            else:
                print("This property is yours.")
        else:
            print("This property doesn't belong to anybody.\n" + str(landed_property) +
                  "\nChoose action:\n"
                  "1. Buy the property...\n"
                  "2. Go to next action...")
            while True:
                input_choice = input()
                if input_choice == '1':
                    self.buy_property(landed_property)
                    break
                elif input_choice == '2':
                    break
                else:
                    print("Wrong output. Try Again: \n"
                          "1. Buy the property...\n"
                          "2. Go to next action...")

    def land_on_airport(self, landed_airport):
        print("{} landed on {}.".format(self.name, landed_airport.name))
        if landed_airport.owner:
            if landed_airport.owner is not self:
                print("Sorry, this property is owned by Agent.")
                if landed_airport.is_mortgaged:
                    print("No Rent needed!")
                else:
                    print("Paying rent...")
                self.pay_rent(rent=landed_airport.rent, owner=landed_airport.owner)
            else:
                print("This property is yours.")
        else:
            print("This property doesn't belong to anybody.\n" + str(landed_airport) +
                  "\nChoose action:\n"
                  "1. Buy the property...\n"
                  "2. Go to next action...")
            while True:
                input_choice = input()
                if input_choice == '1':
                    self.buy_property(landed_airport)
                    break
                elif input_choice == '2':
                    break
                else:
                    print("Wrong output. Try Again: \n"
                          "1. Buy the property...\n"
                          "2. Go to next action...")
