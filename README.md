# Army Simulation System

This is a simple battle simulation system between different civilizations, each with unique military unit characteristics.

## What does the program do?

The program uses an object-oriented design to simulate armies from different civilizations.

## Unit Types

There are 3 types of military units:

| Unit        | Base Strength | Training Cost | Training Gain |
| ----------- | ------------- | ------------- | ------------- |
| **Pikeman** | 5 points      | 10 gold       | +3 points     |
| **Archer**  | 10 points     | 20 gold       | +7 points     |
| **Knight**  | 20 points     | 30 gold       | +10 points    |

## Available Civilizations

Each civilization starts with a different army composition:

### 🏮 Chinese

- **2** Pikemen
- **25** Archers
- **2** Knights
- **Initial gold:** 1000

### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 English

- **10** Pikemen
- **10** Archers
- **10** Knights
- **Initial gold:** 1000

### 🟣 Byzantine

- **5** Pikemen
- **8** Archers
- **15** Knights
- **Initial gold:** 1000

## Available Actions

### 🏋️ Training

- Improves the strength of a specific unit
- Consumes gold according to unit type
- Each unit gains strength points when trained

### 🔄 Transformation

Only certain transformations are allowed:

- **Pikeman → Archer:** Costs 30 gold
- **Archer → Knight:** Costs 40 gold
- The transformed unit preserves its years of life and previous training

### ⚔️ Battle

When two armies fight:

- The **total strength** of both armies is compared
- **Victory:** +100 gold, enemy loses their 2 strongest units
- **Defeat:** Enemy gains +100 gold, you lose your 2 strongest units
- **Draw:** Both armies lose their strongest unit
- All surviving units age by 1 year

## System Features

- **Resource management:** Each action consumes gold
- **Battle history:** Each encounter is recorded
- **Aging:** Units accumulate years of life
- **Strategy:** You can train and transform units
