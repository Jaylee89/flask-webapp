from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

#登陆表单
class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

#注册表单
class RegistrationForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名已被注册'
                                          u'字母开头, 只能包含字母或者点，下划线')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'再次输入', validators=[Required()])
    submit = SubmitField(u'注册')
#验证邮箱与用户名不重复
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已存在')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户已存在')

#更改密码
class ChangePasswordForm(Form):
    old_password = PasswordField(u'原始密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'再次确认', validators=[Required()])
    submit = SubmitField(u'更改密码')

#更改密码请求
class PasswordResetRequestForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'重设密码')

#更改密码表单
class PasswordResetForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮件地址不存在')

#更改电子邮件
class ChangeEmailForm(Form):
    email = StringField(u'请输入新邮件', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'请输入密码', validators=[Required()])
    submit = SubmitField(u'确认更改邮件')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已存在')
