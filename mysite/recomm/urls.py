from django.conf.urls import url

from . import views

# The urls of polls app, different from urls in mysite/urls.py
app_name="recomm"
urlpatterns = [
    #url(r'^$', views.index, name='index')
    url(r'^login/$', views.login, name='login'),
    url(r'^logincheck/$', views.logincheck, name='logincheck'),

    url(r'^assistant/index/(?P<assistant_id>[0-9]+)/$', views.assistant_index, name='assistantindex'),#ok
    url(r'^teacher/index/(?P<teacher_id>[0-9]+)/$', views.teacher_index, name='teacherindex'),
    url(r'^student/index/(?P<student_id>[0-9]+)/$', views.student_index, name='studentindex'),
    # manage users
    url(r'^assistant/manage_student/(?P<assistant_id>[0-9]+)/$', views.manage_student, name='managestudent'), #ok
    url(r'^assistant/edit_teacher/(?P<assistant_id>[0-9]+)/$', views.edit_teacher, name='editteacher'),
    url(r'^assistant/edit_student/(?P<assistant_id>[0-9]+)/$', views.edit_student, name='editstudent'),
    url(r'^assistant/handin_studentessay/(?P<assistant_id>[0-9]+)/$', views.handin_studentessay, name='handinstudentessay'),
    url(r'^assistant/upload_studentessay/(?P<assistant_id>[0-9]+)/$', views.upload_studentessay,name='uploadstudentessay'),
    url(r'^assistant/user_info/(?P<assistant_id>[0-9]+)/$', views.assistant_userinfo, name='assistantuserinfo'),#####
    url(r'^assistant/change_passwd/(?P<assistant_id>[0-9]+)/$', views.ass_change_passwd, name='ass_change_passwd'),

    #ex: /polls/assistant/studentessay/1     # Need urls to begin the match process
    url(r'^assistant/studentessay/(?P<assistant_id>[0-9]+)/$', views.check_studentessay, name='checkstudentessay'),
    url(r'^assistant/teacheressay/(?P<assistant_id>[0-9]+)/$', views.check_teacheressay, name='checkteacheressay'),
    url(r'^assistant/matchresult/(?P<assistant_id>[0-9]+)/$', views.check_matchresult, name='checkmatchresult'),
    url(r'^assistant/matchpage/(?P<assistant_id>[0-9]+)/$', views.match_page, name='matchpage'),
    url(r'^assistant/beginmatch/(?P<assistant_id>[0-9]+)/$', views.begin_match, name='beginmatch'),
    url(r'^assistant/setrule/(?P<assistant_id>[0-9]+)/$', views.set_rule, name='setrule'),
    url(r'^assistant/submitrule/(?P<assistant_id>[0-9]+)/$', views.submit_rule, name='submitrule'),
    url(r'^assistant/getprogress/(?P<assistant_id>[0-9]+)/$', views.get_progress, name='getprogress'),
    url(r'^assistant/downloadresult/$', views.download_result, name='downloadresult'),
    url(r'^assistant/fileformatrule/$', views.download_fileformat_rule, name='downloadfileformatrule'),

    #ex: /polls/teacher/handin/1
    url(r'^teacher/handin/(?P<teacher_id>[0-9]+)/$', views.teacher_handin, name='teacherhandin'),
    url(r'^teacher/upload/(?P<teacher_id>[0-9]+)/$', views.teacher_upload,name='teacherupload'),
    url(r'^teacher/edit_teacher_essay/(?P<teacher_id>[0-9]+)/$', views.edit_teacher_essay,name='editteacheressay'),
    url(r'^teacher/check_essay/(?P<teacher_id>[0-9]+)/$', views.teacher_checkessay, name='teachercheckessay'),

    #ex: /polls/teacher/matchresult/1
    url(r'^teacher/matchresult/(?P<teacher_id>[0-9]+)/$', views.teacher_match,name='teachermatch'),
    #ex: /polls/teacher/download/nn.pdf
    url(r'^teacher/download/(?P<filename>.+)/$', views.teacher_download,name='teacher_download'),
    # ex: /polls/teacher/1/deletefile/nn.pdf
    url(r'^teacher/(?P<teacher_id>[0-9]+)/deletefile/(?P<filename>.+)/$', views.teacher_deletefile, name='teacher_deletefile'),
    url(r'^teacher/user_info/(?P<teacher_id>[0-9]+)/$', views.teacher_userinfo, name='teacheruserinfo'),#33
    url(r'^teacher/change_passwd/(?P<teacher_id>[0-9]+)/$', views.teacher_change_passwd, name='tch_change_passwd'),
    url(r'^teacher/(?P<teacher_id>[0-9]+)/download/(?P<filename>.+)/$', views.teacher_downlaod_stuessay, name='tchdownloadstuessay'),

    #ex: /polls/student/handin/1
    url(r'^student/handin/(?P<student_id>[0-9]+)/$', views.student_handin, name='studenthandin'),
    url(r'^student/upload/(?P<student_id>[0-9]+)/$', views.student_upload,name='studentupload'),
    #ex: /polls/student/matchresult/1
    url(r'^student/matchresult/(?P<student_id>[0-9]+)/$', views.student_match, name='studentmatch'),
    # ex: /polls/student/1/deletefile/nn.pdf
    url(r'^student/(?P<student_id>[0-9]+)/deletefile/(?P<filename>.+)/$', views.student_deletefile,
        name='student_deletefile'),

]