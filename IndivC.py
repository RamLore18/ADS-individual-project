# Ramogi Lore Mukisa
# 188454
# Individual Project submission


from collections import defaultdict # I will use defaultdict for hash tables
import heapq # I will use for heaps
import pandas as pd # I will use pandas for data manipulation
import matplotlib.pyplot as plt # I can use to visualize emissions trends
import time # Measure time taken for operations
co2_data = pd.read_csv("co2 Emission Africa(1).csv") # Load your data here.

class EmissionRecord: # Record keeping class
    """Class to represent an emission record."""
    def __init__(self, country, year, sector, emission1, emmission2):
        self.country = country
        self.year = year
        self.sector = sector # Sectors of emissions (e.g., Energy, Industry, etc.)
        self.emission1 = emission1 # Total CO2 emmission including LUCF (Mt)
        self.emission2 = emmission2 # Total CO2 emmission excluding LUCF (Mt)

    def __repr__(self):
        return f"\n({self.country} || {self.year} || \n{self.sector} || \nTotal CO2 emmission including LUCF {self.emission1}(Mt) || \nTotal CO2 emmission excluding LUCF {self.emission2}(Mt))->"
# This class represents a single emission record with attributes for country, year, sector, and emissions.


class Node:
    def __init__(self, data: EmissionRecord):
        self.data = data
        self.next = None

class LinkedList:  # Used for undo operations and record storage (Q6 & 7)
    def __init__(self):
        self.head = None

    def insert(self, data: EmissionRecord):
        node = Node(data)
        node.next = self.head
        self.head = node

    def remove_first(self):
        if self.head:
            self.head = self.head.next

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class EmissionSystem:
    def __init__(self):
        self.country_map = defaultdict(list)  # hash table
        self.year_totals = defaultdict(float) #purely for storing total emissions per year
        self.records = LinkedList()  # linked list
        self.undo_stack = []  # list of recently added records

    # 1. Search Emissions by Country
    def search_by_country(self, country):
        return self.country_map[country]  # O(1) lookup time, Constant 

    # 2. Total Emissions Per Year
    def compute_total_per_year(self):
        return dict(self.year_totals)  # O(n) Increases with number of entries

    # 3. Top N Emitting Countries
    def top_n_emitters(self, year, N):
        country_emissions = defaultdict(float)
        for record in self.records.to_list():
            if record.year == year:
                country_emissions[record.country] += record.emission1
        heap = [(-v, k) for k, v in country_emissions.items()]
        heapq.heapify(heap)  # O(n)
        return [(k, -v) for v, k in heapq.nsmallest(N, heap)]  # O(N log n) Increases with N
        # Returns a list of tuples (country, total_emission) for the top N emitters

    # 4. Emissions by Sector
    def emissions_by_sector(self, country):
        sector_totals = co2_data[co2_data['Country'] == country].iloc[:, 12:].sum()  # Sectors start from index 12 to the end
        sector_totals = sector_totals[sector_totals > 0] # Filter out sectors with no emissions
        sector_totals = sector_totals.sort_values(ascending=False)  # Sort sectors by total emissions
        print(f"Emissions by Sector for {country}:")
        for sector, total in sector_totals.items():
            print(f"{sector}: {total} Mt") # O(n log n) for sorting
        # will require finding out which sector to use
        # complete later
        # completed
    
    # 5. Emissions Trend for a Country
    def emissions_trend(self, country):
        country_data = self.country_map[country]
        sorted_data = sorted(country_data, key=lambda r: r.year)
        # Plotting the emissions trend
        plt.plot([r.year for r in sorted_data], [r.emission1 for r in sorted_data], marker='o', linestyle='-', color='r', label=f"{country} Emissions (Mt)")
        plt.plot([r.year for r in sorted_data], [r.emission2 for r in sorted_data], marker='x', linestyle='--', color='b', label=f"{country} Emissions (Mt)")
        plt.title(f"Emissions Trend for {country}")
        plt.xlabel("Year")
        plt.ylabel("Emissions")
        plt.legend([f"{country} Emissions (Mt)"])
        plt.grid()
        plt.show()
        plt.clf() 
        return [(r.year, r.emission1, r.emission2) for r in sorted_data]
          # O(n log n)

    # 6. Insert New Emission Record
    def insert_record(self, record: EmissionRecord):
        self.records.insert(record)
        self.country_map[record.country].append(record)
        self.year_totals[record.year] += record.emission1
        self.undo_stack.append(record) # O(1) appending to a list

    # 7. Undo Last Insertion
    def undo_last_insertion(self):
        if not self.undo_stack:
            return "No insertions to undo"
        last = self.undo_stack.pop()
        # Remove from linked list
        self.records.remove_first()  # O(1)
        # Remove from hash table
        self.country_map[last.country].remove(last)  # O(n) worst case
        self.year_totals[last.year] -= last.emission1 # Keeps the total emissions per year accurate

    def display_all(self):
        print(self.records.to_list())  # O(n)

system = EmissionSystem()
grouped_data = co2_data.groupby('Country')
for index, row in co2_data.iterrows():
    record = EmissionRecord(
        country=row.iloc[0],
        year=row.iloc[3],
        sector=row.iloc[12:], 
        emission1=row.iloc[9],
        emmission2=row.iloc[10]
    )
    system.insert_record(record)
        

if __name__ == "__main__":
    Nation = str(input("Enter the name of the country you want to search: "))
    print(f"Searching for emissions data for {Nation}...")

    print(f"1)Search {Nation}:")
    start_time = time.time()
    print(system.search_by_country(Nation))
    if not system.search_by_country(Nation):
        print(f"No emissions data found for {Nation}.")
    else:
        print(f"Emissions data for {Nation} retrieved successfully.")
    end_time = time.time()
    print(f"Search Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print("\n2)Total Emissions Per Year:")
    print(system.compute_total_per_year())
    end_time = time.time()
    print(f"Total Emissions Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print("\n3)Top 2 Emitters (2020):")
    print(system.top_n_emitters(2020, 2))
    end_time = time.time()
    print(f"Top Emitters Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print("\n4)Emissions by Sector:")
    print(system.emissions_by_sector(Nation))
    end_time = time.time()
    print(f"Emissions by Sector Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print(f"\n5)Emissions Trend for {Nation}:")
    print(system.emissions_trend(Nation))
    end_time = time.time()
    print(f"Emissions Trend Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print("\n6)Insertion of new record:")
    new_record = EmissionRecord("Nigeria", 2021, "Energy", 100.0, 120.0)
    system.insert_record(new_record)
    print(system.undo_stack[-1]) # Show the last inserted record
    end_time = time.time() 
    print(f"Insertion Time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    print("\n7)Undo Last Insertion")
    system.undo_last_insertion()
    print(system.undo_stack[-1])  # Show the stack after undo
    end_time = time.time()
    print(f"Undo Time: {end_time - start_time:.6f} seconds")
    '''
    print("\n8)Display All Records:")
    system.display_all()'''


'''
    # Uncomment the following line to display all records
    # system.display_all()
    Thank you for taking the time to review my code. I hope it meets your expectations and requirements. If you have any questions or need further modifications, please let me know.
    # [my Github link]{https://github.com/RamLore18}'''