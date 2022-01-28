all:
	echo "Building docker for static webserver"
	echo $$(pwd)
	docker run -d --net=skynet --rm -v $$(pwd)/www:/var/www  --name static_webserver \
		ubuntu/nginx
