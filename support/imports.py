

from sqlalchemy import create_engine

# Replace 'username', 'password', 'hostname', 'port', and 'database' with your MySQL credentials
# The format is 'mysql://username:password@hostname:port/database'
connection_string = 'mysql://username:password@hostname:port/database'

# Create the engine
engine = create_engine(connection_string)

# Test the connection
try:
    engine.connect()
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
