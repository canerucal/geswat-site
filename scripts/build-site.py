#!/usr/bin/env python3
"""Generates index.html (single-page site) plus thin redirect pages.
Privacy and terms sections are maintained in data/legal.json.
Run: python3 scripts/build-site.py
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT
LANGS = ['tr', 'en', 'es']
EMAIL = 'hello@brocan.co'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'


def legal(lang, key):
    import json
    return json.loads((ROOT / 'data' / 'legal.json').read_text(encoding='utf8'))[lang][key]


T = {
    'tr': dict(
        title='geswat · Bilmesen de olur, tahmin et', desc='geswat: iki takım, bir soru, en yakın tahmin kazanır. Çevrimdışı iPhone parti oyunu.',
        nav_home='Oyun', nav_how='Nasıl oynanır', nav_support='Destek', nav_privacy='Gizlilik', store='App Store',
        h1a='Bilmesen de olur.', h1b='Tahmin et.',
        lead='İki takım, tek telefon, bir soru. Cevap bir sayı; doğruya en yakın tahmin puanı alır. İnternet gerekmez.',
        cta='App Store’da yakında', cta2='Nasıl oynanır?',
        f=[('Tek telefon, iki takım', 'Telefonu elden ele verin. Her takım yalnızca kendi tahminini görür; cevap açılınca ikisi de ortaya çıkar.'),
           ('Sayı doğrusunda cevap', 'Doğru cevap ve iki tahmin aynı çizgide. Kim daha yakın, neden kazandı: bir bakışta.'),
           ('Her dilde kendi soruları', 'Doğa, bilim, tarih, coğrafya, spor, kültür, teknoloji, insan vücudu. Türkçe, İngilizce ve İspanyolca’da yerel sorular.')],
        how='Nasıl oynanır?',
        steps=[('Takımları kur', 'İsimleri yazın, soru sayısını seçin: 5, 10 ya da 20.'),
               ('Tahmin edin', 'Soru bir sayı ister. İki takım da sırayla tahminini girer.'),
               ('En yakın kazanır', 'Doğru cevaba en yakın takım 1 puan alır. Eşit uzaklıkta ikisi de alır.')],
        support='Destek', support_lead='Takıldığın bir şey mi var? Önce sık sorulanlara bak; bulamazsan bize yaz, en kısa sürede dönelim.',
        contact='Bize ulaş', contact_p='Destek, öneri ve hata bildirimleri için bize yaz. Butonlar kendi e‑posta uygulamanı açar.',
        mail_btn='Destek e‑postası yaz', bug_btn='Hata bildir', mail_subject='geswat destek', bug_subject='geswat hata bildirimi',
        bug_body='Ne oldu?\n\n\nNasıl tekrar edebiliriz?\n1.\n2.\n3.\n\n---\niPhone modeli: \niOS sürümü: \ngeswat sürümü: \nDil: ',
        bug_note='Hata bildirirken iPhone modelini, iOS sürümünü ve geswat sürümünü eklersen daha hızlı çözeriz.',
        faq_h='Sık sorulanlar',
        faq=[('Oyun nasıl oynanır?', 'İki takım aynı telefonda oynar. Her soru sayısal bir cevap ister; iki takım da sırayla tahminini girer, sonra “Cevabı Göster”e dokunulur. Doğru cevaba en yakın takım 1 puan alır; eşit uzaklıkta ikisi de alır. Oyun sonunda puanı yüksek olan kazanır.'),
             ('İnternet gerekiyor mu?', 'Hayır. Sorular uygulamanın içindedir; oyun tamamen çevrimdışı çalışır.'),
             ('Dili nasıl değiştiririm?', 'Ayarlar → Dil. “Otomatik” cihaz dilini kullanır (Türkçe, İngilizce veya İspanyolca; diğer dillerde İngilizce). Dil değişince yeni oyunlar o dilin soru havuzundan gelir; her dilin kendi yerel soruları vardır.'),
             ('Yarım kalan oyunu nasıl sürdürürüm?', 'Ana ekranda “Oyuna Devam Et” kartına dokun. Yeni oyun başlatmak önceki oyunun yerine geçer.'),
             ('Ondalıklı veya negatif sayı girebilir miyim?', 'Evet. Tuş takımındaki virgül (İngilizcede nokta) ondalık, ± tuşu işaret içindir.'),
             ('Bir cevap yanlış görünüyor.', 'Bazı cevaplar yaklaşık değerlerdir ve kaynağa göre değişebilir. Yine de hatalı olduğunu düşündüğün soruyu “Hata bildir” ile gönder; soru metnini yazman yeterli.'),
             ('Verilerim nerede?', 'Hepsi cihazında: takım adları, tercihler, devam eden oyun. Sunucuya hiçbir şey gönderilmez. Ayrıntı için aşağıdaki Gizlilik bölümüne bak.')],
        privacy='Gizlilik Politikası', privacy_lead='geswat hesap istemez, veri toplamaz ve sunucuya hiçbir şey göndermez. Aşağıda cihazında ne tutulduğu anlatılıyor.',
        terms='Kullanım Koşulları', terms_lead='geswat eğlence amaçlı bir tahmin oyunudur. Uygulamayı kullanarak aşağıdaki koşulları kabul etmiş olursun.',
        eula_h='Lisans sözleşmesi', eula_p=f'Uygulama App Store üzerinden dağıtılır ve Apple’ın standart Son Kullanıcı Lisans Sözleşmesi’ne (EULA) tabidir: <a href="{EULA}">apple.com/legal/…/stdeula</a>.',
        contact_h='İletişim', contact_short=f'Sorular için: <a href="mailto:{EMAIL}">{EMAIL}</a>.',
        eyebrow_how='OYUN', eyebrow_support='YARDIM', eyebrow_privacy='VERİ', eyebrow_terms='KURALLAR', updated='Son güncelleme: 20 Ekim 2026', lang_label='Dil', foot_support='Destek', foot_privacy='Gizlilik', foot_terms='Koşullar',
    ),
    'en': dict(
        title='geswat · No clue. Just guess.', desc='geswat is an offline two-team number-guessing party game for iPhone.',
        nav_home='Game', nav_how='How to play', nav_support='Support', nav_privacy='Privacy', store='App Store',
        h1a='No clue.', h1b='Just guess.',
        lead='Two teams, one phone, one question. Every answer is a number; the closest guess scores. No internet needed.',
        cta='Coming soon on the App Store', cta2='How to play',
        f=[('One phone, two teams', 'Pass the phone around. Each team only sees its own guess until the answer is revealed.'),
           ('Answers on a number line', 'The correct answer and both guesses on one line. Who was closer, and why, at a glance.'),
           ('Local questions in every language', 'Nature, science, history, geography, sports, culture, technology, the human body. Native questions in English, Turkish and Spanish.')],
        how='How to play',
        steps=[('Set up the teams', 'Type your names and pick 5, 10 or 20 questions.'),
               ('Make your guesses', 'Every question asks for a number. Both teams enter a guess in turn.'),
               ('Closest wins', 'The team closest to the answer scores 1 point. Equal distance? Both score.')],
        support='Support', support_lead="Stuck on something? Check the FAQ first; if that doesn't help, write to us and we'll get back to you.",
        contact='Contact us', contact_p='Write to us for support, suggestions and bug reports. The buttons open your own mail app.',
        mail_btn='Email support', bug_btn='Report a bug', mail_subject='geswat support', bug_subject='geswat bug report',
        bug_body='What happened?\n\n\nHow can we reproduce it?\n1.\n2.\n3.\n\n---\niPhone model: \niOS version: \ngeswat version: \nLanguage: ',
        bug_note='Please include your iPhone model, iOS version and geswat version so we can fix it faster.',
        faq_h='FAQ',
        faq=[('How do I play?', 'Two teams share one phone. Every question asks for a number; both teams enter a guess in turn, then tap “Reveal Answer”. The team closest to the correct answer scores 1 point; at equal distance both score. Most points at the end wins.'),
             ('Do I need internet?', 'No. Questions ship inside the app; the game is fully offline.'),
             ('How do I change the language?', 'Settings → Language. “Automatic” follows your device language (Turkish, English or Spanish; other languages fall back to English). New games draw from that language’s question bank, which includes its own local questions.'),
             ('How do I resume an unfinished game?', 'Tap the “Resume Game” card on the home screen. Starting a new game replaces the previous one.'),
             ('Can I enter decimals or negative numbers?', 'Yes. The keypad’s decimal key and the ± key handle both.'),
             ('An answer looks wrong.', 'Some answers are approximate and vary by source. If you think one is wrong, send it with “Report a bug”; the question text is enough.'),
             ('Where is my data?', 'All on your device: team names, preferences, the game in progress. Nothing is sent to a server. See the Privacy section below.')],
        privacy='Privacy Policy', privacy_lead='geswat needs no account, collects no data and sends nothing to a server. Here is what stays on your device.',
        terms='Terms of Use', terms_lead='geswat is a guessing game made for fun. By using the app you agree to the terms below.',
        eula_h='License agreement', eula_p=f'The app is distributed through the App Store and is subject to Apple’s standard End User License Agreement (EULA): <a href="{EULA}">apple.com/legal/…/stdeula</a>.',
        contact_h='Contact', contact_short=f'Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.',
        eyebrow_how='THE GAME', eyebrow_support='HELP', eyebrow_privacy='DATA', eyebrow_terms='RULES', updated='Last updated: 20 October 2026', lang_label='Language', foot_support='Support', foot_privacy='Privacy', foot_terms='Terms',
    ),
    'es': dict(
        title='geswat · Ni idea. Adivina.', desc='geswat es un juego de fiesta sin conexión para iPhone: dos equipos, una pregunta, gana la estimación más cercana.',
        nav_home='Juego', nav_how='Cómo se juega', nav_support='Soporte', nav_privacy='Privacidad', store='App Store',
        h1a='Ni idea.', h1b='Adivina.',
        lead='Dos equipos, un teléfono, una pregunta. Cada respuesta es un número; gana la estimación más cercana. Sin internet.',
        cta='Pronto en el App Store', cta2='¿Cómo se juega?',
        f=[('Un teléfono, dos equipos', 'Pásense el teléfono. Cada equipo ve solo su estimación hasta que se revela la respuesta.'),
           ('La respuesta en una recta', 'La respuesta correcta y las dos estimaciones en la misma línea. Quién estuvo más cerca, de un vistazo.'),
           ('Preguntas locales en cada idioma', 'Naturaleza, ciencia, historia, geografía, deportes, cultura, tecnología y cuerpo humano. Preguntas propias en español, inglés y turco.')],
        how='¿Cómo se juega?',
        steps=[('Formen los equipos', 'Escriban los nombres y elijan 5, 10 o 20 preguntas.'),
               ('Hagan su estimación', 'Cada pregunta pide un número. Los dos equipos escriben su estimación por turnos.'),
               ('Gana el más cercano', 'El equipo más cercano a la respuesta suma 1 punto. A igual distancia, suman los dos.')],
        support='Soporte', support_lead='¿Algo no funciona? Mira primero las preguntas frecuentes; si no encuentras la respuesta, escríbenos.',
        contact='Contáctanos', contact_p='Escríbenos para soporte, sugerencias y errores. Los botones abren tu propia app de correo.',
        mail_btn='Escribir a soporte', bug_btn='Informar un error', mail_subject='geswat soporte', bug_subject='geswat informe de error',
        bug_body='¿Qué pasó?\n\n\n¿Cómo lo reproducimos?\n1.\n2.\n3.\n\n---\nModelo de iPhone: \nVersión de iOS: \nVersión de geswat: \nIdioma: ',
        bug_note='Incluye el modelo de iPhone, la versión de iOS y la de geswat para que lo resolvamos antes.',
        faq_h='Preguntas frecuentes',
        faq=[('¿Cómo se juega?', 'Dos equipos comparten un teléfono. Cada pregunta pide un número; los dos equipos escriben su estimación por turnos y luego tocan “Mostrar respuesta”. El equipo más cercano suma 1 punto; a igual distancia, suman los dos. Al final gana quien tenga más puntos.'),
             ('¿Necesito internet?', 'No. Las preguntas están dentro de la app; el juego funciona sin conexión.'),
             ('¿Cómo cambio el idioma?', 'Ajustes → Idioma. “Automático” sigue el idioma del dispositivo (turco, inglés o español; otros idiomas usan inglés). Las partidas nuevas usan el banco de preguntas de ese idioma, con sus propias preguntas locales.'),
             ('¿Cómo continúo una partida?', 'Toca la tarjeta “Continuar partida” en la pantalla principal. Empezar una partida nueva reemplaza la anterior.'),
             ('¿Puedo escribir decimales o negativos?', 'Sí. La tecla de coma del teclado numérico y la tecla ± sirven para eso.'),
             ('Una respuesta parece incorrecta.', 'Algunas respuestas son aproximadas y varían según la fuente. Si crees que una está mal, envíala con “Informar un error”; basta con el texto de la pregunta.'),
             ('¿Dónde están mis datos?', 'Todo en tu dispositivo: nombres de equipos, preferencias y la partida en curso. No se envía nada a un servidor. Consulta la sección de Privacidad más abajo.')],
        privacy='Política de privacidad', privacy_lead='geswat no requiere cuenta, no recopila datos y no envía nada a un servidor. Esto es lo que se guarda en tu dispositivo.',
        terms='Términos de uso', terms_lead='geswat es un juego de estimaciones hecho para divertirse. Al usar la app aceptas los términos siguientes.',
        eula_h='Acuerdo de licencia', eula_p=f'La app se distribuye a través del App Store y está sujeta al Acuerdo de licencia de usuario final (EULA) estándar de Apple: <a href="{EULA}">apple.com/legal/…/stdeula</a>.',
        contact_h='Contacto', contact_short=f'Preguntas: <a href="mailto:{EMAIL}">{EMAIL}</a>.',
        eyebrow_how='EL JUEGO', eyebrow_support='AYUDA', eyebrow_privacy='DATOS', eyebrow_terms='REGLAS', updated='Última actualización: 20 de octubre de 2026', lang_label='Idioma', foot_support='Soporte', foot_privacy='Privacidad', foot_terms='Términos',
    ),
}

MOCK = {
    'tr': dict(a='Kartallar', b='Kaplanlar', q='Çita saatte yaklaşık kaç km hıza ulaşır?', turn='Kartallar · sıra sende', unit='km/sa', dec=','),
    'en': dict(a='Eagles', b='Tigers', q='How fast can a cheetah run, in km/h?', turn='Eagles · your turn', unit='km/h', dec='.'),
    'es': dict(a='Águilas', b='Tigres', q='¿A cuántos km/h corre un guepardo?', turn='Águilas · tu turno', unit='km/h', dec=','),
}

def ico(path, color='currentColor'):
    return f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

LEGAL_ICONS = {
    'privacy': [ico('<rect x="4" y="10" width="16" height="11" rx="2.5"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path>'),
                ico('<path d="M3 9c5-4.5 13-4.5 18 0M6.5 12.5c3-2.5 8-2.5 11 0M10 16c1.2-1 2.8-1 4 0"></path><path d="M3 3l18 18"></path>'),
                ico('<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"></path>'),
                ico('<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"></path><path d="M9 12l2 2 4-4"></path>'),
                ico('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M3 8l9 6 9-6"></path>')],
    'terms': [ico('<rect x="3" y="3" width="18" height="18" rx="4"></rect><circle cx="8.5" cy="8.5" r="1.2" fill="currentColor"></circle><circle cx="15.5" cy="15.5" r="1.2" fill="currentColor"></circle><circle cx="15.5" cy="8.5" r="1.2" fill="currentColor"></circle><circle cx="8.5" cy="15.5" r="1.2" fill="currentColor"></circle>'),
              ico('<circle cx="12" cy="12" r="9"></circle><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7"></path><circle cx="12" cy="17" r="0.7" fill="currentColor"></circle>'),
              ico('<path d="M5 4h11l3 3v13H5z"></path><path d="M8 4v5h7V4M8 20v-6h8v6"></path>'),
              ico('<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"></path><path d="M4 7.5l8 4.5 8-4.5M12 12v9"></path>'),
              ico('<path d="M6 3h9l4 4v14H6z"></path><path d="M14 3v5h5M9 13h6M9 17h6"></path>'),
              ico('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M3 8l9 6 9-6"></path>')],
}

ICONS = {
    'teams': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E8652B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"></circle><circle cx="17" cy="9" r="2.5"></circle><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M15 15c2.8 0 5 2 5 5"></path></svg>',
    'line': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C5CE0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M8 8v8M16 8v8"></path><circle cx="12" cy="12" r="2.5" fill="#7C5CE0"></circle></svg>',
    'star': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9A7A00" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 9.3l6.1-.7z"></path></svg>',
    'globe': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"></path></svg>',
    'apple': '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.5 2-3.7 2.1-3.8-1.2-1.7-3-1.9-3.6-2-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.8-1.7 0-3.2 1-4.1 2.5-1.8 3-.5 7.6 1.3 10.1.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.3.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.9-1.1-2.9-4.1zM14 5.1c.7-.9 1.2-2.1 1-3.3-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.2 1.2.1 2.3-.6 3.1-1.5z"></path></svg>',
}


def enc(s):
    from urllib.parse import quote
    return quote(s, safe='')


def L(lang, key, tag='span'):
    cls = ' class="eyebrow"' if key.startswith('eyebrow_') else ''
    return f'<{tag} data-lang="{lang}"{cls}>{T[lang][key]}</{tag}>'


def tri(key, tag='span'):
    return ''.join(L(l, key, tag) for l in LANGS)


def section_legal(key, lead_key, lang, extras):
    t = T[lang]
    out = f'      <div data-lang="{lang}">\n        <span class="eyebrow">{t["eyebrow_" + key]}</span>\n        <h2 class="section">{t[key]}</h2>\n        <p class="lead">{t[lead_key]}</p>\n        <span class="chip">{t["updated"]}</span>\n        <div class="legal-grid">\n'
    for i, (a, b) in enumerate(legal(lang, key) + extras(lang)):
        b2 = b if '<a ' in b else html.escape(b)
        icon = LEGAL_ICONS[key][i % len(LEGAL_ICONS[key])]
        out += f'          <div class="lcard"><div class="ic">{icon}</div><h3>{html.escape(a)}</h3><p>{b2}</p></div>\n'
    return out + '        </div>\n      </div>\n'


def page():
    head = '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    head += f'<title>{T["en"]["title"]}</title>\n' + ''.join(f'<title data-lang="{l}">{T[l]["title"]}</title>\n' for l in LANGS)
    head += f'<meta name="description" content="{T["en"]["desc"]}">\n' + ''.join(f'<meta name="description" data-lang="{l}" content="{T[l]["desc"]}">\n' for l in LANGS)
    head += '<link rel="icon" href="assets/favicon.png">\n<link rel="apple-touch-icon" href="assets/icon-512.png">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap">\n<link rel="stylesheet" href="site.css">\n</head>\n<body>\n'

    nav = f'''<header class="topbar">
  <div class="pill">
    <a class="brand" href="#top" aria-label="geswat"><img src="assets/icon-512.png" alt="" width="30" height="30"><span>geswat</span></a>
    <nav class="nav" aria-label="Site">
      <a href="#top" data-section="top">{tri('nav_home')}</a>
      <a href="#how" data-section="how">{tri('nav_how')}</a>
      <a href="#support" data-section="support">{tri('nav_support')}</a>
      <a href="#privacy" data-section="privacy">{tri('nav_privacy')}</a>
    </nav>
    <a class="store" href="#" aria-disabled="true">{ICONS['apple']}<span>App Store</span></a>
  </div>
</header>
'''

    m = lambda l, k: MOCK[l][k]
    phone = f'''    <div class="phone" aria-hidden="true">
      <div class="blob a"></div><div class="blob b"></div>
      <div class="frame">
        <div class="btn mute"></div><div class="btn vol1"></div><div class="btn vol2"></div><div class="btn power"></div>
        <div class="screen">
          <div class="island"></div>
          <div class="mock-score">
            <div class="side t">{''.join(f'<span data-lang="{l}">{m(l,"a")}</span>' for l in LANGS)}<b>2</b></div>
            <div class="round">4<span>/10</span></div>
            <div class="side l">{''.join(f'<span data-lang="{l}">{m(l,"b")}</span>' for l in LANGS)}<b>1</b></div>
          </div>
          <div class="mock-q">{''.join(f'<span data-lang="{l}">{m(l,"q")}</span>' for l in LANGS)}</div>
          <div class="mock-turn"><span class="on">{''.join(f'<span data-lang="{l}">{m(l,"turn")}</span>' for l in LANGS)}</span><span>{''.join(f'<span data-lang="{l}">{m(l,"b")}</span>' for l in LANGS)}</span></div>
          <div class="mock-num">95<small>{''.join(f'<span data-lang="{l}">{m(l,"unit")}</span>' for l in LANGS)}</small></div>
          <div class="mock-bar"></div>
          <div class="mock-pad"><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span class="m">{''.join(f'<span data-lang="{l}">{m(l,"dec")}</span>' for l in LANGS)}</span><span>0</span><span class="m">±</span></div>
        </div>
      </div>
    </div>
'''

    hero = f'''<main id="top" class="wrap">
  <section class="hero">
    <div class="hero-text">
      {''.join(f'<div data-lang="{l}"><h1>{T[l]["h1a"]}<br><em>{T[l]["h1b"]}</em></h1><p>{T[l]["lead"]}</p></div>' for l in LANGS)}
      <div class="cta-row">
        <a class="cta" href="#" aria-disabled="true">{ICONS['apple']}{tri('cta')}</a>
        <a class="cta ghost" href="#how">{tri('cta2')}</a>
      </div>
    </div>
{phone}  </section>
'''

    icons = ['teams', 'line', 'star']
    cls = ['t', 'l', 's']
    features = '  <section class="features">\n'
    for i in range(3):
        features += f'    <div class="card"><div class="ic {cls[i]}">{ICONS[icons[i]]}</div>'
        features += ''.join(f'<div data-lang="{l}"><h3>{T[l]["f"][i][0]}</h3><p>{T[l]["f"][i][1]}</p></div>' for l in LANGS)
        features += '</div>\n'
    features += '  </section>\n'

    how = f'  <section id="how" class="block">\n    {tri("eyebrow_how", "span")}\n    <h2 class="section">{tri("how")}</h2>\n    <div class="steps">\n'
    for i in range(3):
        how += f'      <div class="step"><div class="step-copy"><div class="n">{i+1}</div><div>'
        how += ''.join(f'<div data-lang="{l}"><h3>{T[l]["steps"][i][0]}</h3><p>{T[l]["steps"][i][1]}</p></div>' for l in LANGS)
        how += '</div></div><div class="phone step-phone"><div class="frame">'
        how += '<span class="btn mute"></span><span class="btn vol1"></span><span class="btn vol2"></span><span class="btn power"></span>'
        how += '<div class="screen"><div class="island" aria-hidden="true"></div>'
        stage = ['setup', 'guess', 'answer'][i]
        how += ''.join(f'<img data-lang="{l}" class="shot" src="assets/how-{stage}-{l}.webp" alt="{html.escape(T[l]["steps"][i][0], quote=True)}" width="1170" height="2532" loading="eager" decoding="async">' for l in LANGS)
        # A consistent presentation status bar masks the device's live clock and indicators.
        how += '<div class="capture-status" aria-hidden="true"><span>09:41</span><svg viewBox="0 0 64 16" fill="currentColor"><rect x="0" y="10" width="3" height="5" rx="1"/><rect x="5" y="7" width="3" height="8" rx="1"/><rect x="10" y="4" width="3" height="11" rx="1"/><rect x="15" y="1" width="3" height="14" rx="1"/><path d="M23 5a13 13 0 0 1 18 0l-2 2a10 10 0 0 0-14 0zm4 4a7 7 0 0 1 10 0l-2 2a4 4 0 0 0-6 0zm4 4a2 2 0 0 1 2 0l-1 2z"/><rect x="46" y="2" width="15" height="12" rx="3" fill="none" stroke="currentColor"/><rect x="48" y="4" width="11" height="8" rx="1"/><path d="M63 6v4" stroke="currentColor" stroke-width="2"/></svg></div>'
        how += '</div></div></div></div>\n'
    how += '    </div>\n  </section>\n'

    support = '  <section id="support" class="block">\n'
    support += '    ' + tri('eyebrow_support', 'span') + '\n'
    support += ''.join(f'    <div data-lang="{l}"><h2 class="section">{T[l]["support"]}</h2><p class="lead">{T[l]["support_lead"]}</p></div>\n' for l in LANGS)
    support += '    <div class="contact">\n      <div class="contact-main">\n        <div class="contact-ic">' + ico('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M3 8l9 6 9-6"></path>', '#FFD45C') + '</div>\n'
    support += ''.join(f'        <div data-lang="{l}"><h3>{T[l]["contact"]}</h3><p>{T[l]["contact_p"]}</p></div>\n' for l in LANGS)
    support += '      </div>\n      <div class="contact-actions">\n        <div class="cta-col">\n'
    for l in LANGS:
        t = T[l]
        support += f'          <a class="cta" data-lang="{l}" href="mailto:{EMAIL}?subject={enc(t["mail_subject"])}">{t["mail_btn"]}</a>\n'
        support += f'          <a class="cta dark" data-lang="{l}" href="mailto:{EMAIL}?subject={enc(t["bug_subject"])}&body={enc(t["bug_body"])}">{t["bug_btn"]}</a>\n'
    support += '        </div>\n        ' + ''.join(f'<p class="meta" data-lang="{l}">{T[l]["bug_note"]}</p>' for l in LANGS) + '\n      </div>\n    </div>\n'
    support += f'    <div class="faq panel">\n      <h3 class="sub">{tri("faq_h")}</h3>\n'
    for l in LANGS:
        support += f'        <div data-lang="{l}">\n' + ''.join(f'          <details><summary>{q}</summary><p>{a}</p></details>\n' for q, a in T[l]['faq']) + '        </div>\n'
    support += '    </div>\n  </section>\n'

    privacy = '  <section id="privacy" class="block legal">\n' + ''.join(section_legal('privacy', 'privacy_lead', l, lambda l: [(T[l]['contact_h'], T[l]['contact_short'])]) for l in LANGS) + '  </section>\n'
    terms = '  <section id="terms" class="block legal">\n' + ''.join(section_legal('terms', 'terms_lead', l, lambda l: [(T[l]['eula_h'], T[l]['eula_p']), (T[l]['contact_h'], T[l]['contact_short'])]) for l in LANGS) + '  </section>\n'

    footer = f'''  <footer class="footer">
    <div class="foot-left">© 2026 brocan · geswat</div>
    <div class="foot-links">
      <a href="#support">{tri('foot_support')}</a>
      <a href="#privacy">{tri('foot_privacy')}</a>
      <a href="#terms">{tri('foot_terms')}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
    <div class="lang">{ICONS['globe']}<span class="lang-current">Türkçe</span>
      <select class="lang-select" aria-label="Language"><option value="tr">Türkçe</option><option value="en">English</option><option value="es">Español</option></select>
    </div>
  </footer>
</main>
<script src="site.js"></script>
</body>
</html>
'''
    return head + nav + hero + features + how + support + privacy + terms + footer


def redirect(target, title):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>geswat · {title}</title>
<meta http-equiv="refresh" content="0; url=index.html#{target}">
<link rel="canonical" href="index.html#{target}">
<script>location.replace('index.html' + location.search + '#{target}');</script>
</head>
<body><p><a href="index.html#{target}">geswat · {title}</a></p></body>
</html>
'''


if __name__ == '__main__':
    (DOCS / 'index.html').write_text(page(), encoding='utf8')
    for name, target, title in [('support', 'support', 'Support'), ('privacy', 'privacy', 'Privacy Policy'), ('terms', 'terms', 'Terms of Use')]:
        (DOCS / f'{name}.html').write_text(redirect(target, title), encoding='utf8')
    print('index.html + redirect pages written')
