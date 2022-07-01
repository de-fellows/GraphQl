from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import graphene 
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
import json



app = Flask(__name__)


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
       interfaces = (graphene.relay.Node) 



class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_music = SQLAlchemyConnectionField(MusicObject)



class CreateMusic(graphene.Mutation):
    music = graphene.Field(MusicObject)
    class Arguments:
        name =graphene.String(required=True)
        description =graphene.String(required=True)
    
    def mutate(self, info, name, description):
        music = Music(name=name, description=description)
        if music:
            db.session.add(music)
            db.session.commit()
        return CreateMusic(music=music)



class Mutation(graphene.ObjectType):
    create_music = CreateMusic.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route('/')
def index():
    return "<h1>Music Genres!</h>"


@app.route("/music")
def get_music():
    music = Music.query.all()

    output = []
    for genre in music :
        music_info = {'name': genre.name, 'description': genre.description}

        output.append(music_info)

    return {"music": output}


@app.route('/music/<id>')
def get_music_id(id):         
    music = Music.query.get_or_404(id)         # this will either fetch the drink with a specific id or return a 404 error
    return {"name": music.name, "description":music.description}

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == "__main__":
    app.run()