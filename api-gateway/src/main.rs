mod config;
mod middleware;
mod services;
mod error;

use actix_web::{web, App, HttpServer, HttpResponse};
use serde_json::json;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::Utc;
use std::sync::atomic::{AtomicU64, Ordering};

// Global startup time stored as seconds since UNIX epoch
static STARTUP_TIME: AtomicU64 = AtomicU64::new(0);

async fn health_check() -> HttpResponse {
    // Read version from VERSION file
    let version = fs::read_to_string("../VERSION")
        .unwrap_or_else(|_| "1.0.0".to_string())
        .trim()
        .to_string();

    // Calculate uptime
    let startup_time = STARTUP_TIME.load(Ordering::Relaxed);
    let current_time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let uptime_seconds = current_time - startup_time;

    // Get current UTC timestamp in ISO 8601 format
    let timestamp = Utc::now().to_rfc3339();

    HttpResponse::Ok().json(json!({
        "status": "ok",
        "version": version,
        "uptime_seconds": uptime_seconds,
        "timestamp": timestamp
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Store the startup time
    let startup_time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    STARTUP_TIME.store(startup_time, Ordering::Relaxed);

    println!("API Gateway running on port 8000");

    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health_check))
    })
    .bind("0.0.0.0:8000")?
    .run()
    .await
}