import os
import django
import random
import json
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from relecloud.models import Destination, Cruise, Purchase, CruiseReview, DestinationReview

# Función auxiliar para cargar datos JSON
def load_data(filename):
    file_path = os.path.join('data', filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def populate():
    print("Cleaning old database...")
    Purchase.objects.all().delete()
    CruiseReview.objects.all().delete()
    DestinationReview.objects.all().delete()
    Cruise.objects.all().delete()
    Destination.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    # --- 1. CARGAR DATOS DESDE ARCHIVOS ---
    print("Loading data files...")
    users_data = load_data('users.json')
    destinations_data = load_data('destinations.json')
    cruises_data = load_data('cruises.json')
    reviews_data = load_data('reviews.json')

    # --- 2. CREAR USUARIOS ---
    print(f"Creating {len(users_data)} users...")
    created_users = []
    for u in users_data:
        user = User.objects.create_user(username=u['username'], email=f"{u['username']}@test.com", password=u['password'])
        created_users.append(user)

    # --- 3. CREAR DESTINOS ---
    print(f"Creating {len(destinations_data)} destinations...")
    created_destinations = []
    for i, d in enumerate(destinations_data):
        dest = Destination.objects.create(
            name=d['name'],
            desc=d['desc'],
            image_url=d['image'],
            position=i
        )
        created_destinations.append(dest)

    # --- 4. CREAR CRUCEROS Y ASIGNAR DESTINOS ---
    print(f"Creating {len(cruises_data)} cruises...")
    all_cruises = []
    
    for c_data in cruises_data:
        cruise = Cruise.objects.create(
            name=c_data['name'],
            desc=c_data['desc'],
            price=Decimal(random.randint(2000, 25000)),
            max_capacity=random.randint(10, 100),
            available_seats=random.randint(1, 10)
        )
        
        # Asignar aleatoriamente de 1 a 5 destinos por crucero
        # min() asegura que no intentemos coger más destinos de los que existen
        num_dests = random.randint(1, 5)
        num_dests = min(num_dests, len(created_destinations))
        
        selected_dests = random.sample(created_destinations, num_dests)
        cruise.destinations.set(selected_dests)
        cruise.save()
        all_cruises.append(cruise)

    # --- 5. GENERAR ACTIVIDAD (COMPRAS Y REVIEWS) ---
    print("Generating purchases and reviews...")
    
    for user in created_users:
        # Cada usuario compra 2 cruceros aleatorios
        user_cruises = random.sample(all_cruises, 2)
        
        for cruise in user_cruises:
            # Compra del crucero
            Purchase.objects.create(user=user, cruise=cruise)
            
            # Review aleatoria para el crucero
            rev_data = random.choice(reviews_data)
            CruiseReview.objects.create(
                cruise=cruise,
                name=user.username,
                rating=rev_data['rating'],
                comment=rev_data['text']
            )
            
            # Compra y Review para los destinos de ese crucero
            for dest in cruise.destinations.all():
                Purchase.objects.create(user=user, destination=dest)
                
                rev_data_dest = random.choice(reviews_data)
                DestinationReview.objects.create(
                    destination=dest,
                    name=user.username,
                    rating=rev_data_dest['rating'],
                    comment=rev_data_dest['text']
                )

    print("\nDatabase populated successfully!")

if __name__ == '__main__':
    populate()