"""
Fills the database with sample polar science content so the website
doesn't look empty.

Run it with:   python manage.py seed_data

It is safe to run more than once. Categories and articles are found by
their name/title and UPDATED (not deleted), so their ID numbers - and
therefore their web addresses like /articles/42/ - never change.
Media and events are simply deleted and added again.
"""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import Category, Article, MediaItem, Event, Bookmark


CATEGORIES = [
    ('Glaciology & Ice Sheets', '🧊', 'Glaciers, ice sheets, ice cores and what frozen water tells us about Earth.'),
    ('Polar Wildlife', '🐧', 'Penguins, polar bears, seals, whales and life that survives the extreme cold.'),
    ('Climate Change', '🌡️', 'How a warming world is changing the poles, and how the poles change the world.'),
    ('Oceans & Sea Ice', '🌊', 'Frozen seas, ocean currents and the floating ice that covers the polar oceans.'),
    ('Expeditions & Stations', '🚩', 'Research stations, expeditions and the people who live and work on the ice.'),
    ('Aurora & Space Weather', '🌌', 'The northern and southern lights, and the space science behind them.'),
]


# Every article is written in our own simple words by the PolarPortal team,
# and is based on a real published research paper or official source.
AUTHOR = 'PolarPortal Editorial Team'

# Most articles use their category's icon (e.g. 🧊 for Glaciology).
# These ones need their own icon because the category icon doesn't fit them.
ARTICLE_ICONS = {
    'Polar Bears: Hunters of the Sea Ice': '🐻‍❄️',
    'Krill: The Tiny Animal That Feeds Antarctica': '🦐',
    'Why Seals Can Hold Their Breath for So Long': '🦭',
    'Midnight Sun and Polar Night: Why Days Get So Strange': '☀️',
}

