from flask import Flask, render_template
from mssqlUtil import MssqlHelper
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    sql = None
    name = request.args.get("name")
    page_param = request.args.get("page")
    page = 1
    if page_param is None:
        page = 1
    if int(page_param) < 1:
        page = 1
    sql_helper = MssqlHelper()
    if name is not None and name != "":
        sql = "SELECT * FROM(SELECT row_number() over(ORDER BY A.FID) as [num],A.FID,A.FVideoTitle,A.FVideoImgurl,A.FVideoPageLink,A.FVideoUrl,B.FSiteName FROM Spider_Video A WITH(NOLOCK)  LEFT JOIN Spider_Video_Site B WITH(NOLOCK) ON A.FFromSiteID=B.FID WHERE FVideoTitle LIKE %s)C WHERE C.num BETWEEN {0} AND {1}".format(
            (page - 1) * 50, page * 50)
        sql_helper.execute(sql,("%"+name+"%"))
    else:
        sql = "SELECT * FROM(SELECT row_number() over(ORDER BY A.FID) as [num],A.FID,A.FVideoTitle,A.FVideoImgurl,A.FVideoPageLink,A.FVideoUrl,B.FSiteName FROM Spider_Video A WITH(NOLOCK)  LEFT JOIN Spider_Video_Site B WITH(NOLOCK) ON A.FFromSiteID=B.FID)C WHERE C.num BETWEEN {0} AND {1}".format(
            (page - 1) * 50, page * 50)
        sql_helper.execute(sql)
    row = sql_helper.cursor.fetchall()
    sql_helper.close_cursor()
    sql_helper.close()
    return render_template('hello.html', video_list=row)


if __name__ == '__main__':
    app.run(port=7756)
