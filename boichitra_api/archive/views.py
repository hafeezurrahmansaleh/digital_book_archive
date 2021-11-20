import json

from django.apps import apps
from django.core import serializers as sz
from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated
)
from urllib3.connectionpool import xrange

from .serializers import *
from user_profile.models import *

# Create your views here.


class CategoryList(generics.ListCreateAPIView):
    """
    endpoint for creating book category
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save()


class CategoryDetail(generics.RetrieveUpdateAPIView):
    """
    endpoint for retrieve update menu category
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BookList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookDetailsSerializer
    queryset = BookDetails.objects.all()

    def get_queryset(self):
        list = BookDetails.objects.all()
        print(list[0].rating)
        return list

    def perform_create(self, serializer):
        user = self.request.user
        pub_instance = PublisherProfile.objects.get(user__username=user)
        # querydata = UserRole.objects.filter(user=user, is_rest_owner=False)
        if user.is_superuser:
            raise ValidationError('Superuser can not add books')
        elif user.is_customer:
            raise ValidationError('Customer can not books')
        else:
            serializer.save(publisher=pub_instance)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookDetailsSerializer
    queryset = BookDetails.objects.all()
    lookup_field = 'id'


class BookInfo(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SingleBookDetailsSerializer
    queryset = BookDetails.objects.all()
    lookup_field = 'short_name'


class MyBookList(generics.ListAPIView):
    """
    endpoint for logged publisher owner books
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookDetailsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = BookDetails.objects.filter(publisher__user=user)
        return queryset


class PublisherBooks(generics.ListAPIView):
    """
    endpoint for user to search book of a publisher
    by passing publisher id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookDetailsSerializer
    queryset = BookDetails.objects.all()

    def get_queryset(self):
        publisher_id = self.request.query_params.get('publisher_id', None)
        queryset = BookDetails.objects.filter(pubisher__id=publisher_id, is_available=True)
        return queryset


from django.views.generic.base import View


class DashboardContent(View):
    """
    endpoint for retrieving contents that will be displayed on dashboard
    """

    # permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        popular = BookDetails.objects.filter().order_by('-total_view')[:10]
        recent = BookDetails.objects.filter().order_by('-created_at')[:10]
        # popular = BookDetails.objects.filter().order_by('-total_view')[:10]
        info_dict = {
            'popular': popular,
            'recent': recent
        }
        # print(json.dumps(info_dict))
        # return HttpResponse(
        #     json.dumps(info_dict),
        #     content_type='application/json',
        # )
        popular_json = sz.serialize('json', popular, use_natural_foreign_keys=True)
        recent_json = sz.serialize('json', recent, use_natural_foreign_keys=True)

        return JsonResponse(json.loads('{"recent":' + recent_json + ',"popular":' + popular_json + '}'), safe=False,
                            content_type="text/json-comment-filtered")


#
# class CategoryBook(generics.RetrieveAPIView):
#     """
#         endpoint for user to search book of a publisher
#         by passing publisher id
#         """
#     permission_classes = (IsAuthenticated,)
#     serializer_class = BookListSerializer
#     def get_queryset(self):
#         queryset = BookDetails.objects.filter(
#
#         )
#         return queryset


class BookContent(View):
    """
    Endpoint for retrieving book content by passing book id and word per pages
    """
    permission_classes = (IsAuthenticated,)

    # serializer_class = BookContentSerializer
    # lookup_field = 'book_id'

    def get(self, request, *args, **kwargs):
        res = dict()
        book_id = self.kwargs.get('book_id', None)
        wpp = self.kwargs.get('wpp', None)
        book_details = BookDetails.objects.get(pk=book_id)

        book_json = sz.serialize('json', [book_details, ], use_natural_foreign_keys=True)
        res['book_details'] = book_json
        model = 'BookContent' + book_details.short_name[0:1]
        m = apps.get_model(app_label='archive', model_name=model)
        queryset = m.objects.get(book=book_details)
        c = queryset.content
        book_list = splitter(wpp, c)

        final_list = ["{" + l + "}" for l in book_list]
        print(json.dumps(final_list, ensure_ascii=False, indent=4).replace('"{', '{"page":"').replace('}"', '"}'))

        # for idx, ele in enumerate(list):
        #     res[idx] = ele

        # for piece in splitter(1000, c):
        # print(piece)
        # print(json.dumps(res,ensure_ascii=False,indent = 4))
        # print(json.dumps([z for z in list]))
        return JsonResponse(
            json.dumps(final_list, ensure_ascii=False, indent=4).replace('"{', '{"page":"').replace('}"', '"}'),
            safe=False, json_dumps_params={'ensure_ascii': False})


def splitter(n, s):
    pieces = s.split()
    # print(pieces)
    return (" ".join(pieces[i:i + n]) for i in xrange(0, len(pieces), n))


class SearchBook(generics.ListAPIView):
    """
    endpoint for user to search book by category or sort order
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookDetailsSerializer
    # page_size_query_param = 'page_size'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        try:
            cat = self.request.query_params.get('category', None)
        except:
            cat = None
        try:
            q_string = self.request.query_params.get('q_string', None)
        except:
            q_string = None
        try:
            sort_order = self.request.query_params.get('sort_order', None)
        except:
            sort_order = 'book_name'
        # item_pp = self.request.GET.get('item_pp',None)
        # page_no = self.request.GET.get('page_no',None)
        if cat is not None or cat != 'all':
            if cat == 'recent':
                queryset = BookDetails.objects.filter(is_active=True).order_by(sort_order)
            elif cat == 'popular':
                queryset = BookDetails.objects.filter(is_active=True).order_by(sort_order)
            else:
                queryset = BookDetails.objects.filter(category__category_name__iexact=cat, is_active=True).order_by(
                    sort_order)
        else:
            queryset = BookDetails.objects.filter().order_by(sort_order)
        print(queryset)
        print(cat)
        return queryset


class SliderImageListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SliderImageSerializer
    queryset = SliderImage.objects.filter(is_active=True)


class BookRequestCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookRequestSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_superuser:
            raise ValidationError('Superuser can not request for books')
        elif user.is_customer:
            customer_profile = CustomerProfile.objects.get(user=user)
            serializer.save(request_by=customer_profile)
        else:
            raise ValidationError('You do not have access to create book request. Only customers can do this')


class BookRequestListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookRequestSerializer

    def get_queryset(self):
        book_request_list = BookRequest.objects.all()
        return book_request_list


class MyBookRequestListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookRequestSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        customer_profile = CustomerProfile.objects.get(user=user)
        book_request_list = BookRequest.objects.filter(request_by=customer_profile)
        return book_request_list


class AudioBookDetailsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AudioBookSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'book_id'
    queryset = AudioBook.objects.all()
    # def get_queryset(self):
    #     # book_id = self.request.data.get('book_id', False)
    #     audio_book = AudioBook.objects.all()#get(book_id = 0)
    #     print(audio_book[0].id)
    #     return audio_book[0]


class BookReviewListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoookReviewSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        book_id = self.request.data.get('book', False)
        reviews = Review.objects.filter(book_id=book_id, status='Active')
        return reviews

    def perform_create(self, serializer):
        book_id = self.request.data.get('book', False)
        try:
            customer = CustomerProfile.objects.get(user=self.request.user)
        except Exception as e:
            raise ValidationError('You must have to update your profile before submitting a review')
        if Review.objects.filter(customer=customer,book_id = book_id).exists():
            raise ValidationError('You already submitted a review for this book')
        else:
            serializer.save(customer_id=customer.id, book_id=book_id)

