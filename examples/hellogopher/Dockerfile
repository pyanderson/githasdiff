FROM golang:1.14-alpine3.11

WORKDIR /app

COPY main.go main.go

RUN go build ./

CMD ["./app"]
