from flask import Flask, render_template
import json
import os

app = Flask(__name__, template_folder='templates')

# Mock data based on home.json
with open('data/pages/home.json', 'r') as f:
    content = json.load(f)

# Mock config for sidebar
class User:
    email = 'admin@test.com'
    is_authenticated = True

@app.route('/')
def test():
    return render_template('admin/edit_page.html', 
                         page_id='home', 
                         content=content,
                         section_types=['hero', 'section'],
                         user=User(),
                         active_page='pages')

@app.route('/dashboard')
def dashboard(): pass

@app.route('/pages')
def pages_list(): pass

@app.route('/images')
def images(): pass

@app.route('/settings')
def settings(): pass

@app.route('/logout')
def logout(): pass

if __name__ == '__main__':
    with app.test_request_context():
        try:
            print(render_template('admin/edit_page.html', 
                         page_id='home', 
                         content=content,
                         section_types=['hero', 'section'],
                         user=User(),
                         active_page='pages'))
            print("Render Success")
        except Exception as e:
            print("Render Failed")
            print(e)
            import traceback
            traceback.print_exc()
