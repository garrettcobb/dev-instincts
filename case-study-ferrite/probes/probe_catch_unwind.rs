// Ferrite's release profile sets panic = "abort" (Cargo.toml:148). Ferrite relies on
// catch_unwind as a safety net in src/fonts.rs:844 and src/markdown/mermaid/mod.rs:218,257.
fn main() {
    let r = std::panic::catch_unwind(|| { let v: Vec<u8> = Vec::new(); v[0] });
    println!("caught: {}", r.is_err());
}
