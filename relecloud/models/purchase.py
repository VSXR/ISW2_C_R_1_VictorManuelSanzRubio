from django.db import models
from django.conf import settings
from .destination import Destination
from .cruise import Cruise

class Purchase(models.Model):
    """
    Representa una compra (reserva) hecha por un usuario 
    para un destino o un crucero.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="purchases"
    )
    
    # Permitimos que la compra sea de un destino O un crucero
    destination = models.ForeignKey(
        Destination, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    cruise = models.ForeignKey(
        Cruise, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        item = self.destination.name if self.destination else self.cruise.name
        return f"Compra de {item} por {self.user.username}"

    class Meta:
        # Asegura que un usuario no pueda comprar el mismo item varias veces
        # (Puedes quitar esto si un usuario SÍ puede comprar lo mismo múltiples veces)
        unique_together = [['user', 'destination', 'cruise']]