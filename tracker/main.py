from flask import Flask,render_template,request
from flask import url_for,jsonify,flash,redirect


import dataRetrieve
import indices
import re


labels = ['Name','Open', 'High','Low', 'Close' , 'Adj Close' ,'Volume']


app = Flask(__name__)
@app.route('/')
def index():
    content = dataRetrieve.SheetContent(indices.get_selected_indices())

    return render_template('index.html', labels=labels, content=content,selectedTokenRed=indices.get_selected_indices(),selectedTokenAdd=indices.get_rest_indices())

@app.route('/reduceIndices',methods=['GET','POST'])
def reduceIndes():
    index = request.form.get("selectedTokenRed")
    if index == None:
        return redirect(url_for('index'))
    index=re.sub('"','',index)
    status = indices.reduce_selected_indices(index)
    # if status == True:
    #     flash('Index is removed successfully')
    # elif status == False:
    #     flash('No index can be removed')
    content = dataRetrieve.SheetContent(indices.get_selected_indices())
    # return render_template('index.html', labels=labels, content=content,selectedTokenRed=indices.get_selected_indices(),selectedTokenAdd=indices.get_rest_indices())
    return redirect(url_for('index'))

@app.route('/addIndices',methods=['GET','POST'])
def addIndex():
    index = request.form.get("selectedTokenAdd")
    if index == None:
        return redirect(url_for('index'))
    index=re.sub('"','',index)
    status = indices.add_selected_indices(index)
    content = dataRetrieve.SheetContent(indices.get_selected_indices())
    # if status == True:
    #     flash("Index is added successfully")
    # elif status == False:
    #     flash("No index can be added")
    return redirect(url_for('index'))

@app.route('/ShowIndices',methods=['GET','POST'])
def ShowIndices():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port= 44711)

# content = SheetContent(market_indices)
# print (content)
# print('Open' +"\t"+ 'High' +"\t"+ 'Low' +"\t"+ 'Close' +"\t"+ 'Adj Close' +"\t"+'Volume')
# dataRetrieve.getWeekTrans("AAPL")
# dataRetrieve.createWeekplot(dataRetrieve.getWeekTrans("AAPL"))
