from django.db.models import Avg, Sum, Count
from django_base64field.fields import Base64Field

# Create your models here.
from user_profile.models import *

from django.conf import settings
# from audiofield.fields import AudioField
import os.path

class ContentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.type


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, null=True, blank=True)
    category_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="categories/",
    )
    type = models.ForeignKey(
        ContentType,
        null=True,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return (self.category_name)

    def __str__(self):
        return self.category_name


class BookDetails(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'user_profile.Author',
        on_delete=models.CASCADE,
        related_name='book_author',
    )
    # writer = models.CharField(max_length=5000)
    publisher = models.ForeignKey(
        'user_profile.PublisherProfile',
        on_delete=models.CASCADE,
        related_name='book_publisher'
    )
    isbn = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    book_name = models.CharField(
        max_length=200,
        db_index=True
    )
    alternative_name = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(max_length=8000, null=True, blank=True)
    # cover_image = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to="cover_image/",
    # )
    edition = models.CharField(max_length=50)
    cover_note = models.TextField(max_length=1500)
    cover_image = Base64Field(max_length=900000, blank=True, null=True)
    keywords = models.TextField(max_length=1500)
    is_active = models.BooleanField(default=True)
    total_view = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_by = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name + ' - ' + self.book_name



# class BookDetailsAssociation(models.Model):
#     id = models.AutoField(primary_key=True)
#     book_details = models.ForeignKey(
#         BookDetails,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     table_id = models.BigIntegerField()
#     table_name = models.CharField(max_length=200)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class BookContentA(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentB(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentC(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentD(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentE(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentF(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentG(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentH(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentI(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentJ(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentK(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentL(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentM(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentN(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentO(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentP(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentQ(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentR(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentS(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentT(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentU(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentV(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentW(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentX(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentY(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class BookContentZ(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    content = models.TextField()
    add_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.book.short_name + ' - ' + self.book.book_name


class SliderImage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = Base64Field(max_length=900000, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.title


class BookRequest(models.Model):
    id = models.AutoField(primary_key=True)
    request_by = models.ForeignKey('user_profile.CustomerProfile', on_delete=models.CASCADE)
    request_title = models.CharField(max_length=100)
    request_body = models.CharField(max_length=500)
    additional_note = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.request_title)



class AudioBook(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, related_name='audio_book')
    description = models.TextField(null=True,blank=True)
    audio_file = models.FileField(upload_to='audio_books/', blank=True,
                            # ext_whitelist=(".mp3", ".wav", ".ogg"),
                            help_text=("Allowed type - .mp3, .wav, .ogg"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.book.book_name)

    # def audio_file_player(self):
    #     """audio player tag for admin"""
    #     if self.audio_file:
    #         file_url = settings.MEDIA_URL + str(self.audio_file)
    #         player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (
    #             file_url)
    #         return player_string

    # audio_file_player.allow_tags = True
    # audio_file_player.short_description = ('Audio file player')


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS = (
        ('New', 'New'),
        ('Active', 'Active'),
        ('Blocked', 'Blocked'),
    )
    book = models.ForeignKey(
        BookDetails,
        on_delete=models.CASCADE,
        related_name='book_review'
    )
    customer = models.ForeignKey('user_profile.CustomerProfile', on_delete=models.CASCADE,null=True,blank=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2,default=1, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.name = self.customer.full_name
        rating = Review.objects.filter(book=self.book, status='Active').aggregate(sum = Sum('rating'),count = Count('id'))
        avg = 0
        # avarage = Avg('rating'),
        if rating["sum"] is not None and rating["count"] is not None:
            avg = (float(rating["sum"]) + float(self.rating))/(float(rating["count"])+1.00)
        # print(float(rating["sum"]))
        # print(float(rating["count"]))
        print(avg)
        b = BookDetails.objects.filter(id=self.book_id).update(rating=avg)
        # b.save()
        super(Review, self).save(*args, **kwargs)

