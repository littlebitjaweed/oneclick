import random
import urllib.request
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from app.models import Event, AvailableDate  # Replace with your actual app name

fake = Faker()

CATEGORY_CHOICES = [c[0] for c in Event.CATEGORY_CHOICES]
CITY_CHOICES = [c[0] for c in Event.CITY_CHOICES]

class Command(BaseCommand):
    help = "Populate the Event model with fake data"

    def handle(self, *args, **kwargs):
        # Make sure there’s at least one user
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found. Please create a user first."))
            return

        for _ in range(30):  # Change this to any number of events you want
            name = fake.catch_phrase()
            location = fake.address()
            description = " ".join(fake.sentences(nb=random.randint(3, 5)))
            city = random.choice(CITY_CHOICES)
            category = random.choice(CATEGORY_CHOICES)
            price = round(random.uniform(100, 1000), 2)
            convenience_fee = round(random.uniform(50, 150), 2)
            gst_percentage = 18.00  # Fixed

            # Download a random image
            image_url = "https://picsum.photos/600/400"
            image_path, _ = urllib.request.urlretrieve(image_url)
            image_file = open(image_path, 'rb')

            event = Event(
                seller=user,
                name=name,
                location=location,
                description=description,
                city=city,
                category=category,
                price=price,
                convenience_fee=convenience_fee,
                gst_percentage=gst_percentage,
            )
           
            event.image.save(f"{fake.slug()}.jpg", File(image_file), save=True)
            image_file.close()

            for i in range(1, 4):
                # Generate a random URL for each highlight image
                highlight_image_url = f"https://picsum.photos/600/400"
                try:
                    highlight_image_path, _ = urllib.request.urlretrieve(highlight_image_url)
                    highlight_image_file = open(highlight_image_path, 'rb')
                except urllib.error.HTTPError as e:
                    self.stdout.write(self.style.ERROR(f"Failed to retrieve highlight image {i} from {highlight_image_url}. Error: {e}"))
                    continue  # Skip this highlight image if it fails

                # Dynamically save the highlight images to the event
                getattr(event, f"highlight_image{i}").save(f"highlight{i}.jpg", File(highlight_image_file), save=True)
                highlight_image_file.close()

            # Save the event to the database
            event.save()
            # Save the event to the database


            # Add available dates
            from datetime import timedelta, date

            num_dates = random.randint(3, 5)
            start_date = date.today() + timedelta(days=random.randint(1, 10))

            for i in range(num_dates):
                available_date = AvailableDate.objects.create(
                    event=event,
                    date=start_date + timedelta(days=i * random.randint(1, 3))
                )
                self.stdout.write(self.style.SUCCESS(f"  └─ Added available date: {available_date.date}"))


            self.stdout.write(self.style.SUCCESS(f"Created event: {name}"))