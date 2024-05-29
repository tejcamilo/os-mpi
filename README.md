# MPI

## Setup

This project uses environment variables for configuration. These are stored in a `.env` file.
Now you need to specify two ports. ```receiver.py``` uses the ```SOURCE_IP``` as the destination ip.

### Creating the .env file

1. In the root directory of the project, create a new file named `.env`.

2. Add your environment variables in the format `NAME=VALUE`, one per line. For example:

    ```
    SOURCE_IP=X.X.X.X
    DEST_IP=X.X.X.X
    PORT=X...
    PORT2=X....
    ```

3. Save and close the `.env` file.

### Using the .env file in Python

This project uses the `python-dotenv` library to load the `.env` file. Here's how you can use it in your Python script:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
source_ip = os.getenv('SOURCE_IP')
dest_ip = os.getenv('DEST_IP')
port = int(os.getenv('PORT'))

