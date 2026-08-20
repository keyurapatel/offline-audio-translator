import argostranslate.package as package

package.update_package_index()
available_packages = package.get_available_packages()

langs = [
    ("gu", "en"),
    ("en", "hi"),
    ("hi", "en"),
    ("en", "gu"),
    ("gu", "hi"),   # may not exist
    ("hi", "gu"),   # may not exist
]

for from_code, to_code in langs:
    pkg = next(
        (p for p in available_packages
         if p.from_code == from_code and p.to_code == to_code),
        None
    )

    if pkg is None:
        print(f"⚠️ Model not available for {from_code} -> {to_code}, skipping...")
    else:
        print(f"Installing {from_code} -> {to_code}")
        package.install_from_path(pkg.download())

print("✅ Offline translation models download finished.")