# (title, category name, region, featured, source, source link, summary, content)
ARTICLES = [
    (
        'Ice Cores: Reading 800,000 Years of Climate History',
        'Glaciology & Ice Sheets', 'antarctic', True,
        'Lüthi, D. et al. (2008). High-resolution carbon dioxide concentration record 650,000–800,000 years before present. Nature, 453.',
        'https://doi.org/10.1038/nature06949',
        'Tiny air bubbles trapped deep in Antarctic ice hold a record of Earth\'s past atmosphere.',
        """Every year, snow falls on the Antarctic ice sheet and does not melt. Over thousands of years each layer gets buried under new snow and is slowly pressed into solid ice. Little pockets of air get trapped between the snow grains, and those pockets are real samples of the air from the time the snow fell.

Scientists drill long cylinders of this ice, called ice cores. The EPICA project drilled at Dome C in East Antarctica and recovered ice that is about 800,000 years old at the bottom. By measuring the gases inside the bubbles, researchers can see how much carbon dioxide and methane were in the air long before humans existed.

The ice also contains a temperature record. The ratio of different types of oxygen and hydrogen atoms in the ice changes depending on how cold it was when the snow formed. Put together, the cores show that carbon dioxide and temperature have risen and fallen together through many ice ages.

One of the most important results is that today's carbon dioxide level is far higher than anything found in the whole 800,000-year record. That is why ice cores are some of the strongest evidence we have for human-caused climate change.

Ice cores also catch dust, volcanic ash and even traces of past wildfires. A single core can tell a story of eruptions, droughts and changing winds stretching back across hundreds of thousands of years.""",
    ),
    (
        'Arctic Sea Ice Is Shrinking, and Why That Matters',
        'Oceans & Sea Ice', 'arctic', True,
        'Stroeve, J. & Notz, D. (2018). Changing state of Arctic sea ice across all seasons. Environmental Research Letters, 13.',
        'https://doi.org/10.1088/1748-9326/aade56',
        'Satellites have watched Arctic summer sea ice shrink for more than four decades.',
        """Sea ice is frozen ocean water. In the Arctic it grows through the dark winter and shrinks during the summer, reaching its smallest size every September.

Satellites have measured Arctic sea ice continuously since 1979. Since then the September minimum has been dropping by roughly 12 to 13 percent every decade. The ice has also become much thinner, because the old, thick ice that survived many summers has mostly been replaced by young, thin ice.

This matters because of something called albedo. Bright white ice reflects most of the sunlight that hits it back into space. Dark open ocean absorbs most of it. When ice melts, more ocean is exposed, the ocean absorbs more heat, and even more ice melts. Scientists call this the ice-albedo feedback.

Losing sea ice also affects wildlife and people. Polar bears use the ice as a platform to hunt seals. Walruses rest on it. Arctic communities use it for travel and hunting. Changes in the Arctic may even affect weather patterns further south.

Melting sea ice does not raise sea level much, because the ice was already floating in the water. The ice on land, on Greenland and Antarctica, is the big concern for sea level rise.""",
    ),
    (
        'How Emperor Penguins Survive the Antarctic Winter',
        'Polar Wildlife', 'antarctic', True,
        'Fretwell, P. T. et al. (2012). An emperor penguin population estimate: the first global, synoptic survey of a species from space. PLoS ONE, 7(4).',
        'https://doi.org/10.1371/journal.pone.0033751',
        'They breed in the coldest, darkest season on the coldest continent. Here is how they manage it.',
        """The emperor penguin is the tallest and heaviest of all penguins. Unlike almost every other animal, it chooses to breed during the Antarctic winter, when temperatures can drop below minus 40 degrees Celsius and strong winds blow across the sea ice.

After the female lays a single egg, she passes it carefully to the male and then heads out to sea to feed. The male balances the egg on top of his feet and covers it with a warm fold of skin called a brood pouch. He then stands and waits for about two months, through the darkest part of winter, without eating anything.

To survive, the males huddle together in large groups. The penguins slowly shuffle so that each bird takes turns in the warm centre and on the cold outside edge. Inside a tight huddle the temperature can be much warmer than the air around it.

Their bodies are also built for the cold. They have a thick layer of fat, several layers of tightly packed feathers, and a special blood flow system in their legs and flippers that keeps heat from escaping.

Emperor penguins depend on stable sea ice to raise their chicks. Scientists are watching their colonies closely, often using satellite images, because losing sea ice could put these birds at serious risk in the future.""",
    ),
    (
        'Polar Bears: Hunters of the Sea Ice',
        'Polar Wildlife', 'arctic', False,
        'Stirling, I. & Derocher, A. E. (2012). Effects of climate warming on polar bears: a review of the evidence. Global Change Biology, 18(9).',
        'https://doi.org/10.1111/j.1365-2486.2012.02753.x',
        'The polar bear is classified as a marine mammal because it spends so much of its life on sea ice.',
        """Polar bears live only in the Arctic. Although they are bears, scientists classify them as marine mammals, because they spend most of their lives on the frozen sea and depend on the ocean for their food.

Their main prey is seals. A polar bear will wait patiently next to a breathing hole in the ice, sometimes for hours, until a seal comes up for air. Without sea ice, polar bears have no platform to hunt from, so they are closely linked to the health of the ice.

A polar bear's fur is not actually white. Each hair is transparent and hollow, and it looks white because it scatters light. Underneath the fur, the bear's skin is black, which helps it absorb heat from the sun.

Polar bears are also strong swimmers and can cover long distances in the water. However, longer swims and longer ice-free seasons use up a lot of energy, which is a growing problem as the Arctic warms.""",
    ),
    (
        'India in Antarctica: From Dakshin Gangotri to Bharati',
        'Expeditions & Stations', 'antarctic', False,
        'National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences, Government of India.',
        'https://ncpor.res.in',
        'The story of India\'s research stations at both ends of the world.',
        """India sent its first scientific expedition to Antarctica in 1981. Just two years later, in 1983, India set up its first research station there, called Dakshin Gangotri. Over time it became buried in ice and was later used only as a supply base.

In 1989 India opened Maitri, a permanent station in the Schirmacher Oasis, an ice-free rocky area in East Antarctica. Maitri has supported research in geology, glaciology, atmospheric science and biology for more than three decades.

In 2012 India opened its newest Antarctic station, Bharati, in the Larsemann Hills. It is a modern building designed to save energy and is used for studies in oceanography, geology and the history of how India and Antarctica were once joined as part of the supercontinent Gondwana.

India also works in the Arctic. Himadri, India's Arctic research station, opened in 2008 at Ny-Ålesund in Svalbard, Norway.

All of this work is coordinated by the National Centre for Polar and Ocean Research (NCPOR) in Goa, which organises the yearly Indian Scientific Expeditions to Antarctica.""",
    ),
    (
        'The Science Behind the Northern and Southern Lights',
        'Aurora & Space Weather', 'both', False,
        'NOAA Space Weather Prediction Center. Aurora: Tutorial and background.',
        'https://www.swpc.noaa.gov/phenomena/aurora',
        'Auroras are a light show created when particles from the Sun meet Earth\'s magnetic field.',
        """The Sun is constantly sending out a stream of charged particles called the solar wind. When this stream reaches Earth, most of it is pushed away by our planet's magnetic field. But near the poles, the magnetic field lines guide some of these particles down into the upper atmosphere.

When the particles crash into gas atoms high above the ground, the atoms get extra energy and then release it as light. That glowing light is the aurora. In the north it is called the aurora borealis, or northern lights. In the south it is called the aurora australis, or southern lights.

The colours depend on which gas is hit and how high up it is. Oxygen produces the common green colour and, at greater heights, a deep red. Nitrogen can produce blue and purple shades along the lower edges.

Auroras are strongest during geomagnetic storms, which happen after big explosions on the Sun. The same storms can disturb satellites, GPS signals and power grids, which is why scientists study space weather carefully.""",
    ),
    (
        'Permafrost: The Frozen Ground That Stores Carbon',
        'Climate Change', 'arctic', False,
        'Schuur, E. A. G. et al. (2015). Climate change and the permafrost carbon feedback. Nature, 520.',
        'https://doi.org/10.1038/nature14338',
        'Huge areas of the Arctic sit on ground that has been frozen for thousands of years.',
        """Permafrost is ground that stays frozen for at least two years in a row. In parts of Siberia, Alaska and northern Canada it can be hundreds of metres deep and has been frozen since the last ice age.

Frozen inside the permafrost are the remains of plants and animals that never fully rotted. Scientists estimate that permafrost holds about twice as much carbon as is currently in the atmosphere.

When permafrost thaws, microbes wake up and start breaking down this old material. In the process they release carbon dioxide and methane, both greenhouse gases. This adds more warming, which thaws even more permafrost. It is another example of a climate feedback loop.

Thawing permafrost also causes problems on the surface. The ground can sink and collapse, damaging roads, buildings and pipelines in Arctic towns. Coastlines held together by frozen ground can erode quickly once it thaws.""",
    ),
    (
        'The Antarctic Ice Sheet and Rising Seas',
        'Glaciology & Ice Sheets', 'antarctic', False,
        'Fretwell, P. et al. (2013). Bedmap2: improved ice bed, surface and thickness datasets for Antarctica. The Cryosphere, 7.',
        'https://doi.org/10.5194/tc-7-375-2013',
        'Antarctica holds most of the world\'s ice. Even a small change there affects coastlines everywhere.',
        """The Antarctic ice sheet is the largest single mass of ice on Earth. On average it is about two kilometres thick, and in some places it is more than four kilometres deep. It holds around 90 percent of all the ice on the planet.

If all of it melted, global sea level would rise by roughly 58 metres. That is not going to happen any time soon, but even a small fraction of that amount would affect coastal cities around the world, including many in India.

West Antarctica is the area scientists are most worried about. Much of its ice sits on rock that is below sea level, which makes it easier for warm ocean water to melt it from underneath. Thwaites Glacier, sometimes nicknamed the Doomsday Glacier, is one of the most closely watched glaciers on Earth for this reason.

Scientists use satellites, aircraft radar, ocean robots and field camps to measure how much ice is being lost and how fast. These measurements help improve predictions of future sea level rise.""",
    ),
    (
        'Why the Poles Matter for the Whole Planet',
        'Climate Change', 'both', False,
        'Rantanen, M. et al. (2022). The Arctic has warmed nearly four times faster than the globe since 1979. Communications Earth & Environment, 3.',
        'https://doi.org/10.1038/s43247-022-00498-3',
        'What happens at the top and bottom of the world does not stay there.',
        """It is easy to think of the poles as distant places with little effect on our daily lives. In reality, they act like the planet's air conditioner.

The bright ice and snow reflect a large part of the sunlight that reaches them, which helps keep Earth cool. The cold, salty water that forms around Antarctica and in the North Atlantic sinks to the bottom of the ocean and drives a global system of currents that carries heat around the world.

The Arctic is warming much faster than the rest of the planet. Recent studies show it has warmed nearly four times faster than the global average since 1979. This fast change is known as Arctic amplification.

Melting land ice from Greenland and Antarctica raises sea levels for every coastline. Changes in the Arctic may also affect the jet stream and weather patterns in countries far to the south.

Studying the poles therefore helps us understand and prepare for the future of the entire planet, not just the frozen regions.""",
    ),
    (
        'A Day in the Life at a Polar Research Station',
        'Expeditions & Stations', 'both', False,
        'British Antarctic Survey. Life and work at Antarctic research stations.',
        'https://www.bas.ac.uk',
        'What do scientists actually do all day at the bottom of the world?',
        """Life at a polar research station is a mix of science, teamwork and survival. A typical day starts early with a team meeting to check the weather, because conditions decide which field work is safe.

Scientists might spend the day collecting snow and ice samples, launching weather balloons, checking instruments that measure the atmosphere, or counting penguins and seals. Back at the station, they process samples in the lab and send data home.

Everyone also helps with daily jobs like cooking, cleaning and melting snow for water. In summer the sun never sets, and in winter it may not rise for weeks. Staff have to manage their sleep, stay healthy and keep up good spirits in a small group.

Safety comes first. Teams train in first aid, firefighting and cold-weather survival, and nobody goes out onto the ice alone. Despite the challenges, many people describe working in the polar regions as the experience of a lifetime.""",
    ),
    (
        'The Antarctic Treaty: A Continent for Peace and Science',
        'Expeditions & Stations', 'antarctic', False,
        'Secretariat of the Antarctic Treaty. The Antarctic Treaty (1959) and the Protocol on Environmental Protection (1991).',
        'https://www.ats.aq',
        'How countries agreed to keep an entire continent free of war and open for research.',
        """On 1 December 1959, twelve countries signed the Antarctic Treaty in Washington. It came into force in 1961 and is one of the most successful international agreements ever made.

The treaty says that Antarctica can be used only for peaceful purposes. Military bases, weapons testing and nuclear explosions are not allowed, and nuclear waste cannot be dumped there. Scientists from any country are free to carry out research and are expected to share their results.

Several countries had claimed parts of Antarctica before 1959. The treaty does not cancel these claims, but it freezes them, so no new claims can be made and the old ones cannot be pushed further.

In 1991 the treaty members added the Madrid Protocol on environmental protection, which came into force in 1998. It calls Antarctica a natural reserve devoted to peace and science and bans mining.

Today more than 50 countries have joined the treaty. India joined in 1983, and in 2022 passed the Indian Antarctic Act to make sure its activities follow these rules.""",
    ),
    (
        'Midnight Sun and Polar Night: Why Days Get So Strange',
        'Aurora & Space Weather', 'both', False,
        'NASA Space Place. What causes the seasons?',
        'https://spaceplace.nasa.gov/seasons/',
        'Near the poles the Sun can stay up for weeks, or disappear for weeks. Earth\'s tilt explains why.',
        """Earth's axis is tilted by about 23.5 degrees. As Earth goes around the Sun, first one pole and then the other leans towards the Sun.

When the North Pole leans towards the Sun, the Arctic gets the midnight sun: the Sun stays above the horizon all day and all night. At the same time, the Antarctic is in polar night, with the Sun staying below the horizon. Six months later, the situation flips.

The Arctic and Antarctic Circles, at about 66.5 degrees latitude, mark where this begins. Anywhere inside these circles has at least one full day of midnight sun in summer and one full day of polar night in winter. The closer you go to the pole, the longer these periods last. At the poles themselves there are roughly six months of daylight followed by six months of darkness.

These extreme light conditions shape life in the polar regions. Plants and animals squeeze their growing and breeding into the short bright summer. People at research stations have to adjust their sleep and routine, and the long polar night is the best time to watch the aurora.""",
    ),
    (
        'Krill: The Tiny Animal That Feeds Antarctica',
        'Polar Wildlife', 'antarctic', False,
        'Atkinson, A. et al. (2004). Long-term decline in krill stock and increase in salps within the Southern Ocean. Nature, 432.',
        'https://doi.org/10.1038/nature02996',
        'A shrimp-like creature only a few centimetres long holds up the whole Antarctic food web.',
        """Antarctic krill are small, shrimp-like animals that grow to about six centimetres long. On their own they look unimportant, but together they are one of the most abundant animals on the planet, with a total mass estimated at hundreds of millions of tonnes.

Krill feed on tiny plant-like organisms called phytoplankton, including algae that grow on the underside of sea ice. In winter, the sea ice acts like a nursery and feeding ground for young krill.

Almost everything in the Southern Ocean depends on krill. Whales, seals, penguins, fish and seabirds all eat them. Large whales such as the blue whale can eat several tonnes of krill in a single day during the feeding season.

Krill also help the climate. They eat carbon-rich algae near the surface, and their waste sinks to the deep ocean, carrying that carbon with it.

Because krill depend on sea ice and cold water, scientists worry about how warming will affect them. Krill fishing is managed by an international body called CCAMLR to make sure enough krill are left for the animals that need them.""",
    ),
    (
        'Icebergs, Ice Shelves and Calving',
        'Glaciology & Ice Sheets', 'both', False,
        'Scambos, T. A. et al. (2004). Glacier acceleration and thinning after ice shelf collapse in the Larsen B embayment, Antarctica. Geophysical Research Letters, 31.',
        'https://doi.org/10.1029/2004GL020670',
        'Where do icebergs come from, and why do scientists care when ice shelves break apart?',
        """Glaciers and ice sheets are always moving slowly downhill, like very thick rivers of ice. In Antarctica, many of them flow out onto the ocean and form ice shelves: huge floating platforms of ice that can be hundreds of metres thick.

At the edge of a glacier or ice shelf, pieces of ice break off and fall into the sea. This is called calving, and the floating pieces are icebergs. Because ice is only a little less dense than sea water, about 90 percent of an iceberg sits below the surface.

Some icebergs are enormous. In 2017 an iceberg called A68 broke away from the Larsen C Ice Shelf with an area of about 5,800 square kilometres, several times larger than the city of Delhi.

Calving is a natural process, but scientists watch ice shelves carefully. In 2002 the Larsen B Ice Shelf broke up in just a few weeks. Ice shelves act like a cork in a bottle, holding back the glaciers behind them. When an ice shelf disappears, those glaciers can speed up and push more land ice into the ocean, which raises sea level.""",
    ),
]


