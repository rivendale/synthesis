
from django.db import models
from ..models import BaseModel


class AddressTokens(BaseModel):
    """
    Address Tokens Model
    """
    address = models.CharField(null=False,
                               db_index=True, max_length=255,
                               unique=True, blank=False)
    bored_ape_yacht_token_count = models.IntegerField(default=0)
    rumble_kong_league_token_count = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of this `Address Tokens`.

        This string is used when a `Address Tokens` is printed in the console.
        """
        return f'{self.address} - {self.bored_ape_yacht_token_count}'

    class Meta:
        ordering = ['-created_at']
