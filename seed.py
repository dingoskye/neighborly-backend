from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import User, Post, Comment, Event, AttendeeAgeGroup
from datetime import datetime

def seed_db():
    # Remove the existing database file to ensure a fresh seed
    import os
    if os.path.exists("database.db"):
        os.remove("database.db")

    create_db_and_tables()
    with Session(engine) as session:
        # Users (implied from mock data)
        users = [
            User(id="user-1", name="Jarmo Lindman", avatar="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face", neighborhood="Keskusta", bio="Love meeting new people and exploring local events! 🌟", joinedDate="2024-01-15"),
            User(id="user-2", name="Ilse Nikula", avatar="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face", neighborhood="Keskusta", bio="Gardening enthusiast", joinedDate="2023-05-10"),
            User(id="user-5", name="Peter Saarinen", avatar="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face", neighborhood="Oak Street", bio="Dog lover", joinedDate="2023-08-20"),
            User(id="user-7", name="Hannah Virtanen", avatar="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&h=150&fit=crop&crop=face", neighborhood="Main Street", bio="Coffee shop owner", joinedDate="2010-01-01"),
            User(id="user-10", name="Jasmin Hyvönen", avatar="https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=150&h=150&fit=crop&crop=face", neighborhood="Harbor", bio="Yoga Instructor", joinedDate="2022-03-15"),
            User(id="user-11", name="Eliisa Tuulola", avatar="https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=150&h=150&fit=crop&crop=face", neighborhood="Art District", bio="Artist", joinedDate="2022-06-01"),
            User(id="user-12", name="Nelma Numminen", avatar="https://images.unsplash.com/photo-1554151228-14d9def656e4?w=150&h=150&fit=crop&crop=face", neighborhood="Library", bio="Bookworm", joinedDate="2023-11-11"),
            User(id="user-13", name="Joonas Eskelinen", avatar="https://images.unsplash.com/photo-1738762389087-35bcc2b03b2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", neighborhood="City Center", bio="Event organizer", joinedDate="2024-01-01")
        ]
        for user in users:
            session.add(user)

        # Posts
        posts_data = [
            {
                "id": "post-1",
                "title": "Community Garden Opening This Weekend! 🌻",
                "subtitle": "Join us for the grand opening of our new community garden space",
                "content": "We're thrilled to announce the grand opening of our neighborhood community garden! \n\nAfter months of planning and hard work from dedicated volunteers, we're finally ready to welcome everyone to this beautiful green space.\n\n**What to expect:**\n- Free seedlings for the first 50 visitors\n- Gardening workshops throughout the day\n- Live music from local artists\n- Refreshments and snacks\n- Kids' corner with fun activities\n\nThe garden will be open from 10 AM to 4 PM. Bring your family, friends, and neighbors!\n\nThis is a wonderful opportunity to meet fellow gardening enthusiasts and learn from experienced growers in our community.\n\nSee you there! 🌱",
                "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=400&fit=crop",
                "authorId": "user-2",
                "authorName": "Ilse Nikula",
                "authorAvatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "createdAt": "2026-01-20T10:30:00Z",
                "likes": 47,
                "comments": [
                    {"id": "comment-1", "userId": "user-3", "userName": "Jaska Ukkonen", "userAvatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face", "content": "This is amazing! Can't wait to attend with my kids!", "createdAt": "2026-01-20T11:15:00Z"},
                    {"id": "comment-2", "userId": "user-4", "userName": "Pauliina Ahokas", "userAvatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=face", "content": "Finally! I've been waiting for a community garden in our area 🌸", "createdAt": "2026-01-20T12:00:00Z"}
                ]
            },
            {
                "id": "post-2",
                "title": "Lost Dog Found Near Oak Street Park",
                "subtitle": "Golden Retriever found this morning - looking for owner",
                "content": "Found this friendly golden retriever wandering near Oak Street Park around 8 AM this morning. \n\n**Description:**\n- Golden Retriever, appears to be around 3-4 years old\n- Wearing a blue collar but no tags\n- Very friendly and well-trained\n- Responds to basic commands\n\nThe dog is currently safe at my house with food and water. If this is your dog or you know who the owner might be, please contact me through the comments or reach out to the neighborhood association.\n\nLet's help this pup get back home! 🐕",
                "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800&h=400&fit=crop",
                "authorId": "user-5",
                "authorName": "Peter Saarinen",
                "authorAvatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
                "createdAt": "2026-01-19T08:45:00Z",
                "likes": 23,
                "comments": [
                    {"id": "comment-3", "userId": "user-6", "userName": "Jonna Koskela", "userAvatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face", "content": "Shared this with our walking group! Hope the owner is found soon.", "createdAt": "2026-01-19T09:30:00Z"}
                ]
            },
            {
                "id": "post-3",
                "title": "New Coffee Shop Opening on Main Street ☕",
                "subtitle": "Local entrepreneur brings artisan coffee to our neighborhood",
                "content": "Exciting news for coffee lovers! A new artisan coffee shop called \"Neighborhood Brew\" is opening next week on Main Street.\n\nThe owner, Hannah Virtanen, has been a resident of our neighborhood for over 15 years and is finally pursuing her dream of opening a local coffee spot.\n\n**What's special:**\n- Locally roasted beans from small farms\n- Cozy reading corner with community book exchange\n- Free WiFi and plenty of outlets for remote workers\n- Pastries baked fresh daily\n\nThey're offering 20% off all drinks during opening week! Stop by and show some support for our local businesses.\n\nLocation: 123 Main Street (next to the bookstore)\nOpening Day: January 25th",
                "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=400&fit=crop",
                "authorId": "user-7",
                "authorName": "Hannah Virtanen",
                "authorAvatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&h=150&fit=crop&crop=face",
                "createdAt": "2026-01-18T14:20:00Z",
                "likes": 89,
                "comments": [
                    {"id": "comment-4", "userId": "user-8", "userName": "Arvid Lehtonen", "userAvatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&h=150&fit=crop&crop=face", "content": "Yes!! We need more local coffee shops. Can't wait to try it!", "createdAt": "2026-01-18T15:00:00Z"},
                    {"id": "comment-5", "userId": "user-9", "userName": "Nina Koskela", "userAvatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face", "content": "The book exchange idea is brilliant! Count me in as a regular.", "createdAt": "2026-01-18T16:30:00Z"},
                    {"id": "comment-6", "userId": "user-1", "userName": "Jarmo Lindman", "userAvatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face", "content": "Congratulations Hannah! This is wonderful for the community.", "createdAt": "2026-01-18T17:45:00Z"}
                ]
            }
        ]

        for p_data in posts_data:
            post = Post(
                id=p_data["id"],
                title=p_data["title"],
                subtitle=p_data["subtitle"],
                content=p_data["content"],
                image=p_data["image"],
                authorId=p_data["authorId"],
                authorName=p_data["authorName"],
                authorAvatar=p_data["authorAvatar"],
                createdAt=datetime.strptime(p_data["createdAt"], "%Y-%m-%dT%H:%M:%SZ"),
                likes=p_data["likes"]
            )
            session.add(post)
            # Comments
            for c_data in p_data["comments"]:
                comment = Comment(
                    id=c_data["id"],
                    userId=c_data["userId"],
                    userName=c_data["userName"],
                    userAvatar=c_data["userAvatar"],
                    content=c_data["content"],
                    post_id=post.id,
                    createdAt=datetime.strptime(c_data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
                )
                session.add(comment)

        # Events
        events_data = [
            {
                "id": "event-1",
                "title": "Saturday Morning Yoga at Lahti Harbor",
                "description": "Start your weekend with a relaxing outdoor yoga session by the beautiful Lahti Harbor!\n\nAll skill levels welcome - from complete beginners to experienced yogis. Our certified instructor, Jasmin, will guide you through a gentle flow perfect for connecting with nature and your neighbors.\n\n**What to bring:**\n- Yoga mat (we have extras if you don't have one)\n- Water bottle\n- Comfortable clothing\n- Positive vibes!\n\nThe session lasts about 1 hour, followed by optional tea and light snacks where you can mingle with fellow participants.",
                "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=400&fit=crop",
                "date": "2024-01-27",
                "time": "08:00",
                "location": {"name": "Lahti Harbor Park", "address": "Satamakatu, 15140 Lahti", "lat": 60.9827, "lng": 25.6612},
                "organizerId": "user-10",
                "organizerName": "Jasmin Hyvönen",
                "organizerAvatar": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=150&h=150&fit=crop&crop=face",
                "category": "Wellness",
                "attendees": {"count": 18, "ageGroups": [{"range": "18-25", "count": 4}, {"range": "26-35", "count": 8}, {"range": "36-50", "count": 5}, {"range": "50+", "count": 1}]},
                "isJoined": False,
                "isPast": False
            },
            {
                "id": "event-2",
                "title": "Neighborhood Potluck Dinner",
                "description": "Bring your favorite dish and meet your neighbors at our monthly potluck dinner!\n\nThis is a wonderful opportunity to share recipes, stories, and make new friends. Whether you're new to the neighborhood or have lived here for decades, everyone is welcome.\n\n**Theme: Comfort Food from Around the World**\n\nShare a dish that represents your heritage or simply brings you comfort. Don't forget to bring the recipe to share!\n\nTables, chairs, and drinks will be provided. Just bring your dish and an appetite for good food and great conversation.",
                "image": "https://plus.unsplash.com/premium_photo-1673108852141-e8c3c22a4a22?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "date": "2026-01-28",
                "time": "18:30",
                "location": {"name": "Lahti Community Center", "address": "Kirkkokatu 5, 15140 Lahti", "lat": 60.9850, "lng": 25.6550},
                "organizerId": "user-2",
                "organizerName": "Ilse Nikula",
                "organizerAvatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "category": "Social",
                "attendees": {"count": 34, "ageGroups": [{"range": "18-25", "count": 6}, {"range": "26-35", "count": 12}, {"range": "36-50", "count": 10}, {"range": "50+", "count": 6}]},
                "isJoined": True,
                "isPast": False
            },
            {
                "id": "event-3",
                "title": "Kids Art Workshop",
                "description": "A fun and creative afternoon for kids aged 5-12!\n\nJoin local artist Eliisa for a hands-on art workshop where children will create their own masterpieces using various materials including paint, clay, and recycled materials.\n\n**This month's theme: \"My Neighborhood\"**\n\nKids will create artwork inspired by our community - from favorite spots to friendly neighbors.\n\nAll materials provided. Light snacks included. Parents are welcome to stay and watch or enjoy some free time while their kids create!",
                "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&h=400&fit=crop",
                "date": "2026-01-29",
                "time": "14:00",
                "location": {"name": "Lahti Art Museum", "address": "Vesijärvenkatu 11, 15140 Lahti", "lat": 60.9810, "lng": 25.6580},
                "organizerId": "user-11",
                "organizerName": "Eliisa Tuulola",
                "organizerAvatar": "https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=150&h=150&fit=crop&crop=face",
                "category": "Kids",
                "attendees": {"count": 12, "ageGroups": [{"range": "5-8", "count": 7}, {"range": "9-12", "count": 5}]},
                "isJoined": False,
                "isPast": False
            },
            {
                "id": "event-4",
                "title": "Book Club: January Meeting",
                "description": "Join us for this month's book club discussion!\n\n**This month's book: \"The House in the Cerulean Sea\" by TJ Klune**\n\nA heartwarming fantasy about found family, acceptance, and the magic of community. Perfect for our neighborhood book club!\n\nWhether you've finished the book or are still reading, come share your thoughts and enjoy lively discussion with fellow book lovers.\n\nTea, coffee, and homemade cookies provided by our generous host, Nelma.",
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=400&fit=crop",
                "date": "2026-01-30",
                "time": "19:00",
                "location": {"name": "Lahti City Library", "address": "Kirkkokatu 31, 15140 Lahti", "lat": 60.9840, "lng": 25.6630},
                "organizerId": "user-12",
                "organizerName": "Nelma Numminen",
                "organizerAvatar": "https://images.unsplash.com/photo-1554151228-14d9def656e4?w=150&h=150&fit=crop&crop=face",
                "category": "Culture",
                "attendees": {"count": 8, "ageGroups": [{"range": "26-35", "count": 3}, {"range": "36-50", "count": 3}, {"range": "50+", "count": 2}]},
                "isJoined": True,
                "isPast": False
            },
            {
                "id": "event-5",
                "title": "Holiday Cookie Exchange",
                "description": "Our annual holiday cookie exchange was a huge success! Thank you to everyone who participated and brought their delicious homemade cookies.\n\nWe had over 30 different varieties of cookies from family recipes spanning multiple generations and cultures. What a treat to sample them all!\n\nSpecial thanks to the Community Center for hosting and to all the volunteers who helped set up.",
                "image": "https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=800&h=400&fit=crop",
                "date": "2025-12-15",
                "time": "15:00",
                "location": {"name": "Sibelius Hall", "address": "Ankkurikatu 7, 15140 Lahti", "lat": 60.9790, "lng": 25.6670},
                "organizerId": "user-2",
                "organizerName": "Ilse Nikula",
                "organizerAvatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "category": "Social",
                "attendees": {"count": 45, "ageGroups": [{"range": "18-25", "count": 8}, {"range": "26-35", "count": 15}, {"range": "36-50", "count": 14}, {"range": "50+", "count": 8}]},
                "isJoined": True,
                "isPast": True
            },
            {
                "id": "event-6",
                "title": " Laser Tag Night at Megazone",
                "description": " Our laser tag outing at Megazone in Lahti was an absolute hit! Thank you to everyone who joined and brought so much energy and team spirit to the arena.\nWe had intense matches, lots of laughs, and some seriously impressive moves from both new players and seasoned pros. It was awesome to see everyone getting into the game and cheering each other on.\nSpecial thanks to the Megazone Lahti staff for hosting us and keeping everything running smoothly. We’re already looking forward to the next battle!",
                "image": " https://megazone.fi/wp-content/uploads/2018/05/megazone-kuvagalleria-pelihalli-helsinki-012-1024x682.jpg",
                "date": "2026-01-20",
                "time": "18:00",
                "location": {"name": "Megazone Lahti", "address": "Kauppakatu 23, 15140 Lahti", "lat": 60.98894108488988, "lng": 25.666386499999998},
                "organizerId": "user-13",
                "organizerName": "Joonas Eskelinen",
                "organizerAvatar": "https://images.unsplash.com/photo-1738762389087-35bcc2b03b2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "category": "Social",
                "attendees": {"count": 42, "ageGroups": [{"range": "18-25", "count": 16}, {"range": "26-35", "count": 13}, {"range": "36-50", "count": 9}, {"range": "50+", "count": 4}]},
                "isJoined": True,
                "isPast": True
            },
            {
                "id": "event-7",
                "title": " Relax & Recharge at Mukkula Manor’s Lakeside Sauna",
                "description": " We’re excited to invite you to an upcoming wellness evening at the beautiful Mukkula Manor Lakeside Sauna! Join us for a relaxing escape by the water, where warmth, calm, and good company come together.\nExpect a cozy sauna experience, refreshing dips in the lake, and plenty of time to unwind and connect with others in a peaceful setting. Whether you’re a sauna regular or trying it for the first time, this will be the perfect chance to slow down and recharge.\nWe can’t wait to share this tranquil evening with you!",
                "image": " https://visitlahti.fi/wp-content/uploads/2020/09/Mukkulan-kartano-rantasauna-540x360.jpg",
                "date": "2026-01-25",
                "time": "18:00",
                "location": {"name": " Mukkula Manor’s Lakeside Sauna ", "address": " Niemenkatu 30, Ritaniemenkatu 10, 15240 Lahti ", "lat": 61.01516817831573, "lng": 25.641480671164157},
                "organizerId": "user-13",
                "organizerName": "Joonas Eskelinen",
                "organizerAvatar": "https://images.unsplash.com/photo-1738762389087-35bcc2b03b2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "category": "Social",
                "attendees": {"count": 38, "ageGroups": [{"range": "18-25", "count": 4}, {"range": "26-35", "count": 5}, {"range": "36-50", "count": 13}, {"range": "50+", "count": 16}]},
                "isJoined": False,
                "isPast": False
            },
            {
                "id": "event-8",
                "title": " Discover Art & Design at the Malva Museum, Lahti",
                "description": "We’re excited to announce an upcoming cultural outing to the Malva Museum in Lahti! Join us for an inspiring visit filled with art, design, and creative exploration in one of the city’s most vibrant cultural spaces.\nWe’ll spend time discovering unique exhibitions, sharing impressions, and enjoying the atmosphere together. Whether you’re a big art lover or just curious to explore something new, this will be a great chance to get inspired and connect.\nMore details coming soon — we can’t wait to experience Malva with you!\n",
                "image": " https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/5f/55/01/lahti-international-poster.jpg?w=1200&h=-1&s=1",
                "date": "2026-02-15",
                "time": "14:00",
                "location": {"name": " Lahti Museum of Visual Arts Malva", "address": " Päijänteenkatu 9 B 1, 15140 Lahti", "lat": 60.98612871368887, "lng": 25.659201819542506},
                "organizerId": "user-13",
                "organizerName": "Joonas Eskelinen",
                "organizerAvatar": "https://images.unsplash.com/photo-1738762389087-35bcc2b03b2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "category": "Social",
                "attendees": {"count": 48, "ageGroups": [{"range": "18-25", "count": 8}, {"range": "26-35", "count": 11}, {"range": "36-50", "count": 13}, {"range": "50+", "count": 16}]},
                "isJoined": True,
                "isPast": False
            }
        ]

        for e_data in events_data:
            event = Event(
                id=e_data["id"],
                title=e_data["title"],
                description=e_data["description"],
                image=e_data["image"],
                date=e_data["date"],
                time=e_data["time"],
                locationName=e_data["location"]["name"],
                locationAddress=e_data["location"]["address"],
                lat=e_data["location"]["lat"],
                lng=e_data["location"]["lng"],
                organizerId=e_data["organizerId"],
                organizerName=e_data["organizerName"],
                organizerAvatar=e_data["organizerAvatar"],
                category=e_data["category"],
                attendeeCount=e_data["attendees"]["count"],
                isJoined=e_data["isJoined"],
                isPast=e_data["isPast"]
            )
            session.add(event)
            
            # Age Groups
            if "ageGroups" in e_data["attendees"]:
                for ag_data in e_data["attendees"]["ageGroups"]:
                    age_group = AttendeeAgeGroup(
                        range=ag_data["range"],
                        count=ag_data["count"],
                        event_id=event.id
                    )
                    session.add(age_group)

        session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
