from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, App, User

engine = create_engine('sqlite:///vrappswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy users
User1 = User(name="Harry Potter", email="harrypotter@hogwarts.edu",
             picture='https://pbs.twimg.com/profile_images/3390207485/a169862f7b3035075e98a5de57577249.png')
session.add(User1)
session.commit()

User2 = User(name="Draco Malfoy", email="dracomalfoy@hogwarts.edu",
             picture='https://pbs.twimg.com/profile_images/591624878102478849/sDoRs12L.png')
session.add(User2)
session.commit()

User3 = User(name="Hermione Granger", email="hermionegranger@hogwarts.edu",
             picture='https://pbs.twimg.com/profile_images/609088797637271552/1VFeG1bV_400x400.jpg')
session.add(User3)
session.commit()

User4 = User(name="Ron Weasley", email="ronweasley@hogwarts.edu",
             picture='https://pbs.twimg.com/profile_images/3461048434/5ff5ba8c9276ea4ab0428846195ebe9f.jpeg')
session.add(User4)
session.commit()


# Apps for Virtual Trip
category1 = Category(name="Virtual Tour")

session.add(category1)
session.commit()

app1 = App(user_id=1, name="Crystal Habit", developer = "Julius Horsthuis", description="The latest VR Fractal from Julius Horsthuis. An Illuminating VR-trip.", price="Free", website ="http://www.julius-horsthuis.com/", category=category1)

session.add(app1)
session.commit()

app2 = App(user_id=4, name="Lexus Virtual Drive", developer = "Hammerhead VR", description="Experience the brutal elegance of the Lexus in a virtual reality race at Spain's spectacular Ascari track.", price="Free", website ="http://www.hammerheadvr.com/", category=category1)

session.add(app2)
session.commit()

app3 = App(user_id=2, name="Deep Sea", developer = "Antonio Peres", description="Who needs to go Scuba Diving when you've got VR? DIve into the Deep Blue and experience Whales, Sharks, Stingrays and other frightening sea creatures.", price="Free", website ="https://antonioperes3d.wordpress.com/2009/08/12/destaque/", category=category1)

session.add(app3)
session.commit()


# Apps for Interactive Story
category2 = Category(name = "Interactive Story")

session.add(category2)
session.commit()


app1 = App(user_id=2, name="Rexodus VR", developer = "Steelehouse Productions", description = "Rexodus VR is based on the Dark Horse Graphic Novel, Rexodus. Dinosaurs in space with guns VR style!", price = "Free", website = "http://steelehouse.com/", category = category2)

session.add(app1)
session.commit()

app2 = App(user_id = 1, name = "SONAR", developer = "Phillipp Maas", description="Explore your surroundings and dive deep into an ancient cave system. Follow the drone ship and discover the horrific truth about the darkest of all places...", price = "Unknown", category = category2)

session.add(app2)
session.commit()


# Apps for Education

category3 = Category(name = "Education")

session.add(category3)
session.commit()

app1 = App(user_id=3, name="Intro to Gastric Sleeve Surgery - Episode I", developer = "VRTL", description="The first episode in a lecture series on Gastric Sleeve surgery with world renown Bariatric Surgeon, Dr. Ariel Ortiz.", price="Free", website ="http://www.vrtul-edu.com/home", category=category3)

session.add(app1)
session.commit()


# Apps for Simulation!

category4 = Category(name = "Simulation")

session.add(category4)
session.commit()

app1 = App(user_id=4, name="Flying Aces VR", developer = "Ben Librojo", description="Flying Aces VR is a flight sim/combat game set during World War 1. Take to the skies and experience the birth and rise of aerial combat during the Great War (1914-1918). Develop and test your piloting, gunning and bombing skills in structured missions, and lead your side to victory from above!", price="Free", website ="http://www.vr-gameplay.com/", category=category4)

session.add(app1)
session.commit()


# Apps for games!

category5 = Category(name = "Game")

session.add(category5)
session.commit()

app1 = App(user_id=4, name="Casino VR: Poker (Beta)", developer = "Casino VR Ltd.", description="Casino VR: Poker (Beta) is a free multiplayer poker game with realistic avatars, body movement and spatial voice chat. The game is currently running as a Beta. See your avatar come to life as the game mirrors your real life head movements in VR, hear people smack talk as they try to bluff each other to win the game.", price="Free", website ="http://www.casino-vr.com/", category=category5)


session.add(app1)
session.commit()

app2 = App(user_id = 3, name = "InCell", developer = "Nival VR", 
	description="InCell is a non-trivial combination of pipe styled racing and exploration strategy genres in highly unusual micro world of the carefully recreated human cell.", price = "Unknown", website = "http://incell.nivalvr.com/", category = category5)

session.add(app2)
session.commit()

app3 = App(user_id=2, name = "Pinball Labs", developer = "Thomas Kadlec", website = "http://pinballlabs.com/", description="Recreating the Physics, Visuals and Fun of Real World Pinball.", price = "Unknown", category = category5)

session.add(app3)
session.commit()

print "VR Apps added! "