from SimpleAdmin import app

if __name__ == '__main__':
    # Debug mode is only accesible from localhost
    #app.run(debug=True)
    app.run(host='0.0.0.0')