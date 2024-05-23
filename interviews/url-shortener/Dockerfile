FROM golang:1.22-alpine AS build
RUN apk add --no-cache gcc musl-dev
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -o main .
FROM alpine:latest
COPY --from=build /app/main /main
EXPOSE 8080
CMD ["/main"]
