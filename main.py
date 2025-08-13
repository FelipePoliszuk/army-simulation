"""Army simulation system.

This module implements a battle system between different civilizations,
each with unique unit characteristics and military strategies.
"""

# Unit class
class Unit:
    """Base class for all military units."""
    def __init__(self, unit_type: str, strength: int, training_cost: int, training_gain: int):
        self.unit_type = unit_type              # Unit type ("pikeman", "archer", "knight")
        self.strength = strength                # Strength points
        self.years_of_life = 0                  # Years of life
        self.training_cost = training_cost      # Gold needed for training
        self.training_gain = training_gain      # Strength points gained per training
        
    def get_years_of_life(self) -> int:
        return self.years_of_life
    
    def train(self):
        self.strength += self.training_gain
        
    def set_years_of_life(self, years_of_life: int):
        self.years_of_life = years_of_life
        
class Pikeman(Unit):
    """Pikeman unit"""
    def __init__(self):
        super().__init__(unit_type="pikeman", strength=5, training_cost=10, training_gain=3)

class Archer(Unit):
    """Archer unit"""
    def __init__(self):
        super().__init__(unit_type="archer", strength=10, training_cost=20, training_gain=7)

class Knight(Unit):
    """Knight unit"""
    def __init__(self):
        super().__init__(unit_type="knight", strength=20, training_cost=30, training_gain=10)

# Army class
class Army:
    """Represents a civilization's army"""
    def __init__(self, civilization: str):
        self.civilization = civilization
        self.gold = 1000
        self.units = []
        self.battle_record = []
        
        # Initialize units according to civilization
        civilization_lower = civilization.lower()
        if civilization_lower == "chinese":
            # 2 pikemen, 25 archers, 2 knights
            self.units.extend([Pikeman() for _ in range(2)])
            self.units.extend([Archer() for _ in range(25)])
            self.units.extend([Knight() for _ in range(2)])
        elif civilization_lower == "english":
            # 10 pikemen, 10 archers, 10 knights
            self.units.extend([Pikeman() for _ in range(10)])
            self.units.extend([Archer() for _ in range(10)])
            self.units.extend([Knight() for _ in range(10)])
        elif civilization_lower == "byzantine":
            # 5 pikemen, 8 archers, 15 knights
            self.units.extend([Pikeman() for _ in range(5)])
            self.units.extend([Archer() for _ in range(8)])
            self.units.extend([Knight() for _ in range(15)])
        else:
            raise ValueError(f"Unknown civilization: {civilization}. Valid options: chinese, english, byzantine")


    def get_total_strength(self) -> int:
        """Calculates the army's total strength."""
        return sum(unit.strength for unit in self.units)

    def train_unit(self, unit_index: int) -> bool:
        """Trains a specific unit if there's enough gold.
        
        Args:
            unit_index: Index of the unit to train
            
        Returns:
            True if training was successful, False otherwise
        """
        if unit_index < 0 or unit_index >= len(self.units):
            return False
            
        unit = self.units[unit_index]
        if self.gold >= unit.training_cost:
            self.gold -= unit.training_cost
            unit.train()
            return True
        else:
            return False

    def transform_unit(self, unit_index: int, new_type: str) -> bool:
        """Transforms the unit to another type if allowed and there's enough gold.
        
        Args:
            unit_index: Index of the unit to transform
            new_type: Target type ("archer" or "knight")
            
        Returns:
            True if transformation was successful, False otherwise
        """
        if unit_index < 0 or unit_index >= len(self.units):
            return False
        
        current_unit = self.units[unit_index]
        cost = 0
        new_unit = None
        new_type_lower = new_type.lower()
        
        # Transformation rules according to specification
        if isinstance(current_unit, Pikeman) and new_type_lower == "archer":
            cost = 30
            new_unit = Archer()
            # Preserve years of life and accumulated training points
            new_unit.years_of_life = current_unit.years_of_life
            training_bonus = current_unit.strength - 5  # 5 is the pikeman's base strength
            new_unit.strength = 10 + training_bonus  # 10 is the archer's base strength
        elif isinstance(current_unit, Archer) and new_type_lower == "knight":
            cost = 40
            new_unit = Knight()
            # Preserve years of life and accumulated training points
            new_unit.years_of_life = current_unit.years_of_life
            training_bonus = current_unit.strength - 10  # 10 is the archer's base strength
            new_unit.strength = 20 + training_bonus  # 20 is the knight's base strength
        else:
            return False  # Transformation not allowed
        
        if self.gold >= cost:
            self.gold -= cost
            self.units[unit_index] = new_unit
            return True
        else:
            return False

    def remove_strongest_units(self, count: int):
        """Removes the strongest units according to battle result."""
        if not self.units:
            return
        
        # Remove the strongest units (maximum available)
        units_to_remove = min(count, len(self.units))
        for _ in range(units_to_remove):
            strongest_unit = max(self.units, key=lambda unit: unit.strength)
            self.units.remove(strongest_unit)

    def attack(self, other_army: "Army") -> str:
        """Simulates a battle against another army and updates gold/units/history."""
        # Verify that both armies have units
        if not self.units:
            return "no_units"
        if not other_army.units:
            return "no_target"
            
        our_strength = self.get_total_strength()
        enemy_strength = other_army.get_total_strength()
        
        battle_record = {
            'opponent': other_army.civilization,
            'our_strength': our_strength,
            'enemy_strength': enemy_strength
        }
        
        if our_strength > enemy_strength:
            # Victory
            self.gold += 100
            other_army.remove_strongest_units(2)
            battle_record['result'] = 'victory'
        elif enemy_strength > our_strength:
            # Defeat
            other_army.gold += 100
            self.remove_strongest_units(2)
            battle_record['result'] = 'defeat'
        else:
            # Draw
            self.remove_strongest_units(1)
            other_army.remove_strongest_units(1)
            battle_record['result'] = 'draw'
        
        # Increment years of life for all surviving units
        self._age_all_units()
        other_army._age_all_units()
        
        # Add battle to history
        self.battle_record.append(battle_record)
        other_army.battle_record.append({
            'opponent': self.civilization,
            'our_strength': enemy_strength,
            'enemy_strength': our_strength,
            'result': 'defeat' if battle_record['result'] == 'victory' else ('victory' if battle_record['result'] == 'defeat' else 'draw')
        })
        
        return battle_record['result']
    
    def get_battle_record(self):
        """Returns the battle history"""
        if not self.battle_record:
            return f"Army of {self.civilization}\nNo battles recorded"
        
        history_lines = [f"Army of {self.civilization}"]
        for battle in self.battle_record:
            opponent = battle['opponent']
            result = battle['result']
            our_str = battle['our_strength']
            enemy_str = battle['enemy_strength']
            
            battle_line = f"Vs {opponent}: {result} ({our_str} vs {enemy_str})"
            history_lines.append(battle_line)
        
        return "\n".join(history_lines)
    
    def _age_all_units(self):
        """Increments the age of all army units by 1 year."""
        for unit in self.units:
            unit.years_of_life += 1


