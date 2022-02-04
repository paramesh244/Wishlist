from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, Unicode, DateTime
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup

tz = pytz.timezone('Asia/Kolkata')
datetime_ind = datetime.now(tz)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlist.db'
app.secret_key = '696969'
db = SQLAlchemy(app)

meta = MetaData()

engine = create_engine('sqlite:///wishlist.db', echo = True)

class Users(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)    

    def __repr__(self):
        return '<Item %r>' % self.id

@app.route('/ext', methods=['POST','GET'])
def ext():
    f=open('seesion.txt','r')
    name=f.read()
    f.close()
    print('ext route')
    username =name
    class Model(db.Model):
        __tablename__=username
        __table_args__ = {'extend_existing': True} 
        name = db.Column(db.String, primary_key=True)
        link = db.Column(db.String)    #add nullable=False
        site_name = db.Column(db.String)
        image = db.Column(db.Unicode)
        price = db.Column(db.String, default=0)
        date_added = db.Column(db.DateTime, default=datetime_ind)
    if request.method == 'POST':
        print('Got POST request')
        goturl = request.data
        item_name = goturl.decode("utf-8") 
        print(item_name)
        if 'bewakoof' in item_name :
            req = requests.get(item_name)
            soup = BeautifulSoup(req.content,'html.parser')
            price = soup.find('span', class_="sellingPrice").text
            name = soup.find('h1', id = "testProName").text
            image = soup.find_all('img')
            image_link = image[1]['src']
            new_item = Model(name=name, link=item_name, site_name='Bewakoof.com', image=image_link, price=price)

            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        elif 'koovs'in item_name :
             req = requests.get(item_name)
             soup = BeautifulSoup(req.content,'html.parser')
             price = soup.find('span',class_="money").string
             title = soup.find('h1', class_ = "product_title entry-title fwm").string
             image = soup.find_all('img')
             image_link = image[4]['src']
             new_item = Model(name=title, link=item_name, site_name='koovs', image=image_link, price=price)
             db.session.add(new_item)
             db.session.commit()
             return redirect('/')

        elif 'streetstylestore' in item_name:
             req = requests.get(item_name)
             soup = BeautifulSoup(req.content,'html.parser')
             price = soup.find('span',id="our_price_display").string
             name = soup.find('h2', class_ = "product-name").string
             image = soup.find_all('img')
             image_link = image[2]['src']
             new_item = Model(name=name, link=item_name, site_name='SSS', image=image_link, price=price)

             db.session.add(new_item)
             db.session.commit()
             return redirect('/')

        elif 'amazon' in item_name:
            req = requests.get(item_name)
            soup = BeautifulSoup(req.content,'html.parser')
            price= soup.find('span', class_="apexPriceToPay")
            name = soup.find('span', id ="productTitle").string
            image = soup.find_all('img')
            image_link = image[0]['src']
            new_item = Model(name=name, link=item_name, site_name='amazon', image=image_link, price=price)

            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        elif 'flipkart' in item_name :
             req = requests.get(item_name)
             soup = BeautifulSoup(req.content,'html.parser')
             price = soup.find('div',class_="_30jeq3 _16Jk6d").string
             title = soup.find('span', class_ = "B_NuCI").text
             image = soup.find_all('img')
             image_link ="static\img\flipkart.png.crdownload" #soup.find('img', class_="_2r_T1I _396QI4")['src']
             new_item = Model(name=title, link=item_name, site_name='Flipkart', image=image_link, price=price)
             db.session.add(new_item)
             db.session.commit()
             return redirect('/')

        elif 'redwolf' in item_name:
            req=requests.get(item_name)
            soup = BeautifulSoup(req.content,'html.parser')
            price = soup.find('span',class_="no_special_price_original_price")
            name = soup.find('h2', class_ = "product_title")
            image = soup.find_all('img')
            image_link = image[6]['src']
            new_item = Model(name=name, link=item_name, site_name='Redwolf', image=image_link, price=price)

            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        # if 'amazon' in item_name :
        #     req = requests.get(item_name)
        #     soup = BeautifulSoup(req.content,'html.parser')
        #     price = soup.find('span', id ="priceblock_ourprice")
        #     name = soup.find('span', id ="productTitle")
        #     image = soup.find_all('img')
        #     image_link = image[1]['src']
        #     new_item = Model(name=name, link=item_name, site_name='amazon.in', image=image_link, price="Rs "+price)

        #     db.session.add(new_item)
        #     db.session.commit()
        #     return redirect('/')
      
    return redirect('/')

