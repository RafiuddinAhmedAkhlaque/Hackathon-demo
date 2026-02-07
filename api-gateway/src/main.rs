mod config;
mod middleware;
mod services;
mod error;

use actix_web::{web, App, HttpServer, HttpResponse};
use serde_json::json;

async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(json!({
        "status": "healthy",
        "service": "api-gateway"
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("API Gateway running on port 8000");

    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health_check))
    })
    .bind("0.0.0.0:8000")?
    .run()
    .await
}

