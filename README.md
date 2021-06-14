
# Moodle Api

Local Server for Moodle-v2



## Run Locally

Clone the project

```bash
  git clone https://github.com/Janmejay-Joshi/moodle-api.git
```

Go to the project directory

```bash
  cd moodle-api
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 -m flask run --no-reload
```

  
## API Reference

#### Get Cached Assignments

```http
  GET /cached/${branch}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `branch` | `string` | **Required**. Branch Assignments to fetch |

#### Get Latest Assignments

```http
  GET /fetch/${branch}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `branch`  | `string` | **Required**. Branch Assignments to fetch |

#### Refetch Assignments for All Branches

```http
  GET /refetch
```

## FAQ

#### Where is the Server Running ?

The Server is running locally at http://127.0.0.1:5000/
  