@app.route('/', methods=['POST','GET'])
def index():
    print('Request active')
    if 'username' in session:
        print('Session active')
        username = session['username']
        class Model(db.Model):
            __tablename__=username
            __table_args__ = {'extend_existing': True} 
            name = db.Column(db.String, primary_key=True)
            link = db.Column(db.String)    #add nullable=False
            site_name = db.Column(db.String)
            image = db.Column(db.Unicode)
            price = db.Column(db.String, default=0)
            date_added = db.Column(db.DateTime, default=datetime_ind)
        
        if request.method == 'POST':
            flag = 0
            print('Got POST request')
            item_name = request.form['content']
            print('data: '+item_name)
            if 'streetstylestore' in item_name :
                flag = 1
                try:
                    req = requests.get(item_name)
                    soup = BeautifulSoup(req.content,'html.parser')
                    price = soup.find('span',id="our_price_display").string
                    name = soup.find('h2', class_ = "product-name").string
                    image = soup.find_all('img')
                    image_link = image[2]['src']
                    new_item = Model(name=name, link=item_name, site_name='SSS', image=image_link, price=price)

                    db.session.add(new_item)
                    db.session.commit()
                    return redirect('/')
                except AttributeError:
                    try:
                        item_link = item_name
                        prodNum = ''.join(filter(lambda i: i.isdigit(), item_link))
                        req = "https://streetstylestore.com/index.php?id_product="+prodNum+"&controller=product"
                        reqToFilter = requests.get(req)
                        soup = BeautifulSoup(reqToFilter.content,'html.parser')
                        price = soup.find('span',id="our_price_display").string
                        name = soup.find('h2', class_ = "product-name").string
                        image = soup.find_all('img')
                        image_link = image[2]['src']
                        new_item = Model(name=name, link=item_name, site_name='SSS', image=image_link, price=price)

                        db.session.add(new_item)
                        db.session.commit()
                        return redirect('/')
                    except:
                        try:
                            req = requests.get(item_name)
                            soup = BeautifulSoup(req.content,'html.parser')                        
                            name = soup.find('title').string
                            image = soup.find_all('img')
                            image_link = image[0]['src']
                            new_item = Model(name=name, link=item_name, site_name='SSS', image=image_link, price='NA')

                            db.session.add(new_item)
                            db.session.commit()
                            return redirect('/')
                        except:
                            return redirect('/')

            if 'bewakoof' in item_name :
                flag = 1
                try:
                    req = requests.get(item_name)
                    soup = BeautifulSoup(req.content,'html.parser')
                    price = soup.find('span', id = "testNetProdPrice").string
                    name = soup.find('h1', id = "testProName").string
                    image = soup.find_all('img')
                    image_link = image[1]['src']
                    new_item = Model(name=name, link=item_name, site_name='Bewakoof.com', image=image_link, price="Rs "+price)

                    db.session.add(new_item)
                    db.session.commit()
                    return redirect('/')
                except:
                    return redirect('/')

            if 'koovs'in item_name :
                flag = 1
                try:
                    req = requests.get(item_name)
                    soup = BeautifulSoup(req.content,'html.parser')
                    price = soup.find('div',class_="pd-discount-price")
                    title = soup.find('div', class_ = "product-name")
                    image = soup.find_all('img')
                    #image_link = image[2]['src']
                    new_item = Model(name=title.string, link=item_name, site_name='koovs', image='https://getfreedeals.co.in/wp-content/uploads/2012/08/Koovs-logo.jpg', price=price.string)

                    db.session.add(new_item)
                    db.session.commit()
                    return redirect('/')
                except:
                    return redirect('/')

            if flag == 0:
                return render_template('alternate.html', item_name=item_name)

            if 'amazon'in item_name :
                flag = 1
                try:
                  req = requests.get(item_name)
                  soup = BeautifulSoup(req.content,'html.parser')
                  price = soup.find('span', id ="priceblock_ourprice")
                  name = soup.find('span', id ="productTitle")
                  image = soup.find_all('img')
                  image_link = image
                  new_item = Model(name=name, link=item_name, site_name='amazon', image=image_link, price="Rs "+price)

                  db.session.add(new_item)
                  db.session.commit()
                  return redirect('/')
                except:
                    return redirect('/')

            if flag == 0:
                return render_template('alternate.html', item_name=item_name)

        else:
            items = Model.query.order_by(Model.date_added).all()
            wsr = 'Bewakoof.com, StyleStreetStore, Koovs.'
            sesh='Logout'
            return render_template('index.html', items=items, wsr = wsr, sesh=sesh)
    else:
        return redirect('/signin')

@app.route('/sesh')
def sesh():
    if 'username' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/alternate', methods=['POST','GET'])
def alternate():
    username = session['username']
    class Model(db.Model):
        __tablename__=username
        __table_args__ = {'extend_existing': True} 
        name = db.Column(db.String, primary_key=True)
        link = db.Column(db.String)    #add nullable=False
        site_name = db.Column(db.String)
        image = db.Column(db.Unicode)
        price = db.Column(db.String, default=0)
        date_added = db.Column(db.DateTime, default=datetime_ind)

    if request.method == 'POST':    
        # try:
        # name=name, link=item_name, site_name='Bewakoof', image=image_link, price=price
        item_name = request.form['item_name']
        name = request.form['name']
        site_name = request.form['site_name']
        image_link = request.form['img_link']
        if image_link == '':
            image_link = 'https://static.vecteezy.com/system/resources/thumbnails/001/932/473/small_2x/shopping-bag-paper-isolated-icon-free-vector.jpg'
        price = request.form['price']
        
        new_item = Model(name=name, link=item_name, site_name=site_name, image=image_link, price='Rs.'+price)

        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
        # except:
        #     return redirect('/')

@app.route('/register', methods=['POST','GET'])
def register():

    usersdb = create_engine('sqlite:///wishlist.db', echo = True)
    meta = MetaData()

    users = Table(
        'users', meta, 
        Column('username', String, primary_key = True), 
        Column('password', String)
    )
    
    meta.create_all(usersdb)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Table(
            username, meta, 
            Column('name', String, primary_key=True),
            Column('link', String),    #add nullable=False
            Column('site_name', String),
            Column('image', Unicode),
            Column('price', String, default=0),
            Column('date_added', DateTime, default=datetime_ind),
        )
        meta.create_all(usersdb)

        try:
            if(bool(db.session.query(Users).filter_by(username=username).first())):
                return render_template('reg_error.html')
            else:
                new_user = Users(username=username, password=password)

                db.session.add(new_user)
                db.session.commit()
                return render_template('signin.html')
            
        except:
            return 'Error in registration <br><a href="/register">Try again</a>'      
    else:
        return render_template('register.html')

@app.route('/signin', methods=['POST','GET'])
def signin():

    usersdb = create_engine('sqlite:///wishlist.db', echo = True)
    meta = MetaData()

    users = Table(
        'users', meta, 
        Column('username', String, primary_key = True), 
        Column('password', String),
    )
    
    meta.create_all(usersdb)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if(bool(db.session.query(Users).filter_by(username=username).first())):
            if(bool(db.session.query(Users).filter_by(password=password).first())):
                session['username'] = username
                file1=open('seesion.txt','w')
                file1.write(username)
                file1.close()
                return redirect('/')
            else:
                return render_template('signin_error.html')
        else:
            return render_template('signin_error.html')
    else:
        return render_template('signin.html')        

@app.route('/delete/<string:name>')
def delete(name):
    if 'username' in session:

        username = session['username']

        class Model(db.Model):
            __tablename__=username
            __table_args__ = {'extend_existing': True} 
            name = db.Column(db.String, primary_key=True)
            link = db.Column(db.String)    #add nullable=False
            site_name = db.Column(db.String)
            image = db.Column(db.Unicode)
            price = db.Column(db.String, default=0)
            date_added = db.Column(db.DateTime, default=datetime_ind)

        item_to_delete = Model.query.get_or_404(name)

        try:
            # Model.query.filter_by(name=name).delete()
            db.session.delete(item_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error deleting data'
    else:
        return redirect('/')      


@app.route('/update/<string:link>', methods=['GET', 'POST'])
def update(link):
    if 'username' in session:
        username = session['username']
        class Model(db.Model):
            __tablename__=username
            __table_args__ = {'extend_existing': True} 
            name = db.Column(db.String, primary_key=True)
            link = db.Column(db.String)    #add nullable=False
            site_name = db.Column(db.String)
            image = db.Column(db.Unicode)
            price = db.Column(db.String, default=0)
            date_added = db.Column(db.DateTime, default=datetime_ind)


        req = requests.get(link)
        soup = BeautifulSoup(req.content,'html.parser')
        price = soup.find('span',id="our_price_display").string


        session.query().\
        filter(Model.link == link).\
        update({"price": price})
        session.commit()


    else:
        return redirect('/signin')   


if __name__ == "__main__":
    app.run(debug=True)