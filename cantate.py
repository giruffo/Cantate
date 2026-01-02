from datetime import date, timedelta

# --- 1. MOTORE LOGICO: CALCOLO DATE LITURGICHE ---
def calculate_easter(year: int) -> date:
    """Calcola la data della Pasqua usando l'algoritmo di Butcher-Meeus."""
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)

def get_liturgical_dates(year: int) -> dict[date, str]:
    """Mappa le date solari alle occasioni del calendario liturgico luterano."""
    easter = calculate_easter(year)
    xtmas = date(year, 12, 25)
    
    # Calcolo dell'Avvento (4 domeniche prima del Natale)
    adv4 = xtmas - timedelta(days=(xtmas.weekday() + 1) % 7 or 7)
    adv1 = adv4 - timedelta(weeks=3)
    
    dates = {
        date(year, 1, 1): "New Year's Day",
        date(year, 1, 6): "Epiphany",
        date(year, 2, 2): "Purification",
        date(year, 3, 25): "Annunciation",
        date(year, 6, 24): "St. John's Day",
        date(year, 7, 2): "Visitation",
        date(year, 9, 29): "St. Michael's Day",
        date(year, 10, 31): "Reformation",
        date(year, 12, 25): "Christmas Day",
        date(year, 12, 26): "Second Day of Christmas",
        date(year, 12, 27): "Third Day of Christmas",
        easter: "Easter Sunday",
        easter - timedelta(days=7): "Palm Sunday",
        easter - timedelta(days=2): "Good Friday",
        easter + timedelta(days=1): "Easter Monday",
        easter + timedelta(days=2): "Easter Tuesday",
        easter + timedelta(days=39): "Ascension",
        easter + timedelta(days=49): "Pentecost",
        easter + timedelta(days=50): "Pentecost Monday",
        easter + timedelta(days=51): "Pentecost Tuesday",
        easter + timedelta(days=56): "Trinity"
    }
    
    # Domenica dopo Capodanno (importante per l'inizio di gennaio)
    sun_ny = date(year, 1, 1) + timedelta(days=(6-date(year,1,1).weekday()) or 7)
    if sun_ny < date(year, 1, 6):
        dates[sun_ny] = "Sunday after New Year"

    # Ciclo dell'Avvento
    for i, n in enumerate(['I','II','III','IV']): 
        dates[adv1 + timedelta(weeks=i)] = f"Advent {n}"
    
    # Periodo di Settuagesima
    sep = easter - timedelta(days=63)
    dates[sep] = "Septuagesima"
    dates[sep + timedelta(days=7)] = "Sexagesima"
    dates[sep + timedelta(days=14)] = "Estomihi"
    
    # Domeniche post-Epifania
    curr, n = date(year, 1, 6) + timedelta(days=(6 - date(year, 1, 6).weekday()) or 7), 1
    while curr < sep:
        dates[curr] = f"Epiphany {n}"
        curr += timedelta(days=7)
        n += 1
    
    # Domeniche post-Pasqua
    pnames = ["Quasimodogeniti", "Misericordias Domini", "Jubilate", "Cantate", "Rogate", "Exaudi"]
    for i, name in enumerate(pnames): 
        dates[easter + timedelta(weeks=i+1)] = name
    
    # Domeniche dopo Trinità
    curr, n = (easter + timedelta(days=56)) + timedelta(days=7), 1
    while curr < adv1:
        dates[curr] = f"Trinity {n}"
        curr += timedelta(days=7)
        n += 1
        
    return dates

# --- 2. DATABASE INTEGRALE (Esempio dei tre cicli principali) ---
db = {
    'Advent I': [('61','Nun komm... I'),('62','Nun komm... II'),('36','Schwingt freudig')],
    'Christmas Day': [('63','Christen, ätzet'),('91','Gelobet seist du'),('110','Unser Mund'),('248/I','Oratorio I')],
    'Second Day of Christmas': [('40','Dazu ist erschienen'),('121','Christum wir sollen'),('57','Selig ist der Mann'),('248/II','Oratorio II')],
    'Third Day of Christmas': [('64','Sehet, welch eine Liebe'),('133','Ich freue mich'),('151','Süßer Trost'),('248/III','Oratorio III')],
    "New Year's Day": [('190','Singet dem Herrn'),('41','Jesu, nun sei gepreiset'),('16','Herr Gott, dich loben wir'),('248/IV','Oratorio IV')],
    'Sunday after New Year': [('153','Schau, lieber Gott'),('58','Ach Gott, wie manches'),('248/V','Oratorio V')],
    'Epiphany': [('65','Sie werden aus Saba'),('123','Liebster Immanuel'),('248/VI','Oratorio VI')],
    'Epiphany 1': [('154','Mein liebster Jesus'),('124','Meinen Jesum laß ich nicht'),('32','Liebster Jesu')],
    'Epiphany 3': [('73','Herr, wie du willt'),('111','Was mein Gott will'),('72','Alles solo nach Gottes'),('156','Ich steh mit einem Fuß')],
    'Sexagesima': [('18','Gleichwie der Regen'),('181','Leichtgesinnte Flattergeister'),('126','Erhalt uns, Herr')],
    'Easter Sunday': [('4','Christ lag in Todes Banden'),('31','Der Himmel lacht')],
    'Trinity 27': [('140','Wachet auf, ruft uns die Stimme')]
    # Nota: Puoi aggiungere tutte le altre 200+ cantate seguendo lo stesso formato
}

# --- 3. MOTORE DI ANALISI E OUTPUT ---
def analyze_week(target_date: date):
    lit_dates = get_liturgical_dates(target_date.year)
    monday = target_date - timedelta(days=target_date.weekday())
    total_cantatas = sum(len(v) for v in db.values())
    
    print(f"\n{'='*70}")
    print(f"🎹 BACH COMPANION - Database: {total_cantatas} Cantate Caricate")
    print(f"Analisi settimana: {monday.strftime('%d %b %Y')} — {(monday+timedelta(days=6)).strftime('%d %b %Y')}")
    print(f"{'='*70}\n")
    
    for i in range(7):
        current = monday + timedelta(days=i)
        occ = lit_dates.get(current, "Feria")
        print(f"🗓️ {current.strftime('%a %d %b')} -> {occ}")
        
        # Suggerimento Oratorio Natale
        if (current.month == 12 and current.day >= 25) or (current.month == 1 and current.day <= 6):
            print("   💡 [Periodo suggerito: Oratorio di Natale BWV 248]")
            
        for bwv, title in db.get(occ, []):
            b_num = bwv.split('/')[0] if '/' in bwv else bwv
            it_link = f"https://www.bach-cantatas.com/Texts/BWV{b_num}-Ita.htm"
            print(f"   🎼 BWV {bwv}: {title}")
            print(f"      📖 Testo IT: {it_link}")
        print("-" * 50)

if __name__ == "__main__":
    # Oggi è il 2 Gennaio 2026
    # Se vuoi permettere l'input manuale, de-commenta le righe sotto.
    # d_str = input("Inserisci data (AAAA-MM-GG) o premi INVIO per oggi: ").strip()
    # d = date.fromisoformat(d_str) if d_str else date.today()
    
    analyze_week(date.today())
