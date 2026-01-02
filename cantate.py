from datetime import date, timedelta

# --- MOTORE LOGICO: CALCOLO DATE LITURGICHE ---

def calculate_easter(year: int) -> date:
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)

def get_liturgical_dates(year: int) -> dict[date, str]:
    easter = calculate_easter(year)
    xtmas = date(year, 12, 25)
    
    # Calcolo Avvento (4 domeniche prima del 25/12)
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
        easter - timedelta(7): "Palm Sunday",
        easter - timedelta(2): "Good Friday",
        easter: "Easter Sunday",
        easter + timedelta(1): "Easter Monday",
        easter + timedelta(2): "Easter Tuesday",
        easter + timedelta(39): "Ascension",
        easter + timedelta(49): "Pentecost",
        easter + timedelta(50): "Pentecost Monday",
        easter + timedelta(51): "Pentecost Tuesday",
        easter + timedelta(56): "Trinity",
    }
    
    # Cicli Dinamici
    for i, n in enumerate(['I','II','III','IV']): 
        dates[adv1 + timedelta(weeks=i)] = f"Advent {n}"
    
    septuagesima = easter - timedelta(63)
    dates[septuagesima] = "Septuagesima"
    dates[septuagesima + timedelta(days=7)] = "Sexagesima"
    dates[septuagesima + timedelta(days=14)] = "Estomihi"
    
    # Domeniche post-Epifania (Correzione TypeError)
    epiphany_date = date(year, 1, 6)
    curr = epiphany_date + timedelta(days=(6 - epiphany_date.weekday()) or 7)
    n = 1
    while curr < septuagesima:
        dates[curr] = f"Epiphany {n}"
        curr += timedelta(days=7)
        n += 1
        
    # Domeniche post-Pasqua e Trinity
    pnames = ["Quasimodogeniti", "Misericordias Domini", "Jubilate", "Cantate", "Rogate", "Exaudi"]
    for i, name in enumerate(pnames): 
        dates[easter + timedelta(weeks=i+1)] = name

    curr = (easter + timedelta(56)) + timedelta(days=7)
    n = 1
    while curr < adv1:
        dates[curr] = f"Trinity {n}"
        curr += timedelta(days=7)
        n += 1

    # Domeniche fisse legate al Natale
    sun_xtmas = xtmas + timedelta(days=(6-xtmas.weekday()) or 7)
    if sun_xtmas not in dates: 
        dates[sun_xtmas] = "Sunday after Christmas"
        
    sun_ny = date(year, 1, 1) + timedelta(days=(6-date(year,1,1).weekday()) or 7)
    if sun_ny not in dates and sun_ny < date(year, 1, 6): 
        dates[sun_ny] = "Sunday after New Year"

    return dates

# --- DATABASE: LE CANTATE ---

cantatas_by_occasion = {
    'Advent I': [{'bwv': 'BWV 61', 'title': 'Nun komm, der Heiden Heiland', 'year': '1714', 'notes': 'Weimar'}],
    'Christmas Day': [{'bwv': 'BWV 248/I', 'title': 'Jauchzet, frohlocket!', 'year': '1734', 'notes': 'Oratorio I'}],
    'Second Day of Christmas': [{'bwv': 'BWV 248/II', 'title': 'Und es waren Hirten', 'year': '1734', 'notes': 'Oratorio II'}],
    "New Year's Day": [{'bwv': 'BWV 248/IV', 'title': 'Fallt mit Danken', 'year': '1735', 'notes': 'Oratorio IV'}],
    'Sunday after New Year': [{'bwv': 'BWV 248/V', 'title': 'Ehre sei dir, Gott', 'year': '1735', 'notes': 'Oratorio V'}],
    'Epiphany': [{'bwv': 'BWV 248/VI', 'title': 'Herr, wenn die stolzen Feinde', 'year': '1735', 'notes': 'Oratorio VI'}],
    'Epiphany 3': [{'bwv': 'BWV 111', 'title': "Was mein Gott will, das g'scheh allzeit", 'year': '1725', 'notes': 'Corale'}],
    'Estomihi': [{'bwv': 'BWV 127', 'title': "Herr Jesu Christ, wahr' Mensch und Gott", 'year': '1725', 'notes': 'Corale'}],
    'Trinity 27': [{'bwv': 'BWV 140', 'title': 'Wachet auf, ruft uns die Stimme', 'year': '1731', 'notes': 'Corale'}]
}

# --- MOTORE DI ANALISI E OUTPUT ---

def get_week_analysis(date_str: str) -> str:
    target = date.fromisoformat(date_str)
    lit_dates = get_liturgical_dates(target.year)
    monday = target - timedelta(days=target.weekday())
    week = [monday + timedelta(days=i) for i in range(7)]
    
    output = f"## 🎹 Bach Companion: Settimana del {target.year}\n"
    
    for d in week:
        occ = lit_dates.get(d, "Feria")
        output += f"\n### 🗓️ {d.strftime('%A %d %B')} — *{occ}*\n"
        
        # Contestualizzazione Oratorio di Natale
        if date(target.year, 12, 25) <= d <= date(target.year, 1, 6):
            output += "💡 *Contesto: Si suggerisce l'ascolto dell'Oratorio di Natale (BWV 248).*\n"
            
        cantatas = cantatas_by_occasion.get(occ, [])
        if cantatas:
            for c in cantatas:
                bwv_id = c['bwv'].replace('BWV ', '').replace('/I', '-1').replace('/V', '-5').replace('/VI', '-6')
                yt_link = f"https://music.youtube.com/search?q=Bach+{c['bwv'].replace(' ','+')}"
                it_link = f"https://www.bach-cantatas.com/Texts/BWV{bwv_id.split('-')[0]}-Ita.htm"
                en_link = f"https://www.bach-cantatas.com/Texts/BWV{bwv_id.split('-')[0]}-Eng.htm"
                
                output += f"  - **{c['bwv']}: {c['title']}** ({c['year']})\n"
                output += f"    🔗 [Ascolta su YT Music]({yt_link}) | 📖 Testi: [DE/IT]({it_link}) - [DE/EN]({en_link})\n"
        else:
            output += "  - (Nessuna cantata specifica in archivio)\n"
    
    return output

print(get_week_analysis("2026-01-02"))
