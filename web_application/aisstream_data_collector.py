import asyncio
import json
import websockets
import psycopg2
from datetime import datetime
from datetime import timezone

async def connect_to_api_and_store_data():
    while True:
        try:
            async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
                subscribe_message = {"APIKey": "cddcd0f0eef68e0ded72fce83d6a24424e15fb91", "BoundingBoxes": [[[1.3948, 104.0964], [1.1589, 103.5697]]]}
                subscribe_message_json = json.dumps(subscribe_message)
                await websocket.send(subscribe_message_json)

                async for message_json in websocket:
                    message = json.loads(message_json)
                    message_type = message["MessageType"]

                    if message_type == "PositionReport":
                        yield message  # Yield the entire message
                        print(message)

        except ConnectionResetError:
            print("ConnectionResetError occurred. Trying to reconnect...")

def store_in_database(message):
    # Establish a connection to the database
    connection = psycopg2.connect(
        dbname="MARINE TRAFFIC",
        user="postgres",
        password="S9642093e",
        host="localhost",
        port="5432"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Prepare your INSERT INTO statement
    insert_query = """INSERT INTO vessel_data (mmsi, shipname, navigationalstatus, latitude, longitude, timestamp)
                      VALUES (%s, %s, %s, %s, %s, %s)"""

    ais_message = message['Message']['PositionReport']
    record_to_insert = (message['MetaData'].get('MMSI', None), message['MetaData'].get('ShipName', None), ais_message.get('NavigationalStatus', None), ais_message['Latitude'], ais_message['Longitude'], datetime.now(timezone.utc))

    # Execute the SQL command
    cursor.execute(insert_query, record_to_insert)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

async def main():
    async for message in connect_to_api_and_store_data():
        store_in_database(message)


# Run the main function
asyncio.run(main())