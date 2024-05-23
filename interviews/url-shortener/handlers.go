package main

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

func CreateShortURLHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var request struct {
			LongURL string `json:"long_url"`
		}
		err := json.NewDecoder(r.Body).Decode(&request)
		if err != nil {
			http.Error(w, "Error decoding the request's body", http.StatusBadRequest)
			return
		}

		shortURL, err := InsertURL(db, request.LongURL)
		if err != nil {
			http.Error(w, "Error in your request", http.StatusInternalServerError)
			return
		}

		response := map[string]string{"short_url": shortURL}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	}
}

func RedirectHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		shortURL := vars["shortURL"]

		longURL, err := GetLongURL(db, shortURL)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		if longURL == "" {
			http.NotFound(w, r)
			return
		}

		http.Redirect(w, r, longURL, http.StatusFound)
	}
}
