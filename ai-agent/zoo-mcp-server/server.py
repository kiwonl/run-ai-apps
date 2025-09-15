import asyncio
import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Zoo Animal MCP Server 🦁🐧🐻")

# Dictionary of animals at the zoo
ZOO_ANIMALS = [
    {
        "species": "lion",
        "species_kr": "사자",
        "name": "Leo",
        "age": 7,
        "enclosure": "The Big Cat Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "lion",
        "species_kr": "사자",
        "name": "Nala",
        "age": 6,
        "enclosure": "The Big Cat Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "lion",
        "species_kr": "사자",
        "name": "Simba",
        "age": 3,
        "enclosure": "The Big Cat Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "lion",
        "species_kr": "사자",
        "name": "King",
        "age": 8,
        "enclosure": "The Big Cat Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Waddles",
        "age": 2,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Pip",
        "age": 4,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Skipper",
        "age": 5,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Chilly",
        "age": 3,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Pingu",
        "age": 6,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "penguin",
        "species_kr": "펭귄",
        "name": "Noot",
        "age": 1,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "elephant",
        "species_kr": "코끼리",
        "name": "Ellie",
        "age": 15,
        "enclosure": "The Pachyderm Sanctuary",
        "trail": "Savannah Heights",
    },
    {
        "species": "elephant",
        "species_kr": "코끼리",
        "name": "Peanut",
        "age": 12,
        "enclosure": "The Pachyderm Sanctuary",
        "trail": "Savannah Heights",
    },
    {
        "species": "elephant",
        "species_kr": "코끼리",
        "name": "Dumbo",
        "age": 5,
        "enclosure": "The Pachyderm Sanctuary",
        "trail": "Savannah Heights",
    },
    {
        "species": "elephant",
        "species_kr": "코끼리",
        "name": "Trunkers",
        "age": 10,
        "enclosure": "The Pachyderm Sanctuary",
        "trail": "Savannah Heights",
    },
    {
        "species": "bear",
        "species_kr": "곰",
        "name": "Smokey",
        "age": 10,
        "enclosure": "The Grizzly Gulch",
        "trail": "Polar Path",
which
    },
    {
        "species": "bear",
        "species_kr": "곰",
        "name": "Grizzly",
        "age": 8,
        "enclosure": "The Grizzly Gulch",
        "trail": "Polar Path",
    },
    {
        "species": "bear",
        "species_kr": "곰",
        "name": "Barnaby",
        "age": 6,
        "enclosure": "The Grizzly Gulch",
        "trail": "Polar Path",
    },
    {
        "species": "bear",
        "species_kr": "곰",
        "name": "Bruin",
        "age": 12,
        "enclosure": "The Grizzly Gulch",
        "trail": "Polar Path",
    },
    {
        "species": "giraffe",
        "species_kr": "기린",
        "name": "Gerald",
        "age": 4,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "giraffe",
        "species_kr": "기린",
        "name": "Longneck",
        "age": 5,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "giraffe",
        "species_kr": "기린",
        "name": "Patches",
        "age": 3,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "giraffe",
        "species_kr": "기린",
        "name": "Stretch",
        "age": 6,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "antelope",
        "species_kr": "영양",
        "name": "Speedy",
        "age": 2,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "antelope",
        "species_kr": "영양",
        "name": "Dash",
        "age": 3,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "antelope",
        "species_kr": "영양",
        "name": "Gazelle",
        "age": 4,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "antelope",
        "species_kr": "영양",
        "name": "Swift",
        "age": 5,
        "enclosure": "The Tall Grass Plains",
        "trail": "Savannah Heights",
    },
    {
        "species": "polar bear",
        "species_kr": "북극곰",
        "name": "Snowflake",
        "age": 7,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "polar bear",
        "species_kr": "북극곰",
        "name": "Blizzard",
        "age": 5,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "polar bear",
        "species_kr": "북극곰",
        "name": "Iceberg",
        "age": 9,
        "enclosure": "The Arctic Exhibit",
        "trail": "Polar Path",
    },
    {
        "species": "walrus",
        "species_kr": "바다코끼리",
        "name": "Wally",
        "age": 10,
        "enclosure": "The Walrus Cove",
        "trail": "Polar Path",
    },
    {
        "species": "walrus",
        "species_kr": "바다코끼리",
        "name": "Tusker",
        "age": 12,
        "enclosure": "The Walrus Cove",
        "trail": "Polar Path",
    },
    {
        "species": "walrus",
        "species_kr": "바다코끼리",
        "name": "Moby",
        "age": 8,
        "enclosure": "The Walrus Cove",
        "trail": "Polar Path",
    },
    {
        "species": "walrus",
        "species_kr": "바다코끼리",
        "name": "Flippers",
        "age": 9,
        "enclosure": "The Walrus Cove",
        "trail": "Polar Path",
    },
]


@mcp.tool()
def get_animals_by_species(species: str) -> List[Dict[str, Any]]:
    """
    Retrieves all animals of a specific species from the zoo.
    Can also be used to collect the base data for aggregate queries
    of animals of a specific species - like counting the number of penguins
    or finding the oldest lion.

    Args:
        species: The species of the animal (e.g., 'lion', 'penguin', '사자', '펭귄').

    Returns:
        A list of dictionaries, where each dictionary represents an animal
        and contains details like name, age, enclosure, and trail.
    """
    logger.info(f">>> 🛠️ Tool: 'get_animals_by_species' called for '{species}'")
    return [
        animal
        for animal in ZOO_ANIMALS
        if animal["species"].lower() == species.lower()
        or animal["species_kr"].lower() == species.lower()
    ]


@mcp.tool()
def get_animal_details(name: str) -> Dict[str, Any]:
    """
    Retrieves the details of a specific animal by its name.

    Args:
        name: The name of the animal.

    Returns:
        A dictionary with the animal's details (species, species_kr, name, age, enclosure, trail)
        or an empty dictionary if the animal is not found.
    """
    logger.info(f">>> 🛠️ Tool: 'get_animal_details' called for '{name}'")
    for animal in ZOO_ANIMALS:
        if animal["name"].lower() == name.lower():
            return animal
    return {}


if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
