from flask import flash, jsonify, request, abort, url_for, current_app
from thesisarchiving import bcrypt, mail
from thesisarchiving.models import Role, Area, Keyword, Thesis, Semester, Program, Category
from flask_login import current_user
from flask_mail import Message
import os, pathlib #uuid
from fuzzywuzzy import fuzz
from functools import wraps


def has_roles(*roles):
    def decorator(original_route):
        @wraps(original_route) #wraps is for preserving functions passed
        def wrapped_function(*args, **kwargs):
            
            if not current_user.is_authenticated:
                abort(401)

            user_roles = [role.name for role in current_user.roles]

            missing_roles = [role for role in roles if role not in user_roles]

            if current_user in Role.query.filter_by(name='Superuser').first().permitted:
                return original_route(*args,**kwargs)

            if missing_roles:
                abort(403)
            return original_route(*args,**kwargs)

        return wrapped_function

    return decorator

def get_file(file,form_fn):

    form_path = None
    form_file = None

    if file == 'form_file':
        form_path = os.path.join(current_app.root_path, 'static','thesis attachments','form file', form_fn)
    if file == 'thesis_file':
        form_path = os.path.join(current_app.root_path, 'static','thesis attachments','thesis file', form_fn)
    
    form_file = pathlib.Path(form_path)

    return form_file if form_file.is_file() else None

def fuzz_tags(tag_input, table_name):

    def fuzz_name(q_tag):
        return fuzz.token_set_ratio(tag_input, q_tag.name)

    tag_input = tag_input.lower()
    query = None
    tags = []

    if table_name == 'area':
        query = Area.query

    if table_name == 'keywords':
        query = Keyword.query

    if query:
        for r in query:
            fuzz_val = fuzz.token_set_ratio(tag_input, r.name.lower())
            if fuzz_val >= 30:
                tags.append(r)

    tags.sort(key=fuzz_name,reverse=True)

    return tags

def advanced_search(title=None,area=None,keywords=None, program=None, category=None, school_year=None, semester=None, adviser=None):
    #searching uses 'AND' logic
    #maganda maimplement yung 'OR' for general searching

    #declare variables
    suggested = Category.query.filter_by(name='Suggested').first()
    query = Thesis.query.filter(Thesis.category != suggested) #gumagana yung fuzz_title sort dito
    sq_filters = []    
    query_lev = []
    #levenshtein sorting
    def fuzz_title(q_thesis):
        #check kung successful yung lower ng title and q_thesis
        return fuzz.token_set_ratio(title, q_thesis.title)


    # su = (Role.query.filter_by(name='Superuser').first().permitted).subquery()
    # ad = (Role.query.filter_by(name='Admin').first().permitted).subquery()
    # st = (Role.query.filter_by(name='Student').first().permitted).subquery()
    
    #subqueries
    #if filter exist, filter
    #else no result for an invalid filter(non existing data)
    if area:
        area = area.lower() #dito declare kasi what if None diba edi mag error dahil cant lower a none

        if Area.query.filter_by(name=area).first():  
            sq_filters.append((Area.query.filter_by(name=area).first().theses).subquery())
        else:
            return None
            

    if keywords: 
        keywords = [k.lower() for k in keywords]
        for k in keywords:
            if Keyword.query.filter_by(name=k).first():
                sq_filters.append((Keyword.query.filter_by(name=k).first().theses).subquery())
            else:
                return None

    #by id since non modifiable by user naman to
    if program:
        if Program.query.get(int(program)):  
            sq_filters.append((Program.query.get(int(program)).theses).subquery())
        else:
            return None

    if semester:
        if Semester.query.get(int(semester)):  
            sq_filters.append((Semester.query.get(int(semester)).theses).subquery())
        else:
            return None

    #join
    #sq - subquery
    if sq_filters:
        for sq in sq_filters:
            query = query.join(sq, Thesis.id == sq.c.id)

    #sort 
    if title: #lev
        #this sort will remove titles that are not similar as determined by levenshtein (cutoff 30)
        for r in query:
            if fuzz.token_set_ratio(title, r.title) >= 30:
                query_lev.append(r)
                # query_lev.append(r.title)
        query_lev.sort(key=fuzz_title, reverse=True) 
        # query = query.paginate()
        # query.items = query_lev
        return {'query':query_lev, 'count':len(query_lev)}
# pag thesis registration, show all results
    else: #date
        query = query.order_by(Thesis.date_register.desc())
        # query = query.order_by(Thesis.date_register.desc()).paginate()
        return {'query':query, 'count':query.count()}



#########################################################################

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('UE CCSS Thesis Archiving',
                  sender='no-reply@ueccssrnd.tech',
                  recipients=[user.email])
    msg.body = f'''To reset your Archiving System Account password, visit the following link:
{url_for('main.reset_password', token=token, _external=True)}
If you did not make this request, please ignore. This message will expire after 24 hours.

This is an autogenerated message. Do not reply.
'''
    mail.send(msg)