# (title, type, region, description, link)
MEDIA = [
    ('Satellite Views of Polar Ice', 'photo', 'both',
     'Stunning satellite images of glaciers, sea ice and ice shelves from NASA Earth Observatory. Great for presentations and posters.',
     'https://earthobservatory.nasa.gov'),
    ('Sea Ice Data and Daily Updates', 'document', 'arctic',
     'The National Snow and Ice Data Center publishes daily sea ice charts and easy-to-read monthly analysis.',
     'https://nsidc.org'),
    ('Arctic Report Card', 'document', 'arctic',
     'NOAA\'s yearly peer-reviewed report on the state of the Arctic, with clear graphics on temperature, ice and wildlife.',
     'https://arctic.noaa.gov'),
    ('Indian Antarctic Programme', 'document', 'antarctic',
     'Information on Indian research stations Maitri, Bharati and Himadri, and the yearly expeditions, from NCPOR Goa.',
     'https://ncpor.res.in'),
    ('Life on an Antarctic Research Station', 'video', 'antarctic',
     'Videos and stories from British Antarctic Survey scientists about research, wildlife and daily life on the ice.',
     'https://www.bas.ac.uk'),
    ('Aurora Photos from Space', 'photo', 'both',
     'NASA\'s image library has photos of the aurora taken by astronauts on the International Space Station. Search "aurora" for hundreds of images.',
     'https://images.nasa.gov/search?q=aurora'),
    ('NASA\'s Curious Universe', 'podcast', 'both',
     'NASA\'s official podcast about missions, discoveries and the scientists behind them, in space and here on Earth.',
     'https://www.nasa.gov/podcasts/curious-universe/'),
    ('Climate Change Explained Simply', 'video', 'both',
     'Clear explanations and visuals on climate change and its effect on the poles, from NASA\'s climate science team.',
     'https://science.nasa.gov/climate-change/'),
    ('The Antarctic Treaty Documents', 'document', 'antarctic',
     'The full text of the Antarctic Treaty and the Madrid Protocol, published by the Antarctic Treaty Secretariat.',
     'https://www.ats.aq'),
    ('Sea Ice Animations from Satellite Data', 'video', 'both',
     'NASA\'s Scientific Visualization Studio turns satellite measurements into animations showing how polar sea ice grows, shrinks and changes over the years.',
     'https://svs.gsfc.nasa.gov'),
    ('The NOAA Ocean Podcast', 'podcast', 'both',
     'NOAA experts talk about ocean science in short, easy episodes, a good companion to our Oceans & Sea Ice articles.',
     'https://oceanservice.noaa.gov/podcast/'),
    ('Live Aurora Forecast Map', 'photo', 'both',
     'NOAA\'s 30-minute aurora forecast shows where the northern and southern lights may be visible right now.',
     'https://www.swpc.noaa.gov/products/aurora-30-minute-forecast'),
]


