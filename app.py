from flask import Flask, render_template, redirect, url_for, request
from models import db, Category, Dish


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trattoria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():  # put application's code here
    return redirect(url_for("menu"))

@app.route('/menu')
@app.route('/menu/<slug>')
def menu(slug=None):
    categories = Category.query.order_by(Category.id).all()
    current = None
    query = Dish.query.filter_by(is_available=True)

    if slug:
        current = Category.query.filter_by(slug=slug).first_or_404()
        query = query.filter_by(category_id=current.id)

    q = request.args.get('q',"").strip()
    if q:
        query = query.filter(Dish.name.ilike(f"%{q}%"))

    dishes = query.order_by(Dish.category_id, Dish.name).all()
    return render_template('menu.html', categories=categories, current=current, dishes=dishes, q=q)

@app.route('/dish/<int:dish_id>')
def dish_detail(dish_id):
    dish = db.get_or_404(Dish, dish_id)
    return render_template('dish.html', dish=dish)

@app.route('/delivery')
def deliveryForm():
    return render_template('delivery.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
