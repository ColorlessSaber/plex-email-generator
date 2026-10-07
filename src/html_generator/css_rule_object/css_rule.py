from dataclasses import dataclass


@dataclass
class CSSDeclaration:
    """
    Holds a CSS declaration

    Attributes:
        _property: The property of the CSS declaration
        _value: The value of the CSS declaration
    """
    _property: str
    _value: str | int | float # allowing other possibilities for input

    def __str__(self) -> str:
        return f"{self._property}: {self._value};"


class CSSRule:
    """
    Holds the CSS rule for an HTML tag

    Attributes:
        selector: The selector of the CSS rule
        properties: The properties of the CSS rule
    """
    __slots__ = ("properties", "selector")

    def __init__(self, selector: str, properties: dict[str, str | int | float]):
        self.selector = selector

        # Turn each entry in the properties dict into CSSDeclaration objects
        declaration = []
        for key, value in properties.items():
            declaration.append(CSSDeclaration(key, value))
        self.properties = tuple(declaration)

    def __iter__(self):
        yield f"{self.selector} {{"

        for prop in self.properties:
            yield str(prop)

        yield "}"

    def __str__(self) -> str:
        declaration_str = "\n ".join(str(decl) for decl in self.properties)
        return f"{self.selector} {{\n {declaration_str}\n}}"