# (title, days from today, location, online?, description)
EVENTS = [
    ('Webinar: Life of an Antarctic Expedition Member', 7, 'Online (Zoom)', True,
     'A live session with a member of the Indian Scientific Expedition to Antarctica. Learn how expeditions are planned and what life is like at Maitri station. Q&A at the end.'),
    ('Ice Core Workshop for School Students', 18, 'Science Centre, Pune', False,
     'A hands-on workshop where students build their own "ice cores" with coloured layers and learn how scientists read climate history from ice.'),
    ('Polar Photography Exhibition', 30, 'City Art Gallery, Bengaluru', False,
     'An exhibition of photographs from the Arctic and Antarctic taken by researchers in the field. Entry is free for students.'),
    ('Panel Talk: Melting Ice and Rising Seas', 45, 'Online (YouTube Live)', True,
     'Glaciologists and ocean scientists discuss how polar ice loss affects coastlines, with a special focus on India\'s coastal cities.'),
    ('Aurora Night: Science of the Northern Lights', -20, 'Planetarium, Mumbai', False,
     'An evening show explaining how auroras form, followed by a full-dome aurora display.'),
    ('Teachers\' Training on Polar Science', -50, 'Online (Google Meet)', True,
     'A training session for school teachers on using polar science examples to teach climate, geography and biology.'),
]


