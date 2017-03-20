# 注册蓝本导入视图函数
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
 