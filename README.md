# PolarPortal

**Integrated Polar Science Outreach Knowledge Repository and Media Dissemination Portal**

A Django website that collects polar science knowledge (Arctic & Antarctic) in one place,
explains it in simple language, and shares media such as photos, videos, podcasts and documents.

## 🌐 Live Demo

**https://shreyashlm10.pythonanywhere.com**

| Page | Link |
|------|------|
| Home | https://shreyashlm10.pythonanywhere.com/ |
| Knowledge Hub | https://shreyashlm10.pythonanywhere.com/articles/ |
| Media Gallery | https://shreyashlm10.pythonanywhere.com/media/ |
| Login | https://shreyashlm10.pythonanywhere.com/login/ |

Try the member features with the demo account: username `demo`, password `demo@123`.

## Tech stack

- **Backend:** Python 3.13, Django 6.1
- **Database:** SQLite
- **Frontend:** Django templates, plain CSS and vanilla JavaScript (no frameworks)
- **Hosting:** PythonAnywhere

## How to run on your computer

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data        # fills the site with sample content and the demo user
python manage.py createsuperuser  # create your own admin account
python manage.py runserver
```

Open http://127.0.0.1:8000/ in the browser.
Admin panel: http://127.0.0.1:8000/admin/  (log in with the account made by `createsuperuser`)
Demo user:   http://127.0.0.1:8000/login/  (username `demo`, password `demo@123`)

## Pages

| Page | URL | What it does |
|------|-----|--------------|
| Home | `/` | Hero section, stats, topics, featured articles, Arctic vs Antarctic, latest media, events |
| Knowledge Hub | `/articles/` | All articles with search + filter by topic and region |
| Article | `/articles/<id>/` | Full article, view counter, related articles |
| Media Gallery | `/media/` | Photos, videos, podcasts, documents with type filter |
| Events | `/events/` | Upcoming and past outreach events |
| About | `/about/` | Mission and features of the portal |
| Contact | `/contact/` | Contact form (messages saved to database) |
| Sign Up | `/signup/` | Create an account (Django's `UserCreationForm`) |
| Login / Logout | `/login/`, `/logout/` | Django's built-in `LoginView` and `LogoutView` |
| Dashboard | `/dashboard/` | **Login required.** User's bookmarks and submitted articles with status |
| Submit Article | `/submit/` | **Login required.** Users write an article; it waits for admin approval |
| Bookmark | `/articles/<id>/bookmark/` | **Login required.** Save / un-save an article (button on the article page) |

## Login features

- Reading is **public**; logging in only adds extra features (outreach should be open to everyone).
- `@login_required` on a view sends guests to the login page automatically.
- Submitted articles are saved with `is_approved = False`. The admin ticks **Is approved** in the admin panel and the article goes live.
- `Bookmark` links a `User` and an `Article` (two ForeignKeys). `unique_together` stops the same article being saved twice.

## Content and sources

All 14 Knowledge Hub articles are **written in our own simple words** by the "PolarPortal Editorial Team"
and each one **cites the real research it is based on** (`source` and `source_url` fields on Article).
Nothing is copied from the original papers.

| Article | Based on |
|---|---|
| Ice Cores | Lüthi et al. (2008), *Nature* |
| Arctic Sea Ice | Stroeve & Notz (2018), *Environmental Research Letters* |
| Emperor Penguins | Fretwell et al. (2012), *PLoS ONE* |
| Polar Bears | Stirling & Derocher (2012), *Global Change Biology* |
| Permafrost | Schuur et al. (2015), *Nature* |
| Antarctic Ice Sheet | Fretwell et al. (2013), *The Cryosphere* (Bedmap2) |
| Why the Poles Matter | Rantanen et al. (2022), *Communications Earth & Environment* |
| Krill | Atkinson et al. (2004), *Nature* |
| Icebergs & Calving | Scambos et al. (2004), *Geophysical Research Letters* |
| India in Antarctica | NCPOR, Ministry of Earth Sciences |
| Antarctic Treaty | Secretariat of the Antarctic Treaty |
| Aurora | NOAA Space Weather Prediction Center |
| Midnight Sun & Polar Night | NASA Space Place |
| Life at a Research Station | British Antarctic Survey |

Media Gallery items link to real resources from NASA, NOAA, NSIDC, NCPOR, BAS and the Antarctic Treaty Secretariat.

## Project structure

```
polarportal/            -> project settings and main urls
portal/                 -> our app
    models.py           -> database tables (Category, Article, Bookmark, MediaItem, Event, ContactMessage, Subscriber)
    views.py            -> logic for every page
    urls.py             -> links each URL to a view
    forms.py            -> Contact, Subscribe and Submit Article forms
    admin.py            -> what the admin panel shows
    templates/portal/   -> HTML pages (base.html is the common layout)
    static/portal/      -> style.css and main.js
    management/commands/seed_data.py -> sample content
```

## How it works (MVT pattern)

1. The user opens a URL, e.g. `/articles/?q=ice`.
2. `urls.py` sends the request to the matching function in `views.py`.
3. The view gets data from the database through the **models** (e.g. `Article.objects.filter(...)`).
4. The view passes the data to a **template**, which builds the HTML page.
5. Admins add or edit content from `/admin/`, so no code changes are needed for new articles.

## Deployment (PythonAnywhere)

The live site runs with these settings, set in the PythonAnywhere WSGI file (not stored in this repository):

- `DJANGO_DEBUG=False` turns off debug mode, so visitors see a friendly 404 page instead of error details
- `python manage.py collectstatic` copies CSS/JS into `staticfiles/`, which PythonAnywhere serves at `/static/`

To update the live site after pushing new code:

```bash
cd ~/PolarPortal && git pull && workon polarenv && python manage.py migrate && python manage.py collectstatic --noinput
```

Then click **Reload** on the PythonAnywhere Web tab.
