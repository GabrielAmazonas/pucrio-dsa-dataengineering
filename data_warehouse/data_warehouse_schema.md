# Star Schema for Olympic Medal Data
# Fact Table:
- The fact table represents the central business events or transactions. In this case, we can choose the “Medal” column as our fact.
    MedalID (unique identifier for each medal) -- last ID to be created based on dataframes index
    AthleteID (foreign key referencing the “ID” column from the original data frame)
    EventID (foreign key referencing the “Event” column)
    DateID (foreign key referencing the "Date" column)
    MedalType (gold, silver, or bronze)

Dimension Tables:
Dimension tables describe the context of the facts. We’ll create dimension tables for the following entities:

Athlete Dimension:
Columns: AthleteID, Name, Sex, Age, Height, Weight, Team, NOC

Event Dimension:
Columns: EventID, Sport, Event
-- Create EventID column and join it on the other data frames

Date Dimension (commonly used in star schemas):
Columns: DateID, Year, Season, City
-- Create the DateID column and join it on the other data frames



## Fact Table: Medals
- `MedalID` (unique identifier for each medal)
- `AthleteID` (foreign key referencing Athlete Dimension)
- `EventID` (foreign key referencing Event Dimension)
- `Year` (foreign key referencing Date Dimension)
- `MedalType` (gold, silver, or bronze)

## Dimension Tables:
1. **Athlete Dimension**
   - `AthleteID` (unique identifier for each athlete)
   - `Name` (athlete's name)
   - `Sex` (athlete's gender)
   - `Age` (athlete's age)
   - `Height` (athlete's height)
   - `Weight` (athlete's weight)
   - `Team` (national team)
   - `NOC` (National Olympic Committee)

2. **Event Dimension**
   - `EventID` (unique identifier for each event)
   - `Sport` (type of sport)
   - `Event` (specific event within the sport)

3. **Date Dimension**
   - `DateID` (unique identifier for each date)
   - `Year` (Olympic year)
   - `Season` (summer or winter)
   - `City` (host city)

Note: The "Medal" column in the fact table corresponds to the MedalType (gold, silver, or bronze).
