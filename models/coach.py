from typing import List, Optional, Dict


class Coach:
    ALLOWED_ATTRIBUTES = ["tactics", "motivation", "discipline", "adaptability", "leadership", "training"]

    def __init__(self, name: str, attributes: Optional[Dict[str, int]] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        self.name = name
        self.attributes = {attr: 0 for attr in Coach.ALLOWED_ATTRIBUTES}

        if attributes:
            for attr, value in attributes.items():
                if attr not in Coach.ALLOWED_ATTRIBUTES:
                    raise ValueError(f"Invalid attribute '{attr}'. Must be one of {Coach.ALLOWED_ATTRIBUTES}")
                if not isinstance(value, int) or not (0 <= value <= 100):
                    raise ValueError("Attribute values must be integers between 0 and 100")
                self.attributes[attr] = value
