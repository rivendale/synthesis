
from django.db import models
from ..models import BaseModel


class BaycToken(BaseModel):
    """
    Bayc Tokens Model
    """
    metadata = models.JSONField(default=dict)
    token_id = models.IntegerField()


class RklToken(BaseModel):
    """
    Rkl Tokens Model
    """
    metadata = models.JSONField(default=dict)
    token_id = models.IntegerField()


class AddressTokens(BaseModel):
    """
    Address Tokens Model
    """
    address = models.CharField(null=False,
                               db_index=True, max_length=255,
                               unique=True, blank=False)
    bored_ape_yacht = models.ManyToManyField(BaycToken,
                                             related_name='bored_ape_yacht')
    rumble_kong_league = models.ManyToManyField(RklToken,
                                                related_name='rumble_kong_league')

    @property
    def bored_ape_yacht_token_count(self):
        """
        Returns the number of tokens in the `bored_ape_yacht` ManyToManyField.
        """
        return self.bored_ape_yacht.count()

    @property
    def rumble_kong_league_token_count(self):
        """
        Returns the number of tokens in the `rumble_kong_league` ManyToManyField.
        """
        return self.rumble_kong_league.count()

    def __str__(self):
        """
        Returns a string representation of this `Address Tokens`.

        This string is used when a `Address Tokens` is printed in the console.
        """
        return f'{self.address} - {self.bored_ape_yacht_token_count}'

    class Meta:
        ordering = ['-created_at']
