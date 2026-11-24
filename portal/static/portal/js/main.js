// ---------- 1. Mobile menu button ----------
const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');

if (menuBtn) {
    menuBtn.addEventListener('click', function () {
        navLinks.classList.toggle('open');
    });
}


// ---------- 2. Hide flash messages after 4 seconds ----------
setTimeout(function () {
    document.querySelectorAll('.message').forEach(function (msg) {
        msg.style.display = 'none';
    });
}, 4000);


// ---------- 3. Falling snow in the hero section ----------
const hero = document.querySelector('.hero');

if (hero) {
    for (let i = 0; i < 40; i++) {
        const flake = document.createElement('span');
        flake.className = 'snowflake';
        flake.textContent = '•';
        flake.style.left = Math.random() * 100 + '%';
        flake.style.fontSize = (Math.random() * 10 + 6) + 'px';
        flake.style.animationDuration = (Math.random() * 8 + 6) + 's';
        flake.style.animationDelay = (Math.random() * -14) + 's';
        hero.appendChild(flake);
    }
}


// ---------- 4. Count-up animation for the stats ----------
document.querySelectorAll('.stat-number').forEach(function (el) {
    const target = parseInt(el.dataset.target);
    let current = 0;
    if (target === 0) return;

    const timer = setInterval(function () {
        current++;
        el.textContent = current;
        if (current >= target) {
            clearInterval(timer);
        }
    }, 80);
});


// ---------- 5. Fade cards in when they scroll into view ----------
const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(function (el) {
    observer.observe(el);
});
