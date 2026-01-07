from app import app
from database import db, Pokemon

def seed():
    with app.app_context():
        # Check if data exists
        if Pokemon.query.first():
            print("Database already contains Pokemon. Skipping seed.")
            return

        print("Seeding database with 50 Pokemon...")

        pokemon_list = [
            # Grass
            {"name": "Bulbasaur", "type": "Grass", "cp": 318, "id": 1},
            {"name": "Ivysaur", "type": "Grass", "cp": 405, "id": 2},
            {"name": "Venusaur", "type": "Grass", "cp": 525, "id": 3},
            {"name": "Oddish", "type": "Grass", "cp": 290, "id": 43},
            {"name": "Gloom", "type": "Grass", "cp": 390, "id": 44},
            {"name": "Vileplume", "type": "Grass", "cp": 490, "id": 45},
            {"name": "Bellsprout", "type": "Grass", "cp": 280, "id": 69},
            {"name": "Weepinbell", "type": "Grass", "cp": 390, "id": 70},
            {"name": "Victreebel", "type": "Grass", "cp": 490, "id": 71},

            # Fire
            {"name": "Charmander", "type": "Fire", "cp": 309, "id": 4},
            {"name": "Charmeleon", "type": "Fire", "cp": 405, "id": 5},
            {"name": "Charizard", "type": "Fire", "cp": 534, "id": 6},
            {"name": "Vulpix", "type": "Fire", "cp": 299, "id": 37},
            {"name": "Ninetales", "type": "Fire", "cp": 505, "id": 38},
            {"name": "Growlithe", "type": "Fire", "cp": 350, "id": 58},
            {"name": "Arcanine", "type": "Fire", "cp": 555, "id": 59},
            {"name": "Ponyta", "type": "Fire", "cp": 410, "id": 77},
            {"name": "Rapidash", "type": "Fire", "cp": 500, "id": 78},
            {"name": "Magmar", "type": "Fire", "cp": 495, "id": 126},

            # Water
            {"name": "Squirtle", "type": "Water", "cp": 314, "id": 7},
            {"name": "Wartortle", "type": "Water", "cp": 405, "id": 8},
            {"name": "Blastoise", "type": "Water", "cp": 530, "id": 9},
            {"name": "Psyduck", "type": "Water", "cp": 320, "id": 54},
            {"name": "Golduck", "type": "Water", "cp": 500, "id": 55},
            {"name": "Poliwag", "type": "Water", "cp": 300, "id": 60},
            {"name": "Poliwhirl", "type": "Water", "cp": 385, "id": 61},
            {"name": "Poliwrath", "type": "Water", "cp": 510, "id": 62},
            {"name": "Magikarp", "type": "Water", "cp": 10, "id": 129},
            {"name": "Gyarados", "type": "Water", "cp": 540, "id": 130},
            {"name": "Lapras", "type": "Water", "cp": 535, "id": 131},

            # Electric
            {"name": "Pikachu", "type": "Electric", "cp": 320, "id": 25},
            {"name": "Raichu", "type": "Electric", "cp": 485, "id": 26},
            {"name": "Magnemite", "type": "Electric", "cp": 325, "id": 81},
            {"name": "Magneton", "type": "Electric", "cp": 465, "id": 82},
            {"name": "Voltorb", "type": "Electric", "cp": 330, "id": 100},
            {"name": "Electrode", "type": "Electric", "cp": 480, "id": 101},
            {"name": "Electabuzz", "type": "Electric", "cp": 490, "id": 125},
            {"name": "Jolteon", "type": "Electric", "cp": 525, "id": 135},

            # Normal
            {"name": "Pidgey", "type": "Normal", "cp": 251, "id": 16},
            {"name": "Pidgeotto", "type": "Normal", "cp": 349, "id": 17},
            {"name": "Pidgeot", "type": "Normal", "cp": 479, "id": 18},
            {"name": "Rattata", "type": "Normal", "cp": 253, "id": 19},
            {"name": "Raticate", "type": "Normal", "cp": 413, "id": 20},
            {"name": "Meowth", "type": "Normal", "cp": 290, "id": 52},
            {"name": "Persian", "type": "Normal", "cp": 440, "id": 53},
            {"name": "Eevee", "type": "Normal", "cp": 325, "id": 133},
            {"name": "Snorlax", "type": "Normal", "cp": 540, "id": 143},

            # Psychic / Ghost
            {"name": "Abra", "type": "Psychic", "cp": 310, "id": 63},
            {"name": "Kadabra", "type": "Psychic", "cp": 400, "id": 64},
            {"name": "Alakazam", "type": "Psychic", "cp": 500, "id": 65},
            {"name": "Gastly", "type": "Ghost", "cp": 310, "id": 92},
            {"name": "Haunter", "type": "Ghost", "cp": 405, "id": 93},
            {"name": "Gengar", "type": "Ghost", "cp": 500, "id": 94},
            {"name": "Mewtwo", "type": "Psychic", "cp": 680, "id": 150},

            # Rock / Ground / Fighting
            {"name": "Geodude", "type": "Rock", "cp": 300, "id": 74},
            {"name": "Graveler", "type": "Rock", "cp": 390, "id": 75},
            {"name": "Golem", "type": "Rock", "cp": 495, "id": 76},
            {"name": "Machop", "type": "Fighting", "cp": 305, "id": 66},
            {"name": "Machoke", "type": "Fighting", "cp": 405, "id": 67},
            {"name": "Machamp", "type": "Fighting", "cp": 505, "id": 68},
            {"name": "Onix", "type": "Rock", "cp": 385, "id": 95},
            
            # Dragon
            {"name": "Dratini", "type": "Dragon", "cp": 300, "id": 147},
            {"name": "Dragonair", "type": "Dragon", "cp": 420, "id": 148},
            {"name": "Dragonite", "type": "Dragon", "cp": 600, "id": 149},
        ]

        # Convert dicts to Pokemon objects
        pokemon_objects = []
        for p in pokemon_list:
            # Construct the official PokeAPI image URL
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p['id']}.png"
            new_poke = Pokemon(
                name=p['name'],
                type=p['type'],
                cp=p['cp'],
                image_url=img_url
            )
            pokemon_objects.append(new_poke)

        db.session.add_all(pokemon_objects)
        db.session.commit()
        print(f"Successfully seeded {len(pokemon_objects)} Pokemon!")

if __name__ == "__main__":
    seed()