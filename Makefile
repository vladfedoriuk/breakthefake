VERSION=2.0
build:
	docker build -t lemurpwned/hack-news:${VERSION} --platform=linux/amd64  .
push: build
	docker push lemurpwned/hack-news:${VERSION}