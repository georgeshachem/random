package main

type URL struct {
	ID       int    `json:"id"`
	ShortURL string `json:"short_url"`
	LongURL  string `json:"long_url"`
}
