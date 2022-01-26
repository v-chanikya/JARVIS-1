all:
	echo "Building docker for static webserver"
	echo $$(pwd)
	docker run -d --rm -v $$(pwd)/www:/var/www  --name static_webserver \
		ubuntu/nginx
