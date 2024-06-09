from dataclasses import dataclass, field, fields, is_dataclass, _MISSING_TYPE, Field

from typing import NewType, TypeVar, Optional, get_origin, get_args, overload, Literal, Union

from jsondataclass import dataclass_to_dict, dict_to_dataclass
import json

from enum import Enum, StrEnum

@dataclass
class Person:
    name: str | int
    age: int
    address: str | None = None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Person):
            return False
        return self.name == value.name and self.age == value.age and self.address == value.address

@dataclass
class Product:
    name: str
    price: float

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Product):
            return False
        return self.name == value.name and self.price == value.price
class CompanySize(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
@dataclass
class Company:
    name: str
    employees: list[Person]
    products: dict[Union[str, int], Product]
    company_type: Literal["public", "private"]
    company_size: CompanySize
    is_open: bool = field(metadata={"serializer": lambda x: "Yes" if x else "No", "deserializer": lambda x: True if x == "Yes" else False, "rename": "open"})
    phone_numbers: set[str]
    departments: list[tuple[str, int]]

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Company):
            return False
        return self.name == value.name and self.employees == value.employees and self.products == value.products and self.is_open == value.is_open and self.phone_numbers == value.phone_numbers and self.departments == value.departments




def test():
    person1 = Person(name="John", age=30, address="123 Main St")
    person2 = Person(name="Jane", age=25, address="456 Elm St")
    company = Company(name="Acme", employees=[person1, person2], products={"software": Product(name="Acme Software", price=99.99), "hardware": Product(name="Acme Hardware", price=199.99)}, company_type="public", company_size=CompanySize.SMALL, is_open=True, phone_numbers={"123-456-7890", "234-567-8901"}, departments=[("Sales", 10), ("Engineering", 20)])

    print(dataclass_to_dict(company))
    new_company = dict_to_dataclass(Company, json.loads(json.dumps(dataclass_to_dict(company))))
    print(new_company)

    print(company == new_company)

    x = dataclass_to_dict(company)

    # x["name"] = None
    # x["employees"][1]["name"] = None
    # x["products"]["software"] = None

    x["is_open"] = "No"
    x["company_type"] = "unknown"

    x["products"] = {123: Product(name="Acme Software", price=99.99), "Hardware": Product(name="Acme Hardware", price=199.99)}

    print(dict_to_dataclass(Company, x, ret_missing=True))

if __name__ == "__main__":
    test()