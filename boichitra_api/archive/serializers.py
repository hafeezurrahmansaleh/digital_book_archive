from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField
# serializer for food menu


class BookDetailsSerializer(serializers.ModelSerializer):
    # cover_image = Base64ImageField(required=True)
    type = serializers.CharField(
        source="category.type.type",
        read_only=True
    )
    publisher_name = serializers.CharField(
        source="publisher.name",
        read_only=True
    )
    author_name = serializers.CharField(
        source="author.name",
        read_only=True
    )
    category = serializers.CharField(
        source="category.category_name",
        read_only=True
    )


    class Meta:
        model = BookDetails
        fields = (
            'pk',
            'type',
            'category',
            'author_name',
            'publisher_name',
            'short_name',
            'isbn',
            'book_name',
            'alternative_name',
            'description',
            'edition',
            'description',
            'cover_note',
            'rating',
        )
        read_only_fields = (
            'id',
            'publisher',
            'created',
            'updated'
        )


class SingleBookDetailsSerializer(serializers.ModelSerializer):
    # cover_image = Base64ImageField(required=True)
    type = serializers.CharField(
        source="category.type.type",
        read_only=True
    )
    publisher_name = serializers.CharField(
        source="publisher.name",
        read_only=True
    )
    author_name = serializers.CharField(
        source="author.name",
        read_only=True
    )
    category = serializers.CharField(
        source="category.category_name",
        read_only=True
    )

    class Meta:
        model = BookDetails
        fields = (
            'type',
            'category',
            'author_name',
            'publisher_name',
            'short_name',
            'isbn',
            'book_name',
            'alternative_name',
            'description',
            'edition',
            'description',
            'cover_note',
            'rating',
        )
        read_only_fields = (
            'type',
            'category',
            'author_name',
            'publisher_name',
            'short_name',
            'isbn',
            'book_name',
            'alternative_name',
            'description',
            'edition',
            'description',
            'cover_note',
            'rating',
        )


class CategorySerializer(serializers.ModelSerializer):
    # category_image = Base64ImageField(required=True)
    books = BookDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class BookContentSerializer(serializers.ModelSerializer):

    # shortname = self.request.query_params.get('book_shortname', None)
    # model = 'BookContent' + shortname[0:1]

    book_name = serializers.CharField(
        source="book.book_name",
        read_only=True
    )
    book_short_name = serializers.CharField(
        source="book.short_name",
        read_only=True
    )
    publisher_name = serializers.CharField(
        source="book.publisher.name",
        read_only=True
    )
    author_name = serializers.CharField(
        source="book.author.name",
        read_only=True
    )
    category = serializers.CharField(
        source="category.category_name",
        read_only=True
    )
    class Meta:
        model = BookContentS
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class SliderImageSerializer(serializers.ModelSerializer):
    # category_image = Base64ImageField(required=True)
    class Meta:
        model = SliderImage
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class BookRequestSerializer(serializers.ModelSerializer):
    request_by = serializers.CharField(
        source="request_by.phone",
        read_only=True
    )

    class Meta:
        model = BookRequest
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class AudioBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioBook
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class BoookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )
