from datetime import date, timedelta

# --- 1. CALCOLO CALENDARIO LITURGICO (Metodo di Gauss e Calendario Luterano) ---

def calculate_easter(year: int) -> date:
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)

def get_liturgical_dates(year: int) -> dict[date, str]:
    easter = calculate_easter(year)
    xtmas = date(year, 12, 25)
    adv4 = xtmas - timedelta(days=(xtmas.weekday() + 1) % 7 or 7)
    adv1 = adv4 - timedelta(weeks=3)
    
    dates = {
        date(year, 1, 1): "New Year's Day",
        date(year, 1, 6): "Epiphany",
        date(year, 2, 2): "Purification",
        date(year, 3, 25): "Annunciation",
        date(year, 6, 24): "St. John's Day",
        date(year, 7, 2): "Visitation",
        date(year, 8, 13): "Council Election", # Occasionale
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
    
    # Avvento
    for i, n in enumerate(['I','II','III','IV']): dates[adv1 + timedelta(weeks=i)] = f"Advent {n}"
    # Pre-Quaresima
    sep = easter - timedelta(63)
    dates[sep], dates[sep+timedelta(7)], dates[sep+14] = "Septuagesima", "Sexagesima", "Estomihi"
    # Epifania
    curr, n = date(year, 1, 6) + timedelta(days=(6 - date(year, 1, 6).weekday()) or 7), 1
    while curr < sep:
        dates[curr] = f"Epiphany {n}"
        curr, n = curr + timedelta(7), n + 1
    # Pasqua
    pnames = ["Quasimodogeniti", "Misericordias Domini", "Jubilate", "Cantate", "Rogate", "Exaudi"]
    for i, name in enumerate(pnames): dates[easter + timedelta(weeks=i+1)] = name
    # Trinity
    curr, n = (easter + timedelta(56)) + timedelta(7), 1
    while curr < adv1:
        dates[curr] = f"Trinity {n}"
        curr, n = curr + timedelta(7), n + 1
    return dates

# --- 2. DATABASE INTEGRALE DELLE CANTATE (Estratto dei 3 Cicli) ---

db = {
    'Advent I': [('61','Nun komm, der Heiden Heiland I'),('62','Nun komm... II'),('36','Schwingt freudig')],
    'Christmas Day': [('63','Christen, ätzet'),('91','Gelobet seist du'),('110','Unser Mund'),('248/I','Oratorio I')],
    'Second Day of Christmas': [('40','Dazu ist erschienen'),('121','Christum wir sollen'),('57','Selig ist der Mann'),('248/II','Oratorio II')],
    'Third Day of Christmas': [('64','Sehet, welch eine Liebe'),('133','Ich freue mich in dir'),('151','Süßer Trost'),('248/III','Oratorio III')],
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
    'Misericordias Domini': [('104','Du Hirte Israel'),('85','Ich bin ein guter Hirt')],
    'Jubilate': [('12','Weinen, Klagen'),('103','Ihr werdet weinen'),('146','Wir müssen durch viel Trübsal')],
    'Cantate': [('166','Wo gehest du hin?'),('108','Es ist euch gut')],
    'Rogate': [('86','Wahrlich, wahrlich'),('87','Bisher habt ihr nichts')],
    'Ascension': [('37','Wer da gläubet'),('128','Auf Christi Himmelfahrt'),('11','Oratorio di Ascensione')],
    'Exaudi': [('44','Sie werden euch in den Bann tun'),('183','Sie werden euch... II')],
    'Pentecost': [('172','Erschallet, ihr Lieder'),('59','Wer mich liebet'),('74','Wer mich liebet II'),('34','O ewiges Feuer')],
    'Trinity': [('165','O heilges Geist- und Wasserbad'),('194','Höchsterwünschtes Freudenfest'),('176','Es ist ein trotzig und verzagt')],
    'Trinity 1': [('75','Die Elenden sollen essen'),('20','O Ewigkeit, du Donnerwort')],
    'Trinity 2': [('76','Die Himmel erzählen'),('2','Ach Gott, vom Himmel sieh darein')],
    'Trinity 3': [('21','Ich hatte viel Bekümmernis'),('135','Ach Herr, mich armen Sünder')],
    'Trinity 4': [('185','Barmherziges Herze'),('24','Ein ungefärbt Gemüte')],
    'Trinity 5': [('93','Wer nur den lieben Gott'),('88','Siehe, ich will viel Fischer aussenden')],
    'Trinity 6': [('170','Vergnügte Ruh'),('9','Es ist das Heil uns kommen her')],
    'Trinity 7': [('186','Ärgre dich, o Seele, nicht'),('107','Was willst du dich betrüben'),('187','Es wartet alles auf dich')],
    'Trinity 8': [('136','Erforsche mich, Gott'),('178','Wo Gott der Herr nicht bei uns hält'),('45','Es ist dir gesagt')],
    'Trinity 9': [('105','Herr, gehe nicht ins Gericht'),('94','Was frag ich nach der Welt'),('168','Tue Rechnung!')],
    'Trinity 10': [('46','Schauet doch und sehet'),('101','Nimm von uns, Herr'),('102','Herr, deine Augen sehen')],
    'Trinity 11': [('199','Mein Herze schwimmt im Blut'),('179','Siehe zu, daß deine Gottesfurcht'),('113','Herr Jesu Christ, du höchstes Gut')],
    'Trinity 12': [('69a','Lobe den Herrn, meine Seele'),('137','Lobe den Herren, den mächtigen König')],
    'Trinity 13': [('77','Du sollt Gott, deinen Herren, lieben'),('33','Allein zu dir, Herr Jesu Christ')],
    'Trinity 14': [('25','Es ist nichts Gesundes'),('78','Jesu, der du meine Seele'),('17','Wer Dank opfert')],
    'Trinity 15': [('138','Warum betrübst du dich'),('99','Was Gott tut, das ist wohlgetan'),('51','Jauchzet Gott in allen Landen')],
    'Trinity 16': [('161','Komm, du süße Todesstunde'),('95','Christus, der ist mein Leben'),('8','Liebster Gott, wenn werd ich sterben')],
    'Trinity 17': [('148','Bringet dem Herrn Ehre'),('114','Ach, lieben Christen'),('47','Wer sich selbst erhöhet')],
    'Trinity 18': [('96','Herr Christ, der einge Gottessohn'),('169','Gott soll allein mein Herze haben')],
    'Trinity 19': [('48','Ich elender Mensch'),('5','Wo soll ich fliehen hin'),('56','Ich will den Kreuzstab gerne tragen')],
    'Trinity 20': [('162','Ach! ich sehe, itzt'),('180','Schmücke dich, o liebe Seele'),('49','Ich geh und suche mit Verlangen')],
    'Trinity 21': [('109','Ich glaube, lieber Herr'),('38','Aus tiefer Not schrei ich zu dir'),('98','Was Gott tut, das ist wohlgetan')],
    'Trinity 22': [('89','Was soll ich aus dir machen'),('115','Mache dich, mein Geist, bereit'),('55','Ich armer Mensch')],
    'Trinity 23': [('163','Nur jedem das Seine'),('139','Wohl dem, der sich auf seinen Gott'),('52','Falsche Welt, dir trau ich nicht')],
    'Trinity 24': [('60','O Ewigkeit, du Donnerwort II'),('26','Ach wie flüchtig, ach wie nichtig')],
    'Trinity 25': [('90','Es reißet euch ein schrecklich Ende'),('116','Du Friedefürst, Herr Jesu Christ')],
    'Trinity 26': [('70','Wachet! betet!'),('116','Du Friedefürst')],
    'Trinity 27': [('140','Wachet auf, ruft uns die Stimme')],
    'Purification': [('82','Ich habe genug'),('83','Erfreute Zeit'),('125','Mit Fried und Freud')],
    'Annunciation': [('1','Wie schön leuchtet der Morgenstern')],
    'St. John\'s Day': [('7','Christ unser Herr zum Jordan kam'),('167','Ihr Menschen, rühmet Gottes Liebe')],
    'Visitation': [('147','Herz und Mund und Tat und Leben'),('10','Meine Seel erhebt den Herren')],
    'St. Michael\'s Day': [('130','Herr Gott, dich loben alle wir'),('19','Es erhub sich ein Streit'),('149','Man singet mit Freuden')],
    'Reformation': [('80','Ein feste Burg ist unser Gott'),('79','Gott der Herr ist Sonn und Schild')]
}

# --- 3. MOTORE DI ANALISI ---

def analyze_week(target_date: date):
    lit_dates = get_liturgical_dates(target_date.year)
    monday = target_date - timedelta(days=target_date.weekday())
    
    print(f"\n{'='*60}")
    print(f"🎹 BACH COMPANION: SETTIMANA DEL {target_date.year}")
    print(f"Periodo: Lunedì {monday} — Domenica {monday + timedelta(6)}")
    print(f"{'='*60}\n")
    
    for i in range(7):
        current = monday + timedelta(days=i)
        occasion = lit_dates.get(current, "Feria")
        
        # Titolo Giorno
        print(f"🗓️ {current.strftime('%a %d %B')} -> {occasion}")
        
        # Suggerimento Oratorio
        if (current.month == 12 and current.day >= 25) or (current.month == 1 and current.day <= 6):
            print("   💡 [Suggerimento: Periodo dell'Oratorio di Natale BWV 248]")
        
        # Cantate dal DB
        cantatas = db.get(occasion, [])
        if cantatas:
            for bwv, title in cantatas:
                b_num = bwv.split('/')[0] if '/' in bwv else bwv
                it_link = f"https://www.bach-cantatas.com/Texts/BWV{b_num}-Ita.htm"
                print(f"   🎼 BWV {bwv}: {title}")
                print(f"      📖 Testo: {it_link}")
        else:
            print("   - Nessuna cantata specifica in archivio")
        print("-" * 40)

# --- 4. ESECUZIONE ---

if __name__ == "__main__":
    print("BENVENUTO NEL BACH COMPANION 2026")
    inp = input("Inserisci data (AAAA-MM-GG) o premi INVIO per OGGI: ").strip()
    
    try:
        if not inp:
            d = date.today()
        else:
            d = date.fromisoformat(inp)
        analyze_week(d)
    except ValueError:
        print("❌ Formato non valido. Usa AAAA-MM-GG.")
