// Language: explicit ?lang= → saved choice → device/browser language → English.
// Also: smooth anchor scrolling that accounts for the floating nav, and active-link highlighting.
(function () {
  var SUPPORTED = ['tr', 'en', 'es'];
  function pick() {
    var q = new URLSearchParams(location.search).get('lang');
    if (SUPPORTED.indexOf(q) >= 0) return q;
    try { var s = localStorage.getItem('geswat-lang'); if (SUPPORTED.indexOf(s) >= 0) return s; } catch (e) {}
    var nav = (navigator.language || 'en').slice(0, 2).toLowerCase();
    return SUPPORTED.indexOf(nav) >= 0 ? nav : 'en';
  }
  function apply(lang, fromUser) {
    document.documentElement.setAttribute('lang', lang);
    try { localStorage.setItem('geswat-lang', lang); } catch (e) {}
    var selects = document.querySelectorAll('select.lang-select');
    for (var i = 0; i < selects.length; i++) {
      selects[i].value = lang;
      var cur = selects[i].parentNode.querySelector('.lang-current');
      if (cur) cur.textContent = selects[i].options[selects[i].selectedIndex].textContent;
    }
    var t = document.querySelector('title[data-lang="' + lang + '"]');
    if (t) document.title = t.textContent;
    var d = document.querySelector('meta[name="description"][data-lang="' + lang + '"]');
    var m = document.querySelector('meta[name="description"]:not([data-lang])');
    if (d && m) m.setAttribute('content', d.getAttribute('content'));
    if (fromUser && history.replaceState) {
      var url = new URL(location.href); url.searchParams.delete('lang');
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    }
  }
  apply(pick(), false);
  document.addEventListener('change', function (e) {
    if (e.target && e.target.classList && e.target.classList.contains('lang-select')) apply(e.target.value, true);
  });

  // Active section in the nav.
  var links = document.querySelectorAll('.nav a[data-section]');
  var sections = [];
  for (var k = 0; k < links.length; k++) {
    var el = document.getElementById(links[k].getAttribute('data-section'));
    if (el) sections.push({ el: el, link: links[k] });
  }
  function highlight() {
    var y = window.scrollY + 140;
    var current = sections[0];
    for (var j = 0; j < sections.length; j++) if (sections[j].el.offsetTop <= y) current = sections[j];
    for (var n = 0; n < sections.length; n++) {
      if (sections[n] === current) sections[n].link.setAttribute('aria-current', 'page');
      else sections[n].link.removeAttribute('aria-current');
    }
  }
  if (sections.length) { highlight(); window.addEventListener('scroll', highlight, { passive: true }); }
})();
