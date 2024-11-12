from django.db import models
from django.core.files.base import ContentFile
from PIL import Image as PilImage
import io
from django.core.exceptions import ValidationError



def validate_single_cv(value):
    if CV.objects.exists():
        raise ValidationError('Un seul CV peut être téléchargé.')


class CV(models.Model):
    file = models.FileField(upload_to='cv/', validators=[validate_single_cv])

    def __str__(self):
        return "CV"


class Work(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='works/')  # Spécifiez le dossier de sauvegarde des images
    link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = PilImage.open(self.image)
            img = img.convert('RGB')

            # Redimensionner l'image
            img = img.resize((300, 300), PilImage.LANCZOS)  # Utilisation de LANCZOS pour une meilleure qualité

            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_file = ContentFile(img_io.getvalue(), name=self.image.name)

            self.image = img_file

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class WorkDescription(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='descriptions')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class WorkImage(models.Model):
    product = models.ForeignKey(Work, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='work_images/')  # Spécifiez le dossier pour les images

    def save(self, *args, **kwargs):
        if self.image:
            img = PilImage.open(self.image)
            img = img.convert('RGB')

            # Redimensionner l'image
            img = img.resize((300, 300), PilImage.LANCZOS)

            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_file = ContentFile(img_io.getvalue(), name=self.image.name)

            self.image = img_file

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
