// frontend/src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// The Manager trait is needed to access the app handle
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // This cfg attribute ensures the sidecar only runs in release mode
            #[cfg(not(debug_assertions))]
            {
                // Get a handle to the app, which we can use to spawn the sidecar
                let handle = app.handle().clone();

                tauri::async_runtime::spawn(async move {
                    // Spawn the sidecar command
                    // The .await is important as it returns a Result
                    let (mut rx, _child) = handle.shell()
                        .sidecar("backend_server")
                        .spawn()
                        .expect("Failed to spawn sidecar");

                    while let Some(event) = rx.recv().await {
                        if let tauri::shell::SidecarEvent::Stderr(line) = event {
                            println!("Backend log: {}", line);
                        }
                    }
                });
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}