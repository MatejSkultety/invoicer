# Invoicer

A simple invoicing application with a backend service, containerized using Docker.

## Project Structure

- `invoicer-backend/` - Python backend service
	- `main.py` - Entry point for the backend API
	- `requirements.txt` - Python dependencies
	- `Dockerfile` - Containerization for the backend
- `docker-compose.yml` - Orchestrates the backend service

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Running the Application

1. Clone the repository:
	 ```sh
	 git clone <repo-url>
	 cd invoicer
	 ```
2. Start the services:
	 ```sh
	 docker-compose up --build
	 ```
3. The backend API will be available at `http://localhost:<port>` (see `docker-compose.yml` for the port).

### Stopping the Application

```sh
docker-compose down
```

## Development

- Backend code is in `invoicer-backend/`.
- Update dependencies in `requirements.txt`.
- Rebuild the container after changes:
	```sh
	docker-compose up --build
	```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.