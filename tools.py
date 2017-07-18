from flask import Blueprint
from flask import request, render_template, abort
from flask import current_app as app

bp = Blueprint('tools', __name__)


@bp.route('/myip')
def myip():
    ip = request.headers.get(app.config['REMOTE_ADDR_HEADER'], request.remote_addr)
    
    return render_template('myip.html', ip=ip)
