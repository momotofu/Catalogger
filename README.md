# Catalog
Login and create your own categories and items. Upload photos, details, and just catalog stuff. Or you can remain add items to the public catalog.

## Web application features
- Github Oauth 2.0
- API for categories and items with JSON endpoints. (needs documentation)
- User login and authentication
- CRUD for categories and items

## Usage
1. download repo
2. Open your terminal and change into the root of the directory
3. Install Python dependencies by running $ `pip3 install -r requirements.txt`
4. Install JavaScript dependencies by running $ `npm i`

#### Run for production
1. Build JavaScript bundle $ `npm run build`
2. Run the application $ `python3 run.py`
3. Open your browser to $ `http://localhost:5000`

#### Run for dev mode
1. Run the dev server $ `npm start`
2. In a seperate terminal window run the application $ `python3 run.py --debug`
