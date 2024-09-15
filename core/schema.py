import graphene
from graphene_django import DjangoObjectType
from books.models import Book

class BookType(DjangoObjectType):
      
      class Meta:
            model = Book
            fields = ("id", "title", "description")
            
class CreateBookMutation(graphene.Mutation):
      # Especificamos que datos estamos recibiendo
      
      class Arguments:
            title = graphene.String()
            description = graphene.String()
            
      # Especificamos que datos vamos a retornar
      book = graphene.Field(BookType)
            
      def mutate(self, info, title, description):
            
            book = Book(title = title, description = description)
            book.save()
            # Retornamos la instancia con el libro que estamos recibiendo
            return CreateBookMutation(book=book)

class Query(graphene.ObjectType):
      
      hello = graphene.String(default_value="Hello")
      books = graphene.List(BookType)
      book = graphene.Field(BookType, id=graphene.ID(required=True))
      
      def resolve_books(self, info):
            return Book.objects.all()
      
      def resolve_book(self, info, id):
            return Book.objects.get(pk=id)
      
class Mutation(graphene.ObjectType):
      # return, params
      # create_book = graphene.Field(BookType, title = graphene.String(), description = graphene.String())
      create_book = CreateBookMutation.Field()
      
schema = graphene.Schema(query=Query, mutation=Mutation)      