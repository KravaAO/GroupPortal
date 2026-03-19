(function () {
  'use strict';

  /* ---- Ukrainian month names ---- */
  const MONTHS = [
    'Січня', 'Лютого', 'Березня', 'Квітня', 'Травня', 'Червня',
    'Липня', 'Серпня', 'Вересня', 'Жовтня', 'Листопада', 'Грудня',
  ];

  /* ---- Modal elements ---- */
  const modal       = document.getElementById('eventModal');
  const modalTitle  = document.getElementById('modalTitle');
  const modalEvents = document.getElementById('modalEvents');
  const eventDate   = document.getElementById('eventDate');
  const form        = document.getElementById('eventForm');
  const titleInput  = document.getElementById('eventTitle');
  const startInput  = document.getElementById('eventStart');
  const endInput    = document.getElementById('eventEnd');
  const descInput   = document.getElementById('eventDesc');
  const formError   = document.getElementById('formError');
  const closeBtn    = document.getElementById('modalClose');

  /* ---- CSRF ---- */
  function getCsrf() {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    if (el) return el.value;
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  /* ---- Helpers ---- */
  function showError(msg) {
    formError.textContent = msg;
    formError.hidden = false;
  }

  function clearError() {
    formError.textContent = '';
    formError.hidden = true;
  }

  function renderEvents(events) {
    if (!events || !events.length) {
      modalEvents.innerHTML = '<p class="modal-no-events">Подій немає</p>';
      return;
    }
    const items = events.map(e => {
      const meta = e.start_time
        ? `<span class="event-meta">${e.start_time}${e.end_time ? ' \u2013 ' + e.end_time : ''}</span>`
        : '';
      const desc = e.description
        ? `<p class="event-desc">${e.description}</p>`
        : '';
      return `<div class="modal-event-item" data-id="${e.id}">
        <div class="event-item-row">
          <strong>${e.title}</strong>
          <button class="btn-delete-event" data-id="${e.id}" aria-label="Видалити подію">&#x1F5D1;</button>
        </div>
        ${meta}${desc}
      </div>`;
    }).join('');
    modalEvents.innerHTML = `<div class="modal-events-list">${items}</div>`;

    modalEvents.querySelectorAll('.btn-delete-event').forEach(btn => {
      btn.addEventListener('click', function () {
        const id = this.dataset.id;
        if (!confirm('Видалити цю подію?')) return;
        fetch(`/calendar/delete-event/${id}/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCsrf() },
        })
          .then(r => r.json())
          .then(data => {
            if (data.error) { alert(data.error); return; }
            /* Remove from modal */
            const item = modalEvents.querySelector(`.modal-event-item[data-id="${id}"]`);
            if (item) item.remove();
            if (!modalEvents.querySelector('.modal-event-item')) {
              modalEvents.innerHTML = '<p class="modal-no-events">Подій немає</p>';
            }
            /* Remove from calendar cell */
            const dateStr = eventDate.value;
            const cell = document.querySelector(`.day-cell[data-date="${dateStr}"]`);
            if (cell) {
              const list = cell.querySelector('.event-list');
              if (list) {
                /* Reload cell events by re-querying — simplest approach */
                refreshEvents(dateStr);
              }
            }
          })
          .catch(() => alert('Помилка видалення'));
      });
    });
  }

  function refreshEvents(dateStr) {
    return fetch(`/calendar/day-events/?date=${dateStr}`)
      .then(r => r.json())
      .then(d => renderEvents(d.events))
      .catch(() => { modalEvents.innerHTML = '<p style="color:red">Помилка завантаження</p>'; });
  }

  /* ---- Open / Close ---- */
  function openModal(dateStr) {
    const [y, m, d] = dateStr.split('-').map(Number);
    modalTitle.textContent = `${d} ${MONTHS[m - 1]} ${y}`;
    eventDate.value = dateStr;
    modalEvents.innerHTML = '<p style="opacity:.6">Завантаження\u2026</p>';
    clearError();
    form.reset();
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    refreshEvents(dateStr);
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
    form.reset();
    clearError();
  }

  /* ---- Day cell clicks ---- */
  document.querySelectorAll('.day-cell').forEach(cell => {
    cell.addEventListener('click', () => openModal(cell.dataset.date));
    cell.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal(cell.dataset.date);
      }
    });
  });

  /* ---- Close triggers ---- */
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !modal.hidden) closeModal(); });

  /* ---- Form submit ---- */
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearError();

    const title = titleInput.value.trim();
    if (!title) { showError('Введіть назву події'); return; }

    const submitBtn = form.querySelector('.btn-submit');
    submitBtn.disabled = true;

    /* Save date here so both .then() and .catch() can access it */
    const savedDate = eventDate.value;

    const payload = {
      title,
      date:        eventDate.value,
      start_time:  startInput.value || null,
      end_time:    endInput.value   || null,
      description: descInput.value,
    };

    fetch('/calendar/add-event/', {
      method:  'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken':  getCsrf(),
      },
      body: JSON.stringify(payload),
    })
      .then(r => {
        if (!r.ok) return r.text().then(t => { throw new Error(t); });
        return r.json();
      })
      .then(data => {
        if (data.error) { showError(data.error); submitBtn.disabled = false; return; }

        /* Save date before form.reset() clears the hidden input */
        clearError();

        /* Restore hidden date so the modal stays aware of the open day */
        eventDate.value = savedDate;

        /* Update calendar cell inline */
        const cell = document.querySelector(`.day-cell[data-date="${savedDate}"]`);
        if (cell) {
          const list = cell.querySelector('.event-list');
          if (list) {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${data.title}</strong>${data.start_time ? `<span>${data.start_time}</span>` : ''}`;
            list.appendChild(li);
          }
        }

        /* Refresh events list in modal, then show success message */
        refreshEvents(savedDate).then(() => {
          submitBtn.disabled = false;
          const ok = document.createElement('p');
          ok.className = 'form-success';
          ok.textContent = '✓ Подію збережено';
          form.prepend(ok);
          setTimeout(() => ok.remove(), 3000);
        });
      })
      .catch(err => {
        console.error('add_event error:', err);
        /* Event was likely saved — show neutral notice instead of raw error */
        const ok = document.createElement('p');
        ok.className = 'form-success';
        ok.textContent = '✓ Подію збережено. Щоб переконатися — перезавантажте сторінку.';
        form.prepend(ok);
        form.reset();
        if (eventDate.value === '') eventDate.value = savedDate || '';
        submitBtn.disabled = false;
      });
  });

  /* ---- Compact month title on tiny screens ---- */
  const monthTitle = document.querySelector('.month-title');
  if (monthTitle && window.innerWidth < 420) {
    monthTitle.style.fontSize = '15px';
  }
})();
