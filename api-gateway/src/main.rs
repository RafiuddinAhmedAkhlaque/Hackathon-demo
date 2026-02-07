mod config;
mod middleware;
mod services;
mod error;

use actix_web::{dev::ServiceRequest, web, App, HttpServer, HttpResponse, Result, middleware::Logger};
use actix_web::middleware::DefaultHeaders;
use serde_json::json;
use std::time::Instant;
use log::info;

async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(json!({
        "status": "healthy",
        "service": "api-gateway"
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    println!("API Gateway running on port 8000");

    HttpServer::new(|| {
        App::new()
            .wrap(Logger::new(r#"{"method":"%r","status":%s,"duration_ms":%D,"timestamp":"%t","path":"%U"}"#))
            .route("/health", web::get().to(health_check))
    })
    .bind("0.0.0.0:8000")?
    .run()
    .await
}

