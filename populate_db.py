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

    # --- 4. CREAR CRUCEROS Y ASIGNARLOS BALANCEADAMENTE ---
    # Regla: Cada destino tiene entre 1 y 3 cruceros. 
    # Un crucero pertenece a un solo destino (no se comparten).
    
    print(f"Creating {len(cruises_data)} cruises...")
    all_cruises_objects = []
    
    # Primero creamos todos los objetos Cruise sin asignar destinos aún
    for c_data in cruises_data:
        cruise = Cruise.objects.create(
            name=c_data['name'],
            desc=c_data['desc'],
            price=Decimal(random.randint(2000, 25000)),
            max_capacity=random.randint(10, 100),
            available_seats=random.randint(1, 10)
        )
        all_cruises_objects.append(cruise)

    # Mezclamos los cruceros para que la asignación sea aleatoria
    random.shuffle(all_cruises_objects)

    print("Assigning cruises to destinations (1-3 per destination, disjoint)...")
    
    # Verificamos que hay suficientes cruceros para dar al menos 1 a cada destino
    if len(all_cruises_objects) < len(created_destinations):
        print("WARNING: Not enough cruises to give 1 to each destination!")

    # Diccionario para controlar asignaciones: {destination: [list_of_cruises]}
    dest_assignments = {dest: [] for dest in created_destinations}
    unassigned_cruises = all_cruises_objects[:] # Copia de la lista

    # Paso 1: Asegurar que cada destino tenga al menos 1 crucero
    for dest in created_destinations:
        if unassigned_cruises:
            c = unassigned_cruises.pop()
            dest_assignments[dest].append(c)

    # Paso 2: Repartir el resto de cruceros (hasta un máximo de 3 por destino)
    while unassigned_cruises:
        # Elegir un destino al azar
        target_dest = random.choice(created_destinations)
        
        # Solo asignar si tiene menos de 3
        if len(dest_assignments[target_dest]) < 3:
            c = unassigned_cruises.pop()
            dest_assignments[target_dest].append(c)
        else:
            # Si todos los destinos ya tienen 3 y aun sobran cruceros,
            # rompemos el ciclo para evitar bucle infinito (o podríamos aumentar el límite)
            # Verificamos si hay algún destino con espacio
            if all(len(v) >= 3 for v in dest_assignments.values()):
                print("All destinations have 3 cruises. Remaining cruises will be unassigned.")
                break

    # Paso 3: Guardar las relaciones en la base de datos
    for dest, cruises in dest_assignments.items():
        for cruise in cruises:
            # Asignamos el destino. Al ser ManyToMany, usamos set() pasando la lista [dest]
            # Esto cumple la regla: "que otro destino no pueda tener un mismo crucero"
            # porque cada crucero de la lista 'all_cruises_objects' solo se asigna una vez aquí.
            cruise.destinations.set([dest])
            cruise.save()
            # Añadimos a la lista general para usar en compras/reviews
            # (Nota: all_cruises ya tiene todos, pero esto confirma los asignados si quisiéramos filtrar)

    # --- 5. GENERAR ACTIVIDAD (COMPRAS Y REVIEWS) ---
    print("Generating purchases and reviews...")
    
    # Obtenemos solo los cruceros que efectivamente tienen destino asignado
    active_cruises = [c for c in all_cruises_objects if c.destinations.exists()]

    for user in created_users:
        # Cada usuario compra 2 cruceros aleatorios (si hay suficientes)
        if len(active_cruises) >= 2:
            user_cruises = random.sample(active_cruises, 2)
        else:
            user_cruises = active_cruises
        
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
            # Como ahora la regla es 1 crucero -> 1 destino, este bucle corre una sola vez por crucero
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