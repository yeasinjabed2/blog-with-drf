from rest_framework.views import APIView
from .serializers import BlogSerializer
from .models import Blog
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.utils.text import slugify
from random import randint
from rest_framework.permissions import IsAuthenticated


class CreateBlog(APIView):
    permission_classes = [IsAuthenticated]

    def post(sel, request):
        new_slug = slugify(request.data.get('title'))

        # duplicate slug validation
        slug = Blog.objects.filter(slug=new_slug)
        if slug.exists():
            def unique_slug(random_num):
                slug = f"{new_slug}-{random_num}"
                slug_exists = Blog.objects.filter(slug=slug).exists()
                if slug_exists:
                    return unique_slug(randint(1, 1000))
                else:
                    return slug

            new_slug = unique_slug(randint(1, 1000))

        request.data['slug'] = new_slug

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blog = Blog.objects.all()
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data)


class BlogDetail(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        slug_str = slugify(request.data.get('title'))
        slug = Blog.objects.filter(slug=slug_str)

        if not slug.exists():
            def unique_slug(random_num):
                slug = f"{slugify(request.data.get('title'))}-{random_num}"
                slug_exists = Blog.objects.filter(slug=slug).exists()
                if slug_exists:
                    return unique_slug(randint(1, 1000))
                else:
                    return slug

            new_slug = unique_slug(randint(1, 1000))
            request.data['slug'] = new_slug

        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
