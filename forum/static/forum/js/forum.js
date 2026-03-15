document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form.forum-form').forEach(function (form) {
    form.classList.add('needs-validation');

    Array.from(form.querySelectorAll('input, textarea, select')).forEach(function (el) {
      if (!el.classList.contains('form-control') && !el.classList.contains('form-check-input')) {
        el.classList.add('form-control');
      }
    });

    Array.from(form.querySelectorAll('button[type="submit"]')).forEach(function (btn) {
      btn.classList.add('btn', 'btn-primary');
    });

    var first = form.querySelector('input, textarea, select');
    if (first) {
      first.focus();
    }
  });

  if (typeof bootstrap !== 'undefined') {
    document.querySelectorAll('.toast').forEach(function (toastEl) {
      var toast = new bootstrap.Toast(toastEl, { delay: 4500 });
      toast.show();
    });
  }

  var current = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(function (link) {
    if (link.getAttribute('href') === current) {
      link.classList.add('active');
    }
  });
});
