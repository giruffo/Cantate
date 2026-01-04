import requests
from datetime import date, timedelta

# --- 1. MOTORE LOGICO: CALCOLO DATE LITURGICHE ---
def calculate_easter(year: int) -> date:
    """Calcola la data della Pasqua tramite l'algoritmo di Meeus/Jones/Butcher."""
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)

def get_liturgical_dates(year: int) -> dict[date, str]:
    """Genera il calendario liturgico completo per l'anno specificato."""
    easter = calculate_easter(year)
    xtmas = date(year, 12, 25)
    adv4 = xtmas - timedelta(days=(xtmas.weekday() + 1) % 7 or 7)
    adv1 = adv4 - timedelta(weeks=3)
    
    # Feste Fisse e Pasquali
    dates = {
        date(year, 1, 1): "New Year's Day", date(year, 1, 6): "Epiphany",
        date(year, 2, 2): "Purification", date(year, 3, 25): "Annunciation",
        date(year, 6, 24): "St. John's Day", date(year, 7, 2): "Visitation",
        date(year, 9, 29): "St. Michael's Day", date(year, 10, 31): "Reformation",
        date(year, 12, 25): "Christmas Day", date(year, 12, 26): "Second Day of Christmas",
        date(year, 12, 27): "Third Day of Christmas", easter: "Easter Sunday",
        easter - timedelta(days=7): "Palm Sunday", easter - timedelta(days=2): "Good Friday",
        easter + timedelta(days=1): "Easter Monday", easter + timedelta(days=2): "Easter Tuesday",
        easter + timedelta(days=39): "Ascension", easter + timedelta(days=49): "Pentecost",
        easter + timedelta(days=50): "Pentecost Monday", easter + timedelta(days=51): "Pentecost Tuesday",
        easter + timedelta(days=56): "Trinity"
    }
    
    # Domenica dopo Capodanno
    sun_ny = date(year, 1, 1) + timedelta(days=(6-date(year,1,1).weekday()) or 7)
    if sun_ny < date(year, 1, 6): dates[sun_ny] = "Sunday after New Year"

    # Avvento
    for i, n in enumerate(['I','II','III','IV']): 
        dates[adv1 + timedelta(weeks=i)] = f"Advent {n}"
    
    # Settuagesima, Sessagesima, Estomihi
    sep = easter - timedelta(days=63)
    dates[sep], dates[sep + timedelta(days=7)], dates[sep + timedelta(days=14)] = "Septuagesima", "Sexagesima", "Estomihi"
    
    # Epifania
    curr, n = date(year, 1, 6) + timedelta(days=(6 - date(year, 1, 6).weekday()) or 7), 1
    while curr < sep:
        dates[curr] = f"Epiphany {n}"
        curr += timedelta(days=7)
        n += 1
    
    # Domeniche dopo Pasqua
    pnames = ["Quasimodogeniti", "Misericordias Domini", "Jubilate", "Cantate", "Rogate", "Exaudi"]
    for i, name in enumerate(pnames): dates[easter + timedelta(weeks=i+1)] = name
    
    # Domeniche dopo Trinità
    curr, n = (easter + timedelta(days=56)) + timedelta(days=7), 1
    while curr < adv1:
        dates[curr] = f"Trinity {n}"
        curr += timedelta(days=7)
        n += 1
    return dates

