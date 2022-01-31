all:
	echo "Building docker for api gateway"
	docker build -t api_gateway .
	docker run -d --rm --net=skynet --name api_gateway -p 80:80 api_gateway
