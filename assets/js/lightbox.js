// Enlarges photos wrapped in <a data-lightbox> in an overlay, with previous/next.
// Without JavaScript the links simply open the image file.
document.addEventListener('DOMContentLoaded', function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('a[data-lightbox]'));
  if (!links.length) return;

  var overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Enlarged photo');
  overlay.innerHTML =
    '<button class="lightbox-close" aria-label="Close">&times;</button>' +
    '<button class="lightbox-prev" aria-label="Previous photo">&#8249;</button>' +
    '<img alt="">' +
    '<button class="lightbox-next" aria-label="Next photo">&#8250;</button>';
  document.body.appendChild(overlay);

  var img = overlay.querySelector('img');
  var current = 0;
  var lastFocus = null;

  function show(i) {
    current = (i + links.length) % links.length;
    img.src = links[current].href;
    img.alt = links[current].querySelector('img').alt;
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    overlay.querySelector('.lightbox-close').focus();
  }

  function close() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      open(i);
    });
  });

  overlay.addEventListener('click', function (e) {
    if (e.target.classList.contains('lightbox-prev')) show(current - 1);
    else if (e.target.classList.contains('lightbox-next')) show(current + 1);
    else if (e.target !== img) close();
  });

  document.addEventListener('keydown', function (e) {
    if (!overlay.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(current - 1);
    else if (e.key === 'ArrowRight') show(current + 1);
  });
});
