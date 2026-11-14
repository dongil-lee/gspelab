// Mobile menu toggle and keyboard/touch support for the People dropdown.
document.addEventListener('DOMContentLoaded', function () {
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open);
    });
  }

  document.querySelectorAll('.dropdown-toggle').forEach(function (btn) {
    var item = btn.closest('.has-dropdown');
    btn.addEventListener('click', function () {
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        item.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  });

  document.addEventListener('click', function (e) {
    document.querySelectorAll('.has-dropdown.open').forEach(function (item) {
      if (!item.contains(e.target)) {
        item.classList.remove('open');
        item.querySelector('.dropdown-toggle').setAttribute('aria-expanded', 'false');
      }
    });
  });
});
