(() => {
  const translations = {
    en: {
      'skip-link': 'Skip to content',
      'nav-support': 'Support',
      'nav-privacy': 'Privacy',
      'nav-documentation': 'Documentation',
      'primary-nav': 'Primary navigation'
    },
    ar: {
      'skip-link': 'انتقل إلى المحتوى',
      'nav-support': 'الدعم',
      'nav-privacy': 'الخصوصية',
      'nav-documentation': 'التوثيق',
      'primary-nav': 'التنقل الرئيسي'
    }
  };

  const toggles = document.querySelectorAll('[data-language-toggle]');
  const panels = document.querySelectorAll('[data-lang-panel]');
  if (!toggles.length || !panels.length) return;

  const applyLanguage = (language) => {
    const next = language === 'ar' ? 'ar' : 'en';
    const copy = translations[next];
    const root = document.documentElement;
    root.lang = next;
    root.dir = next === 'ar' ? 'rtl' : 'ltr';
    panels.forEach((panel) => {
      panel.hidden = panel.dataset.langPanel !== next;
    });
    document.querySelectorAll('[data-i18n]').forEach((element) => {
      const value = copy[element.dataset.i18n];
      if (value) element.textContent = value;
    });
    document.querySelectorAll('[data-i18n-aria]').forEach((element) => {
      const value = copy[element.dataset.i18nAria];
      if (value) element.setAttribute('aria-label', value);
    });
    const title = next === 'ar' ? root.dataset.titleAr : root.dataset.titleEn;
    const description = next === 'ar' ? root.dataset.descriptionAr : root.dataset.descriptionEn;
    if (title) document.title = title;
    const descriptionElement = document.querySelector('meta[name="description"]');
    if (description && descriptionElement) descriptionElement.content = description;
    toggles.forEach((toggle) => {
      toggle.textContent = next === 'ar' ? 'English' : 'العربية';
      toggle.setAttribute('aria-label', next === 'ar' ? 'Switch to English' : 'التبديل إلى العربية');
      toggle.setAttribute('aria-pressed', String(next === 'ar'));
    });
    try { localStorage.setItem('ayyashking-language', next); } catch (_) {}
  };

  let saved = 'en';
  try { saved = localStorage.getItem('ayyashking-language') || 'en'; } catch (_) {}
  applyLanguage(saved);
  toggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      applyLanguage(document.documentElement.lang === 'ar' ? 'en' : 'ar');
    });
  });

  document.querySelectorAll('.support-form').forEach((form) => {
    const fileInput = form.querySelector('[data-max-bytes]');
    const error = form.querySelector('.form-error');
    const submit = form.querySelector('button[type="submit"]');
    if (!fileInput || !error || !submit) return;

    const clearError = () => {
      error.hidden = true;
      error.textContent = '';
      fileInput.removeAttribute('aria-invalid');
    };
    fileInput.addEventListener('change', clearError);
    form.addEventListener('submit', (event) => {
      clearError();
      const file = fileInput.files && fileInput.files[0];
      const maximum = Number(fileInput.dataset.maxBytes);
      if (file && Number.isFinite(maximum) && file.size > maximum) {
        event.preventDefault();
        error.textContent = document.documentElement.lang === 'ar'
          ? error.dataset.errorAr
          : error.dataset.errorEn;
        error.hidden = false;
        fileInput.setAttribute('aria-invalid', 'true');
        fileInput.focus();
        return;
      }
      submit.disabled = true;
      submit.textContent = document.documentElement.lang === 'ar' ? 'جارٍ الإرسال…' : 'Sending…';
    });
  });
})();
