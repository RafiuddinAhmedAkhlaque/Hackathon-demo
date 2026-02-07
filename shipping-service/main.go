package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/ecommerce/shipping-service/services"
)

type LogData struct {
	Method     string  `json:"method"`
	Path       string  `json:"path"`
	Status     int     `json:"status"`
	DurationMs float64 `json:"duration_ms"`
	Timestamp  string  `json:"timestamp"`
}

func jsonLoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		
		// Custom response writer to capture status code
		rw := &responseWriter{ResponseWriter: w, statusCode: 200}
		
		next.ServeHTTP(rw, r)
		
		duration := time.Since(start)
		durationMs := float64(duration.Nanoseconds()) / 1e6
		
		logData := LogData{
			Method:     r.Method,
			Path:       r.URL.Path,
			Status:     rw.statusCode,
			DurationMs: durationMs,
			Timestamp:  time.Now().UTC().Format("2006-01-02T15:04:05.000Z"),
		}
		
		logJSON, _ := json.Marshal(logData)
		fmt.Println(string(logJSON))
	})
}

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

func main() {
	rateCalculator := services.NewRateCalculator()
	_ = rateCalculator // Use the service

	mux := http.NewServeMux()

	// Health check
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{
			"status":  "healthy",
			"service": "shipping-service",
		})
	})

	// Wrap mux with logging middleware
	loggedMux := jsonLoggingMiddleware(mux)

	port := ":8007"
	fmt.Printf("Shipping Service running on port %s\n", port)
	http.ListenAndServe(port, loggedMux)
}