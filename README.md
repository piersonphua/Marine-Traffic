# Marine-Traffic Webapp

Created this simple app with inspiration from VesselFinder. API is from https://aisstream.io
This application allows you to view vessel data in an interactive map format. Built with Flask and Leaflet.js, it fetches and displays vessel data, including the vessel's name, current status, and coordinates. The data is updated every 5 minutes to provide near real-time tracking.

## Setup and Installation

1. Clone the repository to your local machine.

```bash
git clone https://github.com/username/marine-traffic-webapp.git
```

2. Install the necessary Python dependencies.

```bash
pip install -r requirements.txt
```

3. Set up the PostgreSQL database.

```bash
# Please replace 'database_uri' with your PostgreSQL database URI
export SQLALCHEMY_DATABASE_URI=database_uri
```

4. Run the application.

```bash
python app.py
```

## Usage

Once the server is running, navigate to `localhost:5000` in your web browser. You will see a map displaying vessel positions. Hover over any marker to see details of the vessel.

## Data Storage and Retention

This application stores vessel data in a PostgreSQL database. It has a data retention policy that automatically deletes data older than 30 days to keep the database size manageable.

## Contributing

If you wish to contribute, please open an issue or submit a pull request.

## Contact

If you have any questions or feedback, please contact the developer:

- Pierson Phua - piersonphua@gmail.com