from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image= models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} to {self.campaign.title}"

