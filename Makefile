netname := skynet
reponame := git@github.com:airavata-courses/JARVIS.git
branches := a1-static-server a1-api-gateway
microservices := static_webserver api_gateway

all: checkout_code build_dockers create_docker_network
	echo "Building project"

checkout_code:
	echo "checking code out"
	mkdir build
	for branch in ${branches}; do;\
		git clone -b $${branch} ${reponame} build/$${branch};\
	done
	
build_dockers:
	echo "Building and starting docker images"
	for branch in ${branches}; do;\
		make -C build/$${branch};\
	done

create_docker_network:
	echo "Creating docker network"
	docker network create ${netname}
	for mserv in ${microservices}; do;\
		docker network connect ${netname} $${mserv}\
	done

cleanup: rm_containers rm_images
	echo "Cleaning up"

rm_containers:
	for mserv in ${microservices}; do;\
		docker stop $${mserv};\
		docker rm $${mserv};\
	done

rm_images:
	for mserv in ${microservices}; do;\
		docker image rm $${mserv};\
	done

