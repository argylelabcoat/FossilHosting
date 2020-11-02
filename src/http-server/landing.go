package httpserver

import "fmt"

func Landing(w http.ResponseWriter, r *http.Request) {
	fmt.Println("vim-go")
}
