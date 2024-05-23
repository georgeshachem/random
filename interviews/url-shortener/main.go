package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	db, err := InitializeDatabase("url_shortener.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	router := mux.NewRouter()

	router.HandleFunc("/shorten", CreateShortURLHandler(db)).Methods("POST")
	router.HandleFunc("/{shortURL}", RedirectHandler(db)).Methods("GET")

	log.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", router))
}
