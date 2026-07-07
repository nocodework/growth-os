<div align="center">

<a href="README.md">English</a> · <b>Polski</b>

<br/>
<br/>

<img src="docs/assets/growth-os-hero.svg" alt="Growth OS — Growth OS dla dowolnego agenta AI" width="720" />

<h1>NoCodeWork Growth OS</h1>

<b>Otwartoźródłowy Growth OS dla dowolnego agenta AI.</b>

<br/>
<br/>

![License](https://img.shields.io/badge/license-MIT-7c3aed?style=flat-square)
![Growth OS](https://img.shields.io/badge/Growth%20OS-Growth OS-fd43be?style=flat-square)
![Runtime](https://img.shields.io/badge/runtime-agnostyczny-2a2440?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-ready-3b82f6?style=flat-square)
![Made by NoCodeWork](https://img.shields.io/badge/made%20by-NoCodeWork-1a1a2e?style=flat-square)

<br/>

<a href="#instalacja"><b>Instalacja</b></a> ·
<a href="#podłącz-konta"><b>Podłącz konta</b></a> ·
<a href="#jak-to-działa"><b>Jak to działa</b></a> ·
<a href="#prywatność-i-klucze"><b>Prywatność</b></a>

</div>

<br/>

---

## Dlaczego

Zbudowałem Growth OS, bo mam dość powtarzania agentowi tego samego. Kim jest klient, czym różnimy się od konkurencji, jaki jest ruch z GA4, po co komu ta strona. Za każdym razem od zera. Marketingowe „packi" skilli robią świetną robotę na poziomie pojedynczego zadania — napisz reklamę, zrób audyt SEO — ale nic nie trzyma **kontekstu firmy** i nic nie sięga po **żywe dane** z Twoich kont.

Growth OS wypełnia tę lukę. Dajesz mu URL swojego biznesu. On wyciąga USP, UVP i ICP, zapisuje to raz do trwałego pliku kontekstu, po czym każdy kolejny skill marketingowy czyta z tego samego źródła. Do tego dokłada warstwę odczytu na żywo — GA4, Search Console, PageSpeed, widoczność w AI — więc rekomendacje opierają się na tym, co naprawdę się dzieje, a nie na zgadywaniu.

To nie jest kolejny pack copy. To **warstwa systemowa pod packami** — kontekst plus dane plus orkiestracja. Działa obok istniejących paczek skilli marketingowych, nie zastępuje ich i niczego z nich nie kopiuje.

<br/>

## Co robi

```
URL biznesu
   │
   ├─▶ wyciąga USP / UVP / ICP
   │
   ├─▶ zapisuje do trwałego kontekstu  →  .agents/product-marketing.md
   │
   ├─▶ audyt wzrostu
   │     SEO · page speed · GEO (widoczność w AI) · konkurenci
   │     baseline NA ŻYWO z GA4 + Search Console
   │
   ├─▶ deleguje do atomowych skilli marketingowych
   │
   └─▶ prowadzi Cię przez podłączenie kont i API
```

Konkretnie:

- **Onboarding z jednego URL-a.** Growth OS czyta Twoją stronę i proponuje pierwszą wersję pozycjonowania — USP, UVP, ICP, ton głosu, główne bóle klienta. Ty poprawiasz, on zapisuje.
- **Trwały kontekst.** Wszystko ląduje w `.agents/product-marketing.md`. Jeden plik, wersjonowany w Twoim repo, czytany przez każdy kolejny skill. Piszesz raz, korzystasz wszędzie.
- **Audyt wzrostu.** SEO on-page i techniczne, Core Web Vitals z PageSpeed Insights, GEO (czy ChatGPT / Gemini / Claude / Perplexity w ogóle Cię znają), szybki przegląd konkurencji i baseline na żywo z GA4 oraz GSC.
- **Moduł GEO.** Osobna warstwa: sprawdza jak modele AI opisują Twoją markę, gdzie jest luka i jakie treści ją domykają.
- **Delegacja.** Growth OS nie próbuje sam pisać każdej reklamy. Rozbija cel na atomowe zadania i przekazuje je do wyspecjalizowanych skilli — a kontekst i dane niesie ze sobą.
- **Kreatory podłączania kont.** Najtrudniejsza część analityki to autoryzacja. Growth OS prowadzi Cię krok po kroku: co kliknąć, jaki zakres uprawnień, gdzie wkleić klucz.

<br/>

## Z czym się łączy

Wersja v1 jest **tylko po stronie odczytu** — Growth OS czyta Twoje dane, niczego nie zmienia na kontach. Integracje dzielą się na dwie grupy według tego, jak szybko ruszysz.

🟢 **Zero zatwierdzania** — zaczynasz od zaraz, dosłownie w kilka minut.
🔴 **Wymaga zatwierdzenia z czasem oczekiwania** — jednorazowo, po stronie właściciela konta.

| Integracja | API | Dostęp | Co dostajesz |
|---|---|---|---|
| **Google Analytics 4** | Data API | 🟢 service account (JSON) lub OAuth `analytics.readonly` | Sesje, użytkownicy, konwersje, źródła, ścieżki |
| **Google Search Console** | Search Console API | 🟢 `webmasters.readonly` (to samo konto usługowe co GA4) | Zapytania, kliknięcia, pozycje, pokrycie indeksu |
| **MailerLite** | MailerLite API | 🟢 klucz Bearer z panelu | Subskrybenci, kampanie, open/click rate |
| **PageSpeed Insights** | PSI API | 🟢 klucz API z Google Cloud | Core Web Vitals, wyniki wydajności mobile/desktop |
| **Google Ads** | Google Ads API | 🔴 developer token + konto MCC (na start tryb Test/Explorer) | Kampanie, wydatki, koszt konwersji, wyszukiwane frazy |
| **Meta (Facebook + Instagram)** | Marketing / Graph API | 🔴 Weryfikacja Biznesu (~14+ dni), potem App Review na `ads_read` / `instagram_*` | Kampanie reklamowe, zasięgi, statystyki profili IG |

> **Zacznij od zielonych.** GA4, GSC, MailerLite i PageSpeed dają Ci komplet baseline'u wzrostu bez jednego formularza do zatwierdzenia. Czerwone (Google Ads, Meta) mają czas oczekiwania po stronie platformy — złóż wnioski wcześnie, korzystaj później. Growth OS działa w pełni już na samych zielonych.

Szczegóły autoryzacji dla każdej integracji:
[GA4](docs/integrations/ga4.md) ·
[Search Console](docs/integrations/google-search-console.md) ·
[MailerLite](docs/integrations/mailerlite.md) ·
[PageSpeed](docs/integrations/pagespeed.md) ·
[Google Ads](docs/integrations/google-ads.md) ·
[Meta](docs/integrations/meta-instagram.md)

<br/>

## Instalacja

Growth OS instalujesz jako plugin przez marketplace:

```
/plugin marketplace add nocodework/growth-os
/plugin install growth-os
```

To dokłada slash-command `/growth-os:` oraz CLI `growth-os`. Nic więcej nie jest wymagane, żeby ruszyć z onboardingiem — klucze API podpinasz dopiero przy podłączaniu konkretnych kont.

<br/>

## Podłącz konta

Nie musisz podpinać wszystkiego naraz. Growth OS działa od pierwszej minuty na samym URL-u, a dane dokładasz stopniowo.

```
/growth-os:connect
```

Kreator prowadzi Cię przez każdą integrację: mówi jaki dokładnie zakres uprawnień włączyć, gdzie znaleźć klucz i do której zmiennej środowiskowej go wkleić. Wszystkie klucze trafiają do lokalnego `.env` — nigdzie ich nie wysyłamy (patrz [Prywatność i klucze](#prywatność-i-klucze)).

Sugerowana kolejność:

1. **GA4 + Search Console** — jedno konto usługowe Google obsługuje oba. To fundament baseline'u.
2. **PageSpeed** — klucz API z Google Cloud, dwie minuty.
3. **MailerLite** — klucz z panelu, jeśli robisz mailing.
4. **Google Ads / Meta** — jeśli wydajesz na reklamy, złóż wnioski o dostęp wcześnie (mają czas oczekiwania).

Pełne instrukcje krok po kroku znajdziesz w [docs/integrations/](docs/integrations/).

<br/>

## Jak używać

Wszystko dzieje się przez `/growth-os:` w agencie albo przez `growth-os <adapter> <cmd>` w terminalu.

```
/growth-os:onboard   https://twojafirma.pl
      # czyta stronę, proponuje USP/UVP/ICP, zapisuje kontekst

/growth-os:context
      # pokazuje i edytuje .agents/product-marketing.md

/growth-os:audit
      # pełny audyt wzrostu: SEO, page speed, GEO, konkurenci, baseline GA4/GSC

/growth-os:connect
      # kreator podłączania kont i kluczy API

/growth-os:delegate  "przygotuj plan treści na Q3 pod nasze ICP"
      # rozbija cel na zadania i przekazuje atomowym skillom marketingowym

/growth-os:dashboard
      # zwięzły przegląd baseline'u na żywo z podłączonych kont
```

A z poziomu CLI, kiedy chcesz surowe dane pod skrypt albo pipeline:

```bash
growth-os ga4 summary --days 28
growth-os gsc queries --limit 50
growth-os pagespeed run https://twojafirma.pl
growth-os geo probe "najlepsze narzędzie do X"
```

<br/>

## Działa na dowolnym agencie

Growth OS jest **runtime-agnostyczny**. Warstwa danych to zwykłe CLI w Pythonie, a kontekst to plik markdown — żadne z nich nie jest przywiązane do konkretnego agenta.

- **Claude Code** — natywnie, przez plugin i slash-command `/growth-os:`.
- **Codex** — te same skille i to samo CLI; wołasz komendy `growth-os` bezpośrednio.
- **Hermes** i inne autonomiczne agenty — czytają `.agents/product-marketing.md` i odpalają adaptery jak każde inne narzędzie.
- **Dowolny agent przez MCP** — adaptery odczytu wystawiasz jako zasoby/narzędzia MCP, więc każdy klient zgodny z protokołem korzysta z tych samych danych.

Jedno źródło kontekstu, jedna warstwa danych, dowolny mózg na wierzchu.

<br/>

## Jak to działa

Growth OS to sześć warstw, od orkiestracji na górze po surowe dane na dole.

```
┌─────────────────────────────────────────────────────────┐
│ 1 · Orkiestrator                                         │
│     /growth-os:onboard  audit  connect  context             │
│               delegate  dashboard                        │
├─────────────────────────────────────────────────────────┤
│ 2 · Kompozycja skilli atomowych                          │
│     onboard · context · audit · geo-audit                │
│     geo-content · connect · delegate · dashboard         │
├─────────────────────────────────────────────────────────┤
│ 3 · Adaptery odczytu (Python CLI)                        │
│     GA4 · GSC · Google Ads · Meta · MailerLite · PSI     │
├─────────────────────────────────────────────────────────┤
│ 4 · Moduł GEO                                            │
│     widoczność marki w ChatGPT / Gemini / Claude / Perplexity │
├─────────────────────────────────────────────────────────┤
│ 5 · Kreatory onboardingu kont                            │
│     przeprowadzają przez OAuth, zakresy, klucze API      │
├─────────────────────────────────────────────────────────┤
│ 6 · Hub kontekstu                                        │
│     .agents/product-marketing.md  (trwałe źródło prawdy) │
└─────────────────────────────────────────────────────────┘
```

Przepływ jest prosty: orkiestrator przyjmuje intencję, wybiera odpowiednie skille (warstwa 2), które sięgają po żywe dane przez adaptery (warstwa 3) i moduł GEO (warstwa 4), a wszystko czyta i zapisuje kontekst z huba (warstwa 6). Kreatory (warstwa 5) uruchamiają się tylko wtedy, gdy brakuje jakiegoś połączenia.

Skille żyją w `core/skills/`: `onboard`, `context`, `audit`, `geo-audit`, `geo-content`, `connect`, `delegate`, `dashboard`. Każdy jest mały i robi jedną rzecz — łatwiej je podmieniać i komponować.

<br/>

## Prywatność i klucze

Prosto: **Twoje dane należą do Ciebie i nigdzie nie wychodzą.**

- **Własne klucze.** Podpinasz własne konta i własne klucze API. Growth OS nie ma pośredniczącej chmury, przez którą przechodzą Twoje dane.
- **Klucze w `.env`.** Wszystkie sekrety trzymasz lokalnie w `.env`, który jest w `.gitignore`. Nic nie jest hardkodowane, nic nie trafia do repo.
- **Self-host domyślnie.** Adaptery to skrypty, które odpalasz u siebie. Dane z GA4, GSC czy Meta lecą prosto z API Google/Meta do Twojej maszyny.
- **Zero telemetrii.** Growth OS nie dzwoni do domu. Nie zbieramy statystyk użycia, nie logujemy Twoich zapytań, nie ma „phone home". Możesz to sprawdzić w kodzie — jest otwarty.

Jeśli czegoś nie podłączysz, ta część po prostu nie działa. Żadnych ukrytych żądań w tle.

<br/>

## Jak wypada na tle innych

Uczciwie — Growth OS nie jest dla każdego i nie udaje, że jest.

| | **Growth OS** | Supermetrics | Profound | Agencja |
|---|---|---|---|---|
| Cena | darmowy, open-source | abonament od ~$39/mies. | enterprise | od kilku tys. zł/mies. |
| Trwały kontekst firmy | ✅ `.agents/*.md` | ❌ | ❌ | ✅ (w głowie ludzi) |
| Dane na żywo GA4/GSC | ✅ | ✅ | częściowo | ✅ |
| Widoczność w AI (GEO) | ✅ | ❌ | ✅ (to ich specjalność) | zależy |
| Delegacja do skilli AI | ✅ | ❌ | ❌ | ludzie zamiast skilli |
| Działa w Twoim agencie | ✅ dowolny runtime | ❌ | ❌ | ❌ |
| Gotowe dashboardy BI | ❌ | ✅ (to ich mocna strona) | ✅ | ✅ |
| Wsparcie na telefon | ❌ tylko społeczność | ✅ | ✅ | ✅ |
| Zapis / zmiany na kontach | ❌ v1 tylko odczyt | ✅ | — | ✅ |

**Gdzie Growth OS przegrywa, powiem wprost:** nie zbuduje Ci ładnego dashboardu BI jak Supermetrics — to nie ta liga i nie ten cel. GEO robi węziej niż Profound, który ma na tym zbudowany cały produkt. I nie zadzwoni do Ciebie o 23:00 jak dobra agencja. Za to jest darmowy, trzyma kontekst Twojej firmy i mieszka w Twoim agencie — a tego reszta nie robi.

<br/>

## Część ekosystemu narzędzi NoCodeWork

Growth OS jest jednym z otwartych narzędzi budowanych w [NoCodeWork](https://nocodework.io). Reszta:

- **[ai-context-kit](https://github.com/nocodework/ai-context-kit)** — startowy zestaw plików kontekstu dla agentów AI.
- **[offline-notes](https://github.com/nocodework/offline-notes)** — edytor notatek Markdown, zero żądań sieciowych.
- **[offline-sketch](https://github.com/nocodework/offline-sketch)** — szkicownik z obsługą nacisku rysika, w pełni offline.
- **[offline-whiteboard](https://github.com/nocodework/offline-whiteboard)** — tablica do burzy mózgów, zero telemetrii.

Wspólny mianownik: własne dane, własne klucze, otwarty kod.

<br/>

## Współtworzenie

Growth OS jest młody i chętnie przyjmę pomoc. Szczególnie przydają się:

- **Nowe adaptery odczytu** — LinkedIn Ads, TikTok, Bing Webmaster, Plausible, co tylko czytasz na co dzień.
- **Sondy GEO** — nowe modele i lepsze metody sprawdzania widoczności marki w AI.
- **Skille** — atomowe, jedno zadanie na skill, w duchu warstwy 2.
- **Docsy integracji** — im prościej ktoś podepnie konto, tym lepiej.

Zajrzyj do `CONTRIBUTING.md`, otwórz issue albo od razu PR. Trzymam się prostej zasady: małe, czytelne, bez zależności których nie da się wytłumaczyć.

<br/>

## Licencja

MIT © [NoCodeWork](https://nocodework.io). Rób z tym co chcesz — używaj komercyjnie, forkuj, przerabiaj. Miło, jak zostawisz link zwrotny, ale nie musisz.

<br/>

<div align="center">
<sub>Zbudowane przez <a href="https://nocodework.io">NoCodeWork</a> · <a href="README.md">English version</a></sub>
</div>
