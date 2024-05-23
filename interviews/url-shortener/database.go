package main

import (
	"database/sql"
	"errors"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

const base62Chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func InitializeDatabase(filepath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", filepath)
	if err != nil {
		return nil, err
	}

	query := `
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_url TEXT UNIQUE,
        long_url TEXT NOT NULL
    );`
	_, err = db.Exec(query)
	if err != nil {
		return nil, err
	}

	return db, nil
}

func base62Encode(num int) string {
	if num == 0 {
		return string(base62Chars[0])
	}

	result := []string{}
	base := len(base62Chars)

	for num > 0 {
		remainder := num % base
		result = append([]string{string(base62Chars[remainder])}, result...)
		num = num / base
	}

	return strings.Join(result, "")
}

func InsertURL(db *sql.DB, longURL string) (string, error) {
	result, err := db.Exec(`INSERT INTO urls (long_url) VALUES (?)`, longURL)
	if err != nil {
		return "", err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return "", err
	}

	shortURL := base62Encode(int(id))
	_, err = db.Exec(`UPDATE urls SET short_url = ? WHERE id = ?`, shortURL, id)
	if err != nil {
		return "", err
	}

	return shortURL, nil
}

func GetLongURL(db *sql.DB, shortURL string) (string, error) {
	var longURL string
	err := db.QueryRow(`SELECT long_url FROM urls WHERE short_url = ?`, shortURL).Scan(&longURL)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return "", nil
		}
		return "", err
	}
	return longURL, nil
}
