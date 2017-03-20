from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

#表单类
class NameForm(Form):
    name = StringField(u'你的名字？', validators=[Required()])
    submit = SubmitField(u'提交')

#编辑个人信息
class EditProfileForm(Form):
    name = StringField(u'你的真名', validators=[Length(0, 64)])
    location = StringField(u'地区', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'提交')

#管理员编辑个人信息
class EditProfileAdminForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名必须字母开头 '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField(u'用户角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地区', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已存在')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')

#
class PostForm(Form):
    body = PageDownField(u"有什么新鲜事？", validators=[Required()])
    submit = SubmitField(u'提交')

#评论
class CommentForm(Form):
    body = StringField(u'评论', validators=[Required()])
    submit = SubmitField(u'提交')
