import requests
import re
import json
import html

class recupMonthData:
    def __init__(self, group, url, start, end):
        self.group = group
        self.url = url
        self.start = start
        self.end = end
        self.data = self.loadData()
        self.setHeaders()
        self.setPayload()
        
    def __str__(self):
        if not self.data:
            return "\033[91mAucune donnée disponible. Veuillez récupérer les données d'abord.\033[0m"
        output = []
        border = "═" * 50
        for group, events in self.data.items():
            if group == "Subjects":
                continue
            output.append(f"\033[96m╔{border}╗\033[0m")
            output.append(f"\033[1;94m║ Groupe : {group:<40} ║\033[0m")
            output.append(f"\033[96m╠{border}╣\033[0m")
            allList = []
            for date, details in events.items():
                if date == "Subjects":
                    continue
                dateList = []
                strDate = f"\033[92m║  📅 {date:<43}║\033[0m"
                dateList.append(strDate)
                for idx, event in details.items():
                    name = event.get("name", "N/A")
                    start_time = event.get("start_time", "N/A")
                    end_time = event.get("end_time", "N/A")
                    sites = ', '.join(event.get("sites", []))
                    rooms = ', '.join(event.get("rooms", []))
                    category = event.get("eventCategory", "N/A")
                    strLessons = f"\033[93m║    • {start_time} - {end_time} | {name} | {category} | {sites} in {rooms}\033[0m"
                    dateList.append(strLessons)
                allList.append(dateList)
                
            # Tri des événements par date
            allList.sort(key=lambda x: x[0])  # Trie par la première ligne qui contient la date
            for dateList in allList:
                output.extend(dateList)
            output.append(f"\033[96m╚{border}╝\033[0m\n")
            
        # Affichage des matières
        subjects = self.data.get(self.group, {}).get("Subjects", [])
        if subjects:
            output.append(f"\033[1;95mMatières du groupe {self.group} :\033[0m")
            output.append(f"\033[95m  - " + "\n  - ".join(subjects) + "\033[0m")
        return "\n".join(output)
        
    def setHeaders(self):
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://celcat.u-bordeaux.fr",
            "Referer": f"https://celcat.u-bordeaux.fr/calendar/cal?vt=month&dt={self.start}&et=group&fid0={self.group}"
        }
        
    def setPayload(self):
        self.payload = {
            "start": self.start,
            "end": self.end,
            "resType": "103",
            "calView": "month",
            "federationIds": self.group,
            "coulorSheme": "3"
        }
        
    def saveData(self):
        with open('./assets/json/data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        
    def loadData(self):
        try:
            with open('./assets/json/data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
    def recupData(self):
        try:
            response = requests.post(self.url, data=self.payload, headers=self.headers)
            
            self.data[self.group] = {} if self.group not in self.data else self.data[self.group]
            self.data[self.group]["Subjects"] = [] if "Subjects" not in self.data[self.group] else self.data[self.group]["Subjects"]
            
            if response.status_code == 200:
                rep = response.json()
                for i, event in enumerate(rep):
                    start = event.get("start", "N/A")
                    end = event.get("end", "N/A")
                    name = event.get("modules", "N/A")
                    sites = event.get("sites")
                    enventCategory = event.get("eventCategory", "N/A")
                    description = event.get("description", "N/A")
                    description = html.unescape(description)
                    
                    # check if the format YYYY-MM-DD is in start if yes put the text in date
                    match = re.match(r"\d{4}-\d{2}-\d{2}", start)
                    if match:
                        date = match.group(0)
                        
                    start_time = start[11:16] if start else "N/A"
                    end_time = end[11:16] if end else "N/A"    
                    
                    if sites is None:
                        sites = ["N/A"]
                    else: 
                        sites = list(set(sites))
                    if isinstance(name, list):
                        name = name[0] if name else "N/A"
                        if name not in self.data[self.group]["Subjects"]:
                            self.data[self.group]["Subjects"].append(name)
                    
                    # Extract room from description
                    
                    description = description.replace('\r\n', '\n').replace('<br />', '\n')
                    infos = [line.strip() for line in description.split('\n') if line.strip() and not re.match(r'^<.*>$', line.strip())]
                    formats = [r"CREMI\s-\sBât\.\sA28\sSalle\s\d+", r"[A-Z]\d{2}\s?\/\s?(Amphithéâtre|Salle)"]
                    infos_filtred = [info for info in infos if any(re.search(format, info) for format in formats)]
                    rooms = []
                    for room in infos_filtred:
                        if '/' in room:
                            rooms.append(room.split('/')[1].strip())
                        elif 'CREMI' in room:
                            rooms.append(room.split('A28')[1].strip())
                    
                    
                    if date not in self.data[self.group]:
                        self.data[self.group][date] = {}
                    
                    size = len(self.data[self.group][date])
                    self.data[self.group][date][size] = {
                        "start_time": start_time,
                        "end_time": end_time,
                        "name": name,
                        "sites": sites,
                        "rooms": rooms,
                        "enventCategory": enventCategory
                    }
                
                if self.data[self.group]["Subjects"] == []:
                    # Remove group from data
                    del self.data[self.group]
                    return False
                
                self.saveData()
                return True
                
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            
if __name__ == "__main__":
    group = "INF401A41"
    url = "https://celcat.u-bordeaux.fr/calendar/Home/GetCalendarData"
    

    for m in range(1, 7):
        month = f"{m:02d}"
        start = f"2026-{month}-01"
        end = f"2026-{(m+1):02d}-01"
        obj = recupMonthData(group, url, start, end)
        obj.recupData()