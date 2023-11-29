from flask import Flask,render_template,request,redirect,url_for, session
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY']='HELLO@54'

#-----Check session for each end point except allowed routes
@app.before_request
def require_login():
    allowed_routes=['login','register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return render_template('dropsession.html')    


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""SELECT * FROM users WHERE username=? AND password=?"""
        cur.execute(query,(username,password))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        if len(rows) ==1:
            #set session
            session['username']=username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""INSERT INTO users (name,username,password) VALUES (?,?,?)"""
        cur.execute(query,(name,username,password))
        conn.commit()
        conn.close()
            #if cur.rowcount ==1:
             #   return "Registered successfully <a href='/login'>Go to Login</a>"
            #else:
             #   return "Username already exists <a href='/register'>Try Register again</a>"

        
    return render_template('register.html')


@app.route('/')
def index():
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""SELECT distinct(deckname) from cards"""
    cur.execute(query)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html',rows=rows)

@app.route('/createdeck',methods=['GET','POST'])
def createdeck():
    if request.method=="POST":
        deckname=request.form['deckname']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""INSERT INTO cards (deckname) VALUES (?)"""
        cur.execute(query,(deckname,))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('createdeck.html')

@app.route('/deletedeck/<deckname>')
def deletedeck(deckname):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""DELETE FROM cards WHERE deckname=?"""
    cur.execute(query,(deckname,))
    conn.commit()
    return redirect(url_for('index'))
    
@app.route('/deletecard/<deckname>/<sno>')
def deletecard(deckname,sno):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""DELETE FROM cards WHERE sno=?"""
    cur.execute(query,(sno,))
    conn.commit()
    return redirect(url_for('review', deckname=deckname))

@app.route('/updatedeck/<deckname>',methods=['GET','POST'])
def updatedeck(deckname):
    if request.method=="POST":
        old=deckname
        new=request.form['new']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""UPDATE cards SET deckname=? WHERE deckname=?"""
        cur.execute(query,(new,old))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('updatedeck.html',deckname=deckname)
    
@app.route('/updatecard/<deckname>/<sno>',methods=['GET','POST'])
def updatecard(deckname,sno):
    if request.method=="POST":
        old=sno
        front=request.form['front']
        back=request.form['back']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""UPDATE cards SET front=?, back=? WHERE sno=?"""
        cur.execute(query,(front,back,old))
        conn.commit()
        return redirect(url_for('review', deckname=deckname))
    return render_template('updatecard.html',sno=sno)


@app.route('/review/<deckname>')
def review(deckname):
    
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""SELECT * FROM cards WHERE deckname=? AND front IS NOT NULL ORDER BY RANDOM()"""
    
    cur.execute(query,(deckname,))
    rows=cur.fetchone()
    if rows is not None:
        return render_template('review.html',deckname=deckname,rows=rows)
    else:
        return redirect(url_for('index'))
        
   
@app.route('/addcard/<deckname>',methods=['GET','POST'])
def addcard(deckname):
    if request.method=="POST":
        front=request.form['front']
        back=request.form['back']
        
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""INSERT INTO cards (deckname,front,back) VALUES (?,?,?)"""
        cur.execute(query,(deckname,front,back))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('addcard.html',deckname=deckname)
    
@app.route('/webinfo')
def webinfo():
    return render_template('webinfo.html')

if __name__=="__main__":
    app.run(debug=True)