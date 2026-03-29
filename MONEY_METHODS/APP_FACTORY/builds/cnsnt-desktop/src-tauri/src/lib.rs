use std::fs;
use std::path::PathBuf;

fn vault_dir() -> PathBuf {
    let home = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
    home.join(".cnsnt")
}

fn vault_path() -> PathBuf {
    vault_dir().join("vault.enc")
}

#[tauri::command]
fn save_vault(data: String) -> Result<String, String> {
    let dir = vault_dir();
    fs::create_dir_all(&dir).map_err(|e| format!("Failed to create vault dir: {}", e))?;
    fs::write(vault_path(), &data).map_err(|e| format!("Failed to write vault: {}", e))?;
    Ok("saved".to_string())
}

#[tauri::command]
fn load_vault() -> Result<String, String> {
    let path = vault_path();
    if !path.exists() {
        return Ok(String::new());
    }
    fs::read_to_string(path).map_err(|e| format!("Failed to read vault: {}", e))
}

#[tauri::command]
fn vault_exists() -> bool {
    vault_path().exists()
}

#[tauri::command]
fn delete_vault() -> Result<String, String> {
    let path = vault_path();
    if path.exists() {
        fs::remove_file(path).map_err(|e| format!("Failed to delete vault: {}", e))?;
    }
    Ok("deleted".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            save_vault,
            load_vault,
            vault_exists,
            delete_vault,
        ])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