class Command(BaseCommand):
    help = 'Adds sample categories, articles, media and events to the database'

    def handle(self, *args, **options):
        # media and events have no links pointing to them, so we can just start fresh
        MediaItem.objects.all().delete()
        Event.objects.all().delete()

        now = timezone.now()

        # categories
        # update_or_create: if a category with this name exists, update it, otherwise create it
        categories = {}
        for name, icon, description in CATEGORIES:
            category, created = Category.objects.update_or_create(
                name=name,
                defaults={'icon': icon, 'description': description},
            )
            categories[name] = category

        # articles - found by title, so their ID (and web address) stays the same
        for i, (title, cat, region, featured, source, source_url, summary, content) in enumerate(ARTICLES):
            Article.objects.update_or_create(
                title=title,
                defaults={
                    'category': categories[cat],
                    'region': region,
                    'icon': ARTICLE_ICONS.get(title, ''),
                    'author': AUTHOR,
                    'is_featured': featured,
                    'is_approved': True,
                    'source': source,
                    'source_url': source_url,
                    'summary': summary,
                    'content': content,
                    'views': 0,
                    # each one is dated a few days apart so the order looks natural
                    'created_at': now - timedelta(days=i * 4),
                },
            )

        # media
        for i, (title, media_type, region, description, link) in enumerate(MEDIA):
            MediaItem.objects.create(
                title=title,
                media_type=media_type,
                region=region,
                description=description,
                link=link,
                created_at=now - timedelta(days=i * 3),
            )

        # events - dates are relative to today so there are always upcoming ones
        for title, days, location, online, description in EVENTS:
            event_date = (now + timedelta(days=days)).replace(hour=17, minute=0, second=0, microsecond=0)
            Event.objects.create(
                title=title,
                date=event_date,
                location=location,
                is_online=online,
                description=description,
            )

        # demo user so the login features can be shown straight away
        demo, created = User.objects.get_or_create(username='demo')
        demo.set_password('demo@123')
        demo.save()

        # give the demo user 3 bookmarks (remove old ones first so we start clean)
        Bookmark.objects.filter(user=demo).delete()
        for article in Article.objects.filter(is_featured=True):
            Bookmark.objects.create(user=demo, article=article)

        # one approved article and one waiting for review, written by the demo user
        Article.objects.update_or_create(
            title='My Visit to a Polar Science Exhibition',
            defaults={
                'category': categories['Expeditions & Stations'],
                'region': 'both',
                'author': 'demo',
                'submitted_by': demo,
                'is_approved': True,
                'views': 0,
                'summary': 'What I learned about ice cores and research stations at a student science exhibition.',
                'content': """Last month our class visited a science exhibition on the polar regions. The first thing we saw was a model of an ice core showing coloured layers, one for every year of snowfall.

A volunteer explained how scientists read past climate from tiny air bubbles trapped in the ice. We also saw photos of India's Maitri and Bharati stations in Antarctica.

The most surprising fact for me was that Antarctica holds about 90 percent of all the ice on Earth. After the visit, I started reading more about polar science, which is why I am sharing this with PolarPortal.""",
            },
        )
        Article.objects.update_or_create(
            title='Why Seals Can Hold Their Breath for So Long',
            defaults={
                'category': categories['Polar Wildlife'],
                'region': 'antarctic',
                'icon': ARTICLE_ICONS.get('Why Seals Can Hold Their Breath for So Long', ''),
                'author': 'demo',
                'submitted_by': demo,
                'is_approved': False,  # stays "pending" so the admin approval can be shown in the demo
                'views': 0,
                'summary': 'A short look at how Weddell seals dive deep under the Antarctic sea ice.',
                'content': """Weddell seals live further south than any other mammal and spend much of their lives under the sea ice.

They can dive for a long time because their blood and muscles store a lot of oxygen, and their heart slows down during a dive to save energy.""",
            },
        )

        self.stdout.write(self.style.SUCCESS(
            f'Done! Added {len(CATEGORIES)} categories, {len(ARTICLES)} articles, '
            f'{len(MEDIA)} media items and {len(EVENTS)} events.'
        ))
        self.stdout.write(self.style.SUCCESS('Demo login -> username: demo   password: demo@123'))
