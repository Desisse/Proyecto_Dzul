from flask import Flask, Response, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from api.models import UserModel, db
import re