# Test cases
if __name__ == "__main__":
    # Create armies
    chinese_army = Army("chinese")
    english_army = Army("english")
    byzantine_army = Army("byzantine")

    # Show initial state
    print("Chinese army strength:", chinese_army.get_total_strength())
    print("English army strength:", english_army.get_total_strength())
    print("Byzantine army strength:", byzantine_army.get_total_strength())
    
    # Simulate chinese army training
    for i in range(len(chinese_army.units)):
        chinese_army.train_unit(i)
    
    # Show state
    print("Chinese army strength:", chinese_army.get_total_strength())
    
    # Simulate chinese army vs english army battle
    chinese_army.attack(english_army)
    print(chinese_army.get_battle_record())
    print("--------------------------------")
    print(english_army.get_battle_record())

    # Simulate chinese army vs byzantine army battle
    chinese_army.attack(byzantine_army)
    print(chinese_army.get_battle_record())
    print("--------------------------------")
    print(byzantine_army.get_battle_record())
    
    # Get years of life for each unit
    # for unit in chinese_army.units:
    #     print(f"Chinese army unit {unit.unit_type} years of life: {unit.get_years_of_life()}")
    # for unit in english_army.units:
    #     print(f"English army unit {unit.unit_type} years of life: {unit.get_years_of_life()}")
    # for unit in byzantine_army.units:
    #     print(f"Byzantine army unit {unit.unit_type} years of life: {unit.get_years_of_life()}")
    
    # Transform units
    chinese_army.transform_unit(0, "archer")
    chinese_army.transform_unit(1, "archer")
    chinese_army.transform_unit(0, "knight")
    chinese_army.transform_unit(1, "knight") 
    
    # Show state
    print("Chinese army strength:", chinese_army.get_total_strength())