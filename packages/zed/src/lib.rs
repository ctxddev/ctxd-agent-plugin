use zed_extension_api::{self as zed, settings::ContextServerSettings, Command, ContextServerId, Project, Result};

struct CtxdExtension;

#[derive(Default, serde::Deserialize)]
struct Settings {
    uvx_path: Option<String>,
    #[serde(default)]
    env: std::collections::BTreeMap<String, String>,
}

impl zed::Extension for CtxdExtension {
    fn new() -> Self {
        Self
    }

    fn context_server_command(
        &mut self,
        _id: &ContextServerId,
        project: &Project,
    ) -> Result<Command> {
        let configured = ContextServerSettings::for_project("mcp-server-ctxd", project)?;
        let settings: Settings = match configured.settings {
            Some(value) => zed::serde_json::from_value(value).map_err(|e| e.to_string())?,
            None => Settings::default(),
        };
        let command = settings.uvx_path.unwrap_or_else(|| "uvx".into());
        if command.trim().is_empty() {
            return Err("settings.uvx_path must name a uvx executable.".into());
        }
        let probe = zed::process::Command::new(&command)
            .arg("--version")
            .output()
            .map_err(|e| format!("ctxd needs uvx on Zed's PATH. Install uv or set settings.uvx_path to uvx's absolute path: {e}"))?;
        if probe.status != Some(0) {
            return Err("uvx --version failed. Set settings.uvx_path to a working uvx executable.".into());
        }
        let env = settings.env.into_iter().collect();
        Ok(Command {
            command,
            args: ["--python", "3.12", "--from", "ctxd", "ctxd-mcp"]
                .into_iter()
                .map(String::from)
                .collect(),
            env,
        })
    }
}

zed::register_extension!(CtxdExtension);
