class City:
    def __init__(self, x, y, country, initial_amount):
        self.x = x
        self.y = y
        self.country = country
        self.coins = {country: initial_amount}
        self.new_coins = {country: 0}

    def add_coins(self, country, amount):
        if country not in self.coins:
            self.coins[country] = 0
            self.new_coins[country] = 0
        self.new_coins[country] += amount

    def transfer_coins(self):
        for country, amount in self.new_coins.items():
            self.coins[country] += amount
        self.new_coins = {country: 0 for country in self.coins}

    def distribute_coins(self, neighbors):
        for country, amount in self.coins.items():
            distribute_amount = amount // 1000
            if distribute_amount > 0:
                self.coins[country] -= distribute_amount * len(neighbors)
                for neighbor in neighbors:
                    neighbor.add_coins(country, distribute_amount)

    def all_coins_distributed(self, total_countries):
        return all(self.coins.get(country, 0) > 0 for country in total_countries)

def simulate(countries):
    all_countries = set(country['name'] for country in countries)
    cities = {}
    
    # Initialize cities
    for country in countries:
        name = country['name']
        for x in range(country['xl'], country['xh'] + 1):
            for y in range(country['yl'], country['yh'] + 1):
                cities[(x, y)] = City(x, y, name, 1000000)
    
    # Simulation loop
    day = 0
    completed_countries = set()
    while len(completed_countries) < len(countries):
        day += 1
        # Distribute coins
        for city in cities.values():
            neighbors = [
                cities.get((city.x - 1, city.y)),
                cities.get((city.x + 1, city.y)),
                cities.get((city.x, city.y - 1)),
                cities.get((city.x, city.y + 1))
            ]
            neighbors = [neighbor for neighbor in neighbors if neighbor]
            city.distribute_coins(neighbors)
        
        # Transfer coins
        for city in cities.values():
            city.transfer_coins()
        
        # Check completed countries
        for country in countries:
            if country['name'] not in completed_countries:
                if all(cities[(x, y)].all_coins_distributed(all_countries)
                       for x in range(country['xl'], country['xh'] + 1)
                       for y in range(country['yl'], country['yh'] + 1)):
                    country['days'] = day
                    completed_countries.add(country['name'])

    return sorted(countries, key=lambda c: (c['days'], c['name']))

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    case_number = 1
    idx = 0
    while idx < len(data):
        c = int(data[idx])
        if c == 0:
            break
        idx += 1
        countries = []
        for _ in range(c):
            name, xl, yl, xh, yh = data[idx].split()
            countries.append({
                'name': name,
                'xl': int(xl),
                'yl': int(yl),
                'xh': int(xh),
                'yh': int(yh)
            })
            idx += 1
        
        result = simulate(countries)
        print(f"Case Number {case_number}")
        for country in result:
            print(f"{country['name']} {country['days']}")
        case_number += 1

if __name__ == "__main__":
    main()

