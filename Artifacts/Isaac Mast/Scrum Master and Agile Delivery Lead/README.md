For Project 5, my work was split in the beginning and once planning was complete.

I was heavily involved in the planning process, developing user stories and the release plan.
After planning was complete and development had begun, I spent a large chunk of time getting our server hosted
by Python Anywhere, setting up the PSQL db that is hosted on Python Anywhere, and figuring out how to configure
our django project settings for both the Python Anywhere server and for developers on their local machines. This
requires an ssh tunnel to the database hosted by Python Anywhere with the django database settings configured to
connect to the ssh tunnel. This way, the team has access to the database during development, we can create
various versions of the database for development, testing, and production, and our database is on a persistent
connection and backed up.

As the scrum master, I did my best to lead the team during meetings, come with an agenda, and be sure to address
the things that were required. I was also active and communicative in our group messaging chat, and tried to be
in discussion about issues that were arising, and help with any technological difficulties.

I filled out the critical issue for the scrum master, but I took on the role of developing a system for
persistent storage. Our system was not set up initially, so I also worked to refactor our django project to
follow standards for static file storage and the configuration with our PSQL server for development.
