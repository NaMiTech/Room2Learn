import logging
import os

from flask import ( render_template,
                    redirect,
                    url_for,
                    abort,
                    current_app,
                    send_from_directory,
                    request)
from flask_login import login_required, current_user
from app.auth.decorators import admin_required
from werkzeug.utils import secure_filename
from app.clases.models import Clase, Leccion

from . import admin_bp
from .forms import PostForm, ClaseForm

logger = logging.getLogger(__name__)


@admin_bp.route("/admin/new-lesson/", methods=['GET', 'POST'])
@login_required
@admin_required
def newLessonForm():
    """Crea una nueva leccion"""
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if 'post_image' in request.files:
            file = request.files['post_image']
            # Si el usuario no selecciona un fichero, el navegador
            # enviará una parte vacía sin nombre de fichero
            if file.filename:
                image_name = secure_filename(file.filename)
                images_dir = current_app.config['POSTS_IMAGES_DIR']
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)

            leccion = Leccion(title=title, description=content)
            leccion.icon = image_name
            leccion.save()

        logger.info(f'Guardanda una nueva leccion {title}')
        return redirect(url_for('public.index_page'))
    return render_template("admin/newLesson.html", form=form)


@admin_bp.route("/admin/new-class/", methods=['GET', 'POST'])
@login_required
@admin_required
def newClassForm():
    form = ClaseForm()
    if form.validate_on_submit():
        text = form.text.data
        lesson = form.lesson.data
        level = form.level.data
        type = form.type.data
        order = form.order.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if 'image' in request.files:
            file = request.files['image']
            # Si el usuario no selecciona un fichero, el navegador
            # enviará una parte vacía sin nombre de fichero
            if file.filename:
                image_name = secure_filename(file.filename)
                images_dir = current_app.config['POSTS_IMAGES_DIR']
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)

            clase = Clase(text=text,
                          lesson=lesson,
                          level=level,
                          type=type,
                          order=order)

            clase.image = image_name
            clase.save()

        logger.info(f'Guardanda una nueva clase {order}')
        return redirect(url_for('public.index_page'))
    return render_template("admin/newClase.html", form=form)


# Recuperar imagenes
@admin_bp.route('/media/posts/<filename>')
def media_posts(filename):
    dir_path = os.path.join(
        current_app.config['MEDIA_DIR'],
        current_app.config['POSTS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)
