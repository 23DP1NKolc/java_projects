# Balsošanas programma par mūziķiem

Šī ir GUI (grafiskā) Python programma, kas ļauj lietotājiem autentificēties ar e-pastu un paroli, balsot par saviem iecienītākajiem mūziķiem dažādos žanros, un pēc balsošanas termiņa beigām – skatīt rezultātus.

## Funkcionalitāte
- Lietotāja autentifikācija: Katrs lietotājs var balsot tikai vienu reizi, izmantojot savu e-pastu.
- Balsošana dažādos žanros: Katram žanram jāizvēlas viens mūziķis.
- Dzīvs atpakaļskaitīšanas taimeris: Rāda, cik laika atlicis līdz balsošanas beigām.
- Automātiska rezultātu parādīšana: Pēc noteiktā datuma rezultāti tiek automātiski rādīti.
- Statistikas rādīšana: Cik cilvēku balsojuši par katru mūziķi.

## Tehnoloģijas
- Python 3
- Tkinter – lietotāja saskarnes izveidei
- Pillow (PIL) – attēlu apstrādei
- JSON – datu saglabāšanai (balsis un lietotāji)
- Hashlib – paroļu šifrēšanai (SHA-256)

## Faili
- main.py – galvenais programmas fails
- balsis.json – lietotāju balsis
- balsotaji.json – reģistrētie lietotāji (hash parole)
- rock.png, pop.png, jazz.png, hiphop.png, electro.png – žanru attēli

## Lietošanas instrukcija

1. Instalē nepieciešamās bibliotēkas:
```sh
pip install pillow
```
2. Pārliecinies, ka attēli ir tajā pašā mapē, kur main.py fails.
3. Palaid programmu:
python main.py
4. Ievadi e-pastu un paroli, lai pieslēgtos.
5. Izvēlies mūziķus katrā žanrā un saglabā balsis.
6. Pēc noteiktā datuma (01.05.2025) automātiski tiks parādīti rezultāti.

Datuma maiņa
Lai mainītu balsošanas beigu datumu, rediģē mainīgo END_DATE:
```sh
END_DATE = "2025-05-01 00:00:00"
```
# Autors
# Ņikita Koļcovs, Maksims Koršunovs 
