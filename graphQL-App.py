from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import graphene 
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView



app = Flask(__name__)


# configuring the SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"



class MusicObject(SQLAlchemyObjectType):
    class Meta:
       model = Music
       interfaces = (graphene.relay.Node, )


# Query class 
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_music = SQLAlchemyConnectionField(MusicObject.connection)



# Creates entries into the database
class CreateMusic(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    music = graphene.Field(lambda: MusicObject)

    def mutate(self, info, name, description):    # method to be called when writing data
        music = Music(
            name = name,
            description = description
        )
        if music:
            db.session.add(music)
            db.session.commit()

        return CreateMusic(music=music)



# Mutation class 
class Mutation(graphene.ObjectType):
    create_music = CreateMusic.Field()


# defining the schema 
schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route('/')
def index():
    return "<h1>Music Genres!</h>"




app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


if __name__ == "__main__":
    app.run(debug=True)