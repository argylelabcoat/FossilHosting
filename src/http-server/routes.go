package httpserver

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func Routes() {
	log.Println("Routes()")
	r := mux.NewRouter()
	// Routes consist of a path and a handler function.
	r.HandleFunc("/", Landing)

	return r
}
