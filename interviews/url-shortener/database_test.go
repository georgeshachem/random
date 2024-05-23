package main

import (
	"os"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

const testDatabasePath = "url_shortener_test.db"

func TestInsertURL(t *testing.T) {
	db, err := InitializeDatabase(testDatabasePath)
	if err != nil {
		t.Fatalf("Failed to create db: %v", err)
	}
	defer db.Close()

	longURL := "http://test.com"
	_, err = InsertURL(db, longURL)
	if err != nil {
		t.Fatalf("Failed to insert URL: %v", err)
	}

	os.Remove(testDatabasePath)
}

func TestGetLongURL(t *testing.T) {
	db, err := InitializeDatabase(testDatabasePath)
	if err != nil {
		t.Fatalf("Failed to create db: %v", err)
	}
	defer db.Close()

	longURL := "http://test.com"
	shortURL, err := InsertURL(db, longURL)
	if err != nil {
		t.Fatalf("Failed to insert URL: %v", err)
	}

	retrievedLongURL, err := GetLongURL(db, shortURL)
	if err != nil {
		t.Fatalf("Failed to get long URL: %v", err)
	}

	if retrievedLongURL != longURL {
		t.Errorf("Expected long URL to be %s, got %s", longURL, retrievedLongURL)
	}

	os.Remove(testDatabasePath)
}
