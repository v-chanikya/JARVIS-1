netname := skynet
reponame := git@github.com:airavata-courses/JARVIS.git
microservices := static_webserver api_gateway
branches := a1-static-server a1-api-gateway
# For dev test
# branches := a1-static-server-dev a1-api-gateway-dev

all: checkout_code build_dockers
	echo "Building project"

checkout_code:
	echo "checking code out"
	mkdir -p build
	-for branch in ${branches} ; do \
		git clone -b $${branch} ${reponame} build/$${branch} ;\
	done
	
build_dockers:
	echo "Creating docker network"
	-docker network create ${netname};
	echo "Building and starting docker images"
	-for branch in ${branches} ; do \
		make -C build/$${branch} ;\
	done

cleanup: rm_containers rm_images
	echo "Cleaning up"
	docker network rm ${netname}

rm_containers:
	-for mserv in ${microservices}; do\
		docker stop $${mserv};\
	done

rm_images:
	-for mserv in ${microservices}; do\
		docker image rm $${mserv};\
	done
