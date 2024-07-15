from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import logging

# Define a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Student)
def create_main_plan(sender, instance, created, **kwargs):
    from .models import Plan  # Import Plan model here
    
    if created:
        if not Plan.objects.filter(user=instance).exists():
            # Create the "Main" plan for the user
            new_plan = Plan.objects.create(user=instance, name="Main")
            logger.info(f"Created new plan with id: {new_plan.id}")
        else:
            logger.info(f"Plan already exists for user: {instance}")

