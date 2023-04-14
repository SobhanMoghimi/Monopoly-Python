from Enums import PropertyTypeEnum, CountryTypeEnum
from Property import Property


class Board:
    jail_address = 11

    board = [
        Property(cell_number=1, name="GO", property_type=PropertyTypeEnum.GO),
        Property(cell_number=2, name="Rio", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.BRAZIL,
                 price=60, rent=2),
        Property(cell_number=3, name="Community Chest", property_type=PropertyTypeEnum.CHEST),
        Property(cell_number=4, name="Salvador", property_type=PropertyTypeEnum.LANDMARK,
                 country=CountryTypeEnum.BRAZIL, price=40, rent=6),
        Property(cell_number=5, name="Income Tax", property_type=PropertyTypeEnum.INCOME_TAX),
        Property(cell_number=6, name="Rio Airport", property_type=PropertyTypeEnum.AIRPORT, price=200, rent=25),

        Property(cell_number=7, name="Amol", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.IRAN,
                 price=100, rent=6),
        Property(cell_number=8, name="Community Chest", property_type=PropertyTypeEnum.CHEST),
        Property(cell_number=9, name="Tehran", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.IRAN,
                 price=100, rent=6),
        Property(cell_number=10, name="Qazvin", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.IRAN,
                 price=120, rent=8),
        Property(cell_number=11, name="Jail / Just Visiting", property_type=PropertyTypeEnum.JAIL),

        Property(cell_number=12, name="Padova", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.ITALY, price=140, rent=10),
        Property(cell_number=13, name="Milan", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.ITALY, price=140, rent=10),
        Property(cell_number=14, name="Turin", property_type=PropertyTypeEnum.LANDMARK,country=CountryTypeEnum.ITALY, price=160,
                 rent=14),

        Property(cell_number=15, name="Milan Airport", property_type=PropertyTypeEnum.AIRPORT, price=200, rent=25),
        Property(cell_number=16, name="Frankfurt", property_type=PropertyTypeEnum.LANDMARK,country=CountryTypeEnum.GERMANY, price=180, rent=14),
        Property(cell_number=17, name="Community Chest", property_type=PropertyTypeEnum.CHEST),
        Property(cell_number=18, name="Berlin", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.GERMANY, price=180, rent=14),
        Property(cell_number=19, name="Munich", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.GERMANY, price=200, rent=16),

        Property(cell_number=20, name="The Strand", property_type=PropertyTypeEnum.JUST_VISITING, price=220, rent=18),
        Property(cell_number=21, name="Community Chest", property_type=PropertyTypeEnum.CHEST),

        Property(cell_number=22, name="Moscow", property_type=PropertyTypeEnum.LANDMARK,country=CountryTypeEnum.RUSSIA, price=220, rent=18),
        Property(cell_number=23, name="Saint Petersburg", property_type=PropertyTypeEnum.LANDMARK,country=CountryTypeEnum.RUSSIA, price=240, rent=20),
        Property(cell_number=24, name="Kazan", property_type=PropertyTypeEnum.LANDMARK,country=CountryTypeEnum.RUSSIA, price=200, rent=25),

        Property(cell_number=25, name="Paris", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.FRANCE, price=260, rent=22),
        Property(cell_number=26, name="Lyon", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.FRANCE, price=260, rent=22),
        Property(cell_number=27, name="Toulouse", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.FRANCE, price=280, rent=22),

        Property(cell_number=28, name="Go To Jail", property_type=PropertyTypeEnum.GO_TO_JAIL),

        Property(cell_number=29, name="Manchester", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.ENGLAND, price=300, rent=26),
        Property(cell_number=30, name="Liverpool", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.ENGLAND, price=300, rent=26),
        Property(cell_number=31, name="Community Chest", property_type=PropertyTypeEnum.CHEST),
        Property(cell_number=32, name="London", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.ENGLAND, price=320, rent=28),

        Property(cell_number=33, name="Liverpool St. Airport", property_type=PropertyTypeEnum.AIRPORT, price=200, rent=25),

        Property(cell_number=34, name="Community Chest", property_type=PropertyTypeEnum.CHEST),
        Property(cell_number=35, name="NewYork", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.AMERICA, price=350, rent=35),
        Property(cell_number=36, name="Super Tax", property_type=PropertyTypeEnum.SUPER_TAX),
        Property(cell_number=37, name="San Francisco", property_type=PropertyTypeEnum.LANDMARK, country=CountryTypeEnum.AMERICA, price=400, rent=50),
    ]

    @classmethod
    def return_board(cls):
        return cls.board

    @classmethod
    def number_of_cities_in_a_country(cls, given_country: CountryTypeEnum):
        count = 0
        for _property in cls.board:
            if _property.country == given_country:
                count += 1
        return count

    @classmethod
    def upgrade_cities_to_upgradable(cls, given_country: CountryTypeEnum):
        for _property in cls.board:
            if _property.country == given_country:
                _property.is_upgradable = True

    @classmethod
    def change_cities_to_not_upgradable(cls, given_country):
        for _property in cls.board:
            if _property.country == given_country:
                _property.is_upgradable = False


