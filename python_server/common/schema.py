import graphene
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .my_database_meta_data import db_session, Department as DepartmentModel, Employee as EmployeeModel
from .my_database_meta_data import NewsUser as NewsUserModel, NewsLink as NewsLinkModel
from .utils import input_to_dictionary
import gzip
import zlib




class NewsUser(SQLAlchemyObjectType):
    class Meta:
        model = NewsUserModel
        interfaces = (relay.Node, )

class NewsUserConnection(relay.Connection):
    class Meta:
        node = NewsUser

class NewsLinkAttribute:
    description = graphene.String(description='Description of Link')
    url = graphene.String(description='URL of Link')

class NewsLink(SQLAlchemyObjectType):
    class Meta:
        model = NewsLinkModel
        interfaces = (relay.Node, )

class MyNewsLinkConnection(relay.Connection):
    class Meta:
        node = NewsLink

class CreateNewsLinkInput(graphene.InputObjectType, NewsLinkAttribute):
    '''Arguement to create a News Link'''
    pass

class CreateNewsLink(graphene.Mutation):
    '''Mutation to create a new department'''
    news_link = graphene.Field(lambda: NewsLink, description='News Link created by this mutation')

    class Arguments:
        input = CreateNewsLinkInput(required=True)

    def mutate(self, info, input):
        print('info from func call {}'.format(info))
        print('input from func call {}'.format(input))
        data = input_to_dictionary(input)
        print('data to be used in invokation {}'.format(data))
        data['id'] = db_session.execute('select news_link_seq.nextval from dual').scalar()
        data['created_at'] = datetime.utcnow()
        data['user_id'] = 1000
        print('DOES THIS URL WORL {}'.format(input['url']))
        data['url'] = input['url']
        #data['edited'] = datetime.utcnow()

        news_link = NewsLinkModel(**data)
        print('NEWS LINK :: {}'.format(news_link))
        db_session.add(news_link)
        db_session.commit()

        return CreateNewsLink(news_link=news_link)


class DepartmentAttribute:
    name = graphene.String(description='Name of Department')


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class CreateDepartmentInput(graphene.InputObjectType, DepartmentAttribute):
    '''Arguement to create a person'''
    pass


class CreateDepartment(graphene.Mutation):
    '''Mutation to create a new department'''
    department = graphene.Field(lambda: Department, description='Department created by this mutation')

    class Arguments:
        #name = graphene.String(description='Name of Department')
        input = CreateDepartmentInput(required=True)

    def mutate(self, info, input):
        print('info from func call {}'.format(info))
        print('input from func call {}'.format(input))
        data = input_to_dictionary(input)
        print('data to be used in invokation {}'.format(data))
        data['id'] = db_session.execute('select department_seq.nextval from dual').scalar()
        #data['created'] = datetime.utcnow()
        #data['edited'] = datetime.utcnow()

        department = DepartmentModel(**data)
        print('DEPARTMENT :: {}'.format(department))
        db_session.add(department)
        db_session.commit()

        return CreateDepartment(department=department)


class UpdateDepartmentInput(graphene.InputObjectType, DepartmentAttribute):
    ''' Arguments to update a person'''
    id = graphene.ID(required=True, description="Global Id of the Person")

class UpdateDepartment(graphene.Mutation):
    '''Update a Deparptment'''
    department = graphene.Field(lambda: Department, description='Department mutated by this mutation')

    class Arguments:
        input = UpdateDepartmentInput(required=True)

    def mutate(self, info, input):
        print('info from func call {}'.format(info))
        print('input from func call {}'.format(input))
        data = input
        print('data to be used in invokation {}'.format(input))

        department = db_session.query(DepartmentModel).filter_by(id=data['id'])
        department.update(data)
        db_session.commit()
        department = db_session.query(DepartmentModel).filter_by(id=data['id']).first()

        return UpdateDepartment(department=department)


class EmployeeAttribute:
    name = graphene.String(description='Name of Employee')
    hired_on = graphene.Date(description='Date of Hiring')
    department_id = graphene.ID(description='Department Id')

class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class MyEmployeeConnection(relay.Connection):
    class Meta:
        node = Employee

class SearchResult(graphene.Union):
    class Meta:
        types = (Department, Employee)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    search = graphene.List(SearchResult, q=graphene.String()) # List field for search results
    # Allows sorting over multiple columns, by default over the primary key
    print("Do we even run a query for graphene?")

    all_employees = SQLAlchemyConnectionField(MyEmployeeConnection)
    all_users = SQLAlchemyConnectionField(NewsUserConnection)
    all_links = SQLAlchemyConnectionField(MyNewsLinkConnection)
    #Disable sorting over this field
    department = SQLAlchemyConnectionField(DepartmentConnection)
    find_department = graphene.Field(lambda: Department, name=graphene.String())
    find_employee = graphene.Field(lambda: Employee, name=graphene.String())
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)


    def resolve_search(self, info, **args):
        q = args.get("q")
        employee_query = Employee.get_query(info)

    def resolve_find_department(self, info, **args):
        query = Department.get_query(info)
        name = args.get('name')
        return query.filter(DepartmentModel.name == name).first()

    def resolve_find_employee(self, info, **args):
        query = Employee.get_query(info)
        name = args.get('name')
        return query.filter(EmployeeModel.name == name).first()


class Mutation(graphene.ObjectType):
    createDepartment = CreateDepartment().Field()
    createNewsLink = CreateNewsLink().Field()
    updateDepartment = UpdateDepartment().Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Department, Employee, NewsLink])
