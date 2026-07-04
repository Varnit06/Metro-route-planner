class Station:
    def __init__(self, line, name, next_station, travel_time_to_next, is_interchange):
        self.line = line
        self.name = name
        self.next_station = next_station
        self.travel_time_to_next = travel_time_to_next
        self.is_interchange = is_interchange


class MetroLine:

    def __init__(self, name): # Why not stations as argument : At that moment, you don't have any stations yet. You're going to read them from the file one by one.
        self.name = name
        self.stations = []

    def add_stations(self, station):
        self.stations.append(station)

    def display_stations(self):
        for stn in self.stations:
            print(stn.name)


    
class MetroSystem:

    def __init__(self):
        self.metro_lines = {}

    def load_data(self, filename):
        # self.filename = filename
        with open(filename,"r") as file:
            next(file) #Reads first line (header) and then discards it
            for line in file:
                line = line.strip()
                data = [value.strip() for value in line.split(",")]
                if data[4]=="No":
                    data[4]=False
                else:
                    data[4]=True
                station = Station(data[0], data[1], data[2], int(data[3]), data[4])
                line_name = data[0]
                if line_name not in self.metro_lines:
                    self.metro_lines[line_name]=MetroLine(line_name)
                self.metro_lines[line_name].add_stations(station)

    def build_graph(self):
        self.graph = {}
        for metro_lines in self.metro_lines.keys():
            for stns in self.metro_lines[metro_lines].stations:
                if(stns.next_station != "Nil"):
                    if stns.name not in self.graph:
                        self.graph[stns.name] = []

                    if stns.next_station not in self.graph:
                        self.graph[stns.next_station] = []

                    self.graph[stns.name].append((stns.next_station,stns.travel_time_to_next))
                    self.graph[stns.next_station].append((stns.name, stns.travel_time_to_next))
        
        return self.graph

# Return back and write complete function again
    def shortest_path(self, source):
        import heapq as pq
        distance= {}
        parent = {}
        heap = []
        for station in self.graph:
            distance[station] = float('inf')
            parent[station] = None      
        distance[source] = 0  
        pq.heappush(heap,(0, source))
        while heap:
            current_distance, current_station = pq.heappop(heap)
            if current_distance > distance[current_station]:
                continue
            
            for neigh_stations in self.graph[current_station]:
                if distance[neigh_stations[0]] > distance[current_station] + neigh_stations[1]:
                    distance[neigh_stations[0]] = distance[current_station] + neigh_stations[1]
                    parent[neigh_stations[0]] = current_station
                    pq.heappush(heap, (distance[neigh_stations[0]], neigh_stations[0]))
        
        return distance,parent
                    
    def reconstruct_path(self, parent, destination):
        path = []
        # self.source = source
        # self.destination = destination
        # distance, parent = self.shortest_path(source)
        path.append(destination)
        predecessor = parent[destination]
        while predecessor != None:
            path.append(predecessor)
            predecessor = parent[predecessor]
        for i in range(0, len(path)//2):
            temp = path[i]
            path[i] = path[len(path)-1-i]
            path[len(path)-1-i] = temp
        return path
    
    def find_route(self, source, destination, time_string):
        if not is_service_running(time_string):
            return{
                "success": False,
                "message": "Services currently unavailable, next train at 06:00"
            }
        if source==destination:
            return{
                "success": False,
                "message": "Invalid source or destination"
            }
        if source not in self.graph or destination not in self.graph:
            return {
                "success": False,
                "message": "Invalid source or destination"
            }
        distance, parent = self.shortest_path(source)
        shortest_route  = self.reconstruct_path(parent, destination)
        get_frequency(time_string)
        next_train = next_departure(time_string)
        if next_train != "No services currently available. Next train at 06:00.":
            next_train_minutes = time_to_minutes(next_train)
            train_arrival_minutes = next_train_minutes + distance[destination]
            return {
                "success":True,
                "next_train": next_train,
                "route": shortest_route,
                "travel_time": distance[destination],
                "arrival_time": minutes_to_time(train_arrival_minutes),
                "station_count": len(shortest_route)    
            }
    

def time_to_minutes(time_str):
    if ":" not in time_str:
        raise ValueError("Invalid input !")
    time_str = time_str.strip()
    hh_mm = [value.strip() for value in time_str.split(":")]
    if len(hh_mm) == 2:
        if hh_mm[0].isdigit() and hh_mm[1].isdigit():
            if len(hh_mm[1]) != 2:
                raise ValueError("Time formatting is invalid !")
            if int(hh_mm[0]) not in range (0,24):
                raise ValueError("hh must lie between 0 and 23") 
            if int(hh_mm[1]) not in range (0,60):
                raise ValueError("mm must lie between 0 and 59")
        else:
            raise ValueError("Time must contain only digits")
        return int(hh_mm[0])*60 + int(hh_mm[1])
    else:
        raise ValueError("Invalid Input !")
    
    
        
# Come back here
def minutes_to_time(minutes):
    
    if minutes in range(0,1440):
        hh = minutes // 60
        mm = minutes % 60
        distance = (f"{hh:02d}:{mm:02d}")
        return distance
    else:
        raise ValueError("minutes out of range")
    
def is_peak_hour(time_string):
    time_minutes = time_to_minutes(time_string)
    if time_minutes in range(480, 600) or time_minutes in range(1020, 1140):
        return True
    else:
        return False
    
def is_service_running(time_string):
    time_minutes = time_to_minutes(time_string)
    if time_minutes not in range (360, 1380):
        return False
    return True
    
def get_frequency(time_string):
    if is_peak_hour(time_string):
        return 4
    return 8

def next_departure(time_string):
    time_minutes = time_to_minutes(time_string)
    # if not is_service_running(time_string):
    #     if(time_minutes>=1380 or time_minutes<480):
    #         return "No services currently available. Next train at 06:00."
    frequency = get_frequency(time_string)
    arrival_time = []
    distance = 360
    while(distance<480):
        arrival_time.append(distance)
        distance+=8
    while(distance<600):
        arrival_time.append(distance)
        distance+=4
    while(distance<1020):
        arrival_time.append(distance)
        distance+=8
    while(distance<1260):
        arrival_time.append(distance)
        distance+=4
    while(distance<=1380):
        arrival_time.append(distance)
        distance+=8
    for i in arrival_time:
        if(0<i-time_minutes<frequency):
            return minutes_to_time(i)
    else:
        return time_string
    





if __name__ == "__main__":
    m1 = MetroSystem()
    m1.load_data("Data.txt")
    metro_graph = m1.build_graph()

    source = input("Enter source station: ").strip()
    destination = input("Enter destination station: ").strip()
    time_string = input("Enter current time: ").strip()

    m1.find_route(source, destination, time_string)

    



    

    
    






        



