import pathlib
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
YAML_SUFFIXES = {".yaml", ".yml"}

def iter_config_yaml_files():
    if not CONFIG_DIR.exists():
        return []
    files = []
    for p in CONFIG_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in YAML_SUFFIXES:
            files.append(p)
    return files

def test_config_folder_exists():
    assert CONFIG_DIR.exists() and CONFIG_DIR.is_dir(), "config/ folder missing (expected for Demo #2)"

def test_configuration_yaml_exists():
    assert (CONFIG_DIR / "configuration.yaml").exists(), "config/configuration.yaml missing"

def test_config_contains_yaml_files():
    files = iter_config_yaml_files()
    assert files, "No YAML files found under config/ (unexpected for Demo #2)"

def test_all_config_yaml_files_parse():
    bad = []
    for f in iter_config_yaml_files():
        try:
            with f.open("r", encoding="utf-8") as fh:
                yaml.safe_load(fh)
        except Exception as e:
            bad.append((str(f), str(e)))
    assert not bad, "Invalid YAML under config/:\n" + "\n".join([f"{p}: {err}" for p, err in bad])

def test_no_tabs_in_config_yaml_files():
    offenders = []
    for f in iter_config_yaml_files():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if "\t" in txt:
            offenders.append(str(f))
    assert not offenders, "Tabs found in config YAML files:\n" + "\n".join(offenders)