# --- 2. DATABASE INTEGRALE DELLE CANTATE ---
db = {
    'Advent I': [('61','Nun komm... I'),('62','Nun komm... II'),('36','Schwingt freudig')],
    'Christmas Day': [('63','Christen, ätzet'),('91','Gelobet seist du'),('110','Unser Mund'),('248/I','Oratorio I')],
    'Second Day of Christmas': [('40','Dazu ist erschienen'),('121','Christum wir sollen'),('57','Selig ist der Mann'),('248/II','Oratorio II')],
    'Third Day of Christmas': [('64','Sehet, welch eine Liebe'),('133','Ich freue mich'),('151','Süßer Trost'),('248/III','Oratorio III')],
    "New Year's Day": [('190','Singet dem Herrn'),('41','Jesu, nun sei gepreiset'),('16','Herr Gott, dich loben wir'),('248/IV','Oratorio IV')],
    'Sunday after New Year': [('153','Schau, lieber Gott'),('58','Ach Gott, wie manches'),('248/V','Oratorio V')],
    'Epiphany': [('65','Sie werden aus Saba'),('123','Liebster Immanuel'),('248/VI','Oratorio VI')],
    'Epiphany 1': [('154','Mein liebster Jesus'),('124','Meinen Jesum laß ich nicht'),('32','Liebster Jesu')],
    'Epiphany 2': [('155','Mein Gott, wie lang'),('3','Ach Gott, wie manches'),('13','Meine Seufzer')],
    'Epiphany 3': [('73','Herr, wie du willt'),('111','Was mein Gott will'),('72','Alles nur nach Gottes Willen'),('156','Ich steh mit einem Fuß')],
    'Septuagesima': [('144','Nimm, was dein ist'),('92','Ich hab in Gottes Herz'),('84','Ich bin vergnügt')],
    'Sexagesima': [('18','Gleichwie der Regen'),('181','Leichtgesinnte Flattergeister'),('126','Erhalt uns, Herr')],
    'Estomihi': [('22','Jesus nahm zu sich'),('23','Du wahrer Gott'),('127','Herr Jesu Christ'),('159','Sehen wir')],
    'Easter Sunday': [('4','Christ lag in Todes Banden'),('31','Der Himmel lacht')],
    'Quasimodogeniti': [('67','Halt im Gedächtnis'),('42','Am Abend aber desselbigen')],
    'Misericordias Domini': [('104','Du Hirte Israel'),('85','Ich bin un buon pastore')],
    'Jubilate': [('12','Weinen, Klagen'),('103','Ihr werdet weinen'),('146','Wir müssen attraverso molto travaglio')],
    'Cantate': [('166','Wo gehest du hin?'),('108','Es ist euch gut')],
    'Rogate': [('86','Wahrlich, wahrlich'),('87','Bisher habt ihr nichts')],
    'Ascension': [('37','Wer da gläubet'),('128','Auf Christi Himmelfahrt'),('11','Oratorio di Ascensione')],
    'Pentecost': [('172','Erschallet, ihr Lieder'),('59','Wer mich liebet'),('74','Wer mich liebet II'),('34','O ewiges Feuer')],
    'Trinity': [('165','O heilges Geist-'),('194','Höchsterwünschtes'),('176','Es ist un trotzig')],
    'Trinity 1': [('75','Die Elenden sollen essen'),('20','O Ewigkeit, du Donnerwort')],
    'Trinity 27': [('140','Wachet auf, ruft uns la voce')]
}

# --- 3. MOTORE DI ANALISI ---
def analyze_week(target_date: date):
    lit_dates = get_liturgical_dates(target_date.year)
    monday = target_date - timedelta(days=target_date.weekday())
    
    # Header per superare i blocchi dei server (User-Agent camuffato)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"\n{'='*75}")
    print(f"🎹 BACH COMPANION - Settimana del {target_date.year}")
    print(f"Periodo: {monday.strftime('%d %b')} — {(monday+timedelta(days=6)).strftime('%d %b %Y')}")
    print(f"{'='*75}\n")
    
    suffixes = [""] + [str(i) for i in range(1, 11)]
    
    for i in range(7):
        current = monday + timedelta(days=i)
        occ = lit_dates.get(current, "Feria")
        print(f"🗓️ {current.strftime('%a %d %b')} -> {occ}")
        
        for bwv, title in db.get(occ, []):
            b_num = bwv.split('/')[0] if '/' in bwv else bwv
            print(f"   🎼 BWV {bwv}: {title}")
            
            # Link All of Bach (Netherlands Bach Society)
            nbs_link = f"https://www.bachvereniging.nl/en/bwv/bwv-{b_num}/"
            print(f"      📄 Approfondimenti (All of Bach): {nbs_link}")
            
            # Controllo automatico testi IT (1-10)
            found_any = False
            for sfx in suffixes:
                it_url = f"https://www.bach-cantatas.com/Texts/BWV{b_num}-Ita{sfx}.htm"
                try:
                    check = requests.get(it_url, headers=headers, timeout=1.0, stream=True)
                    if check.status_code == 200:
                        label = sfx if sfx else "base"
                        print(f"      📖 Testo IT ({label}): {it_url}")
                        found_any = True
                except:
                    continue
            
            if not found_any:
                print("      ⚠️ Nessun testo italiano trovato su bach-cantatas.com")
            
            # Ricerca YouTube
            yt_query = f"Bach+BWV+{bwv.replace('/', '+').replace(' ', '+')}+Netherlands+Bach+Society"
            yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
            print(f"      🎧 YouTube: {yt_link}")
            
        print("-" * 55)

# --- ESECUZIONE ---
if __name__ == "__main__":
    # Analizza la settimana corrente di default
    analyze_week(date.today())
    
    # Per analizzare una data specifica, togli il # dalla riga sotto:
    # analyze_week(date(2026, 4, 5))
