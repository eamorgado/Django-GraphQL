import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from movies.models import Actor, Movie

#Create GraphQL type for actor--------------------------------------------------
class ActorType(DjangoObjectType):
    class Meta: #Will have access to all relationships
        model = Actor

#Create GraphQL type for movie--------------------------------------------------
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie



#Define Query type--------------------------------------------------------------
class Query(ObjectType):
    #Define objects
    actor = graphene.Field(ActorType, id=graphene.Int()) #require id to specify
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    #Define resolves
    def resolve_actor(self,info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)
        return None

    def resolve_movie(self,info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)
        return None
    
    def resolve_actors(self,info, **kwargs):
        return Actor.objects.all()
    
    def resolve_movies(self,info, **kwargs):
        return Movie.objects.all()



#Define Mutations =>  operations to change data on server-----------------------
'''
    Mutations can be:
    +   Inputs: only used as arguments in a mutation when we want to pass an
                entire object instead of individual fields
    +   Payloads: regular types used as outputs for a mutation so we can extend
                    them as the API evolves
    
    ex inputs:
        input ActorInput {
            id: ID
            name: String!
        }

        input MovieInput {
            id: ID
            title: String
            actors: [ActorInput]
            year: Int
        }
    
    ex payloads:
        type ActorPayload {
            ok: Boolean
            actor: Actor
        }

        type MoviePayload {
            ok: Boolean
            movie: Movie
        }

    The mutation type brings all together:
    type Mutation {
        createActor(input: ActorInput) : ActorPayload
        createMovie(input: MovieInput) : MoviePayload
        updateActor(id: ID!, input: ActorInput) : ActorPayload
        updateMovie(id: ID!, input: MovieInput) : MoviePayload
    }
'''

#Define Mutations inputs--------------------------------------------------------
class ActorInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()

class MovieInput(graphene.InputObjectType):
    id = graphene.Int()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()



## Create mutations
# Create/Update Actor ----------------------------------------------------------
class CreateActor(graphene.Mutation):
    class Arguments: #input arguments for the mutator
        input = ActorInput(required=True)
    
    ok = graphene.Boolean()             #Payload
    actor = graphene.Field(ActorType)   #Payload

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name) #Using arguments
        actor_instance.save()
        return CreateActor(ok=ok,actor=actor_instance) #using payload
    
class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)
    
    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)


## Create mutations
# Create/Update Movie ----------------------------------------------------------
class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)
    
    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod 
    def mutate(root, info, input=None):
        ok = True
        actors = []
        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)
            if actor is None: #Create
                return CreateMovie(ok=False, movie=None)
            actors.append(actor)
        
        movie_instance = Movie(
            title=input.title,
            year=input.year
        )
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance)
    
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)
    
    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod 
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk=actor_input.id)
                if actor is None:
                    return UpdateMovie(ok=False, movie=None)
                actors.append(actor)
            movie_instance.title = input.title
            movie_instance.year = input.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)


#Define Mutation type-----------------------------------------------------------
class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field() 



#Defining schema----------------------------------------------------------------
schema = graphene.Schema(query=Query, mutation=Mutation